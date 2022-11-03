import os
import traceback
from datetime import datetime
from functools import wraps

import humanize
import orjson
import pendulum
import sentry_sdk
import structlog
import typer
from calitp.storage import download_feed, GTFSDownloadConfig
from google.cloud import storage
from huey import RedisHuey
from huey.registry import Message
from huey.serializer import Serializer
from requests import HTTPError, RequestException

from .metrics import (
    FETCH_PROCESSING_TIME,
    TASK_SIGNALS,
    FETCH_PROCESSING_DELAY,
    FETCH_PROCESSED_BYTES,
)


class PydanticSerializer(Serializer):
    def _serialize(self, data: Message) -> bytes:
        return orjson.dumps(data._asdict())

    def _deserialize(self, data: bytes) -> Message:
        # deal with datetimes manually
        d = orjson.loads(data)
        d["expires_resolved"] = datetime.fromisoformat(d["expires_resolved"])
        d["kwargs"]["tick"] = datetime.fromisoformat(d["kwargs"]["tick"])
        return Message(*d.values())


huey = RedisHuey(
    name=f"gtfs-rt-archiver-v3-{os.environ['AIRFLOW_ENV']}",
    blocking=False,
    results=False,
    # serializer=PydanticSerializer(),
    url=os.getenv("CALITP_HUEY_REDIS_URL"),
    host=os.getenv("CALITP_HUEY_REDIS_HOST"),
    port=os.getenv("CALITP_HUEY_REDIS_PORT"),
    password=os.getenv("CALITP_HUEY_REDIS_PASSWORD"),
)


client = storage.Client()

structlog.configure(processors=[structlog.processors.JSONRenderer()])
base_logger = structlog.get_logger()


class RTFetchException(Exception):
    def __init__(self, url, cause, status_code=None):
        self.url = url
        self.cause = cause
        self.status_code = status_code
        super().__init__(str(self.cause))

    def __str__(self):
        return f"{self.cause} ({self.url})"


@huey.signal()
def increment_task_signals_counter(signal, task, exc=None):
    config: GTFSDownloadConfig = task.kwargs["config"]
    exc_type = ""
    # We want to let RTFetchException propagate up to Sentry so it holds the right context
    # and can be handled in the before_send hook
    # But in Grafana/Prometheus we want to group metrics by the underlying cause
    # All of this might be simplified by https://huey.readthedocs.io/en/latest/api.html#Huey.post_execute?
    if exc:
        if isinstance(exc, RTFetchException):
            exc_type = type(exc.cause).__name__
        else:
            exc_type = type(exc).__name__

    TASK_SIGNALS.labels(
        record_name=config.name,
        record_uri=config.url,
        record_feed_type=config.feed_type,
        signal=signal,
        exc_type=exc_type,
    ).inc()


auth_dict = None


@huey.on_startup()
def load_auth_dict():
    global auth_dict
    # TODO: this isn't ideal, we probably could store the keys from get_secrets_by_label() in consumer.py
    auth_dict = os.environ


# from https://github.com/getsentry/sentry-python/issues/195#issuecomment-444559126
def scoped(f):
    @wraps(f)
    def inner(*args, **kwargs):
        config: GTFSDownloadConfig = kwargs.get("config")
        # to be honest I don't really know why push_scope() does not work here
        with sentry_sdk.configure_scope() as scope:
            scope.clear_breadcrumbs()
            if config:
                scope.set_tag("config_name", config.name)
                scope.set_tag("config_url", config.url)
                scope.set_context("config", config.dict())
            return f(*args, **kwargs)

    return inner


@huey.task(expires=5)
@scoped
def fetch(tick: datetime, config: GTFSDownloadConfig):
    labels = dict(
        record_name=config.name,
        record_uri=config.url,
        record_feed_type=config.feed_type,
    )
    logger = base_logger.bind(
        tick=tick.isoformat(),
        **labels,
    )
    slippage = (pendulum.now() - tick).total_seconds()
    FETCH_PROCESSING_DELAY.labels(**labels).observe(slippage)

    with FETCH_PROCESSING_TIME.labels(**labels).time():
        try:
            extract, content = download_feed(
                config=config,
                auth_dict=auth_dict,
                ts=tick,
            )
        except Exception as e:
            status_code = None
            kwargs = dict(
                exc_type=type(e).__name__,
                exc_str=str(e),
                traceback=traceback.format_exc(),
            )
            if isinstance(e, HTTPError):
                msg = "unexpected HTTP response code from feed request"
                status_code = e.response.status_code
                kwargs.update(
                    dict(
                        code=e.response.status_code,
                        content=e.response.text,
                    )
                )
            elif isinstance(e, RequestException):
                msg = "request exception occurred from feed request"
            else:
                msg = "other non-request exception occurred during download_feed"
            logger.exception(msg, **kwargs)
            raise RTFetchException(config.url, cause=e, status_code=status_code) from e

        typer.secho(
            f"saving {humanize.naturalsize(len(content))} from {config.url} to {extract.path}"
        )
        try:
            extract.save_content(content=content, client=client, retry_metadata=True)
        except Exception as e:
            logger.exception(
                "failure occurred when saving extract or metadata",
                exc_type=type(e).__name__,
                exc_str=str(e),
                traceback=traceback.format_exc(),
            )
            raise
        FETCH_PROCESSED_BYTES.labels(
            **labels,
            content_type=extract.response_headers.get("Content-Type", "").strip(),
        ).inc(len(content))
