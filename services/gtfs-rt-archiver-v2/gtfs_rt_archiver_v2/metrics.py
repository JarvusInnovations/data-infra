from prometheus_client import Summary, Counter, Gauge

FEEDS_IN_PROGRESS = Gauge(
    name="feeds_in_progress",
    documentation="Feeds currently being downloaded/uploaded.",
    labelnames=("url",),
)
FEEDS_DOWNLOADED = Counter(
    name="downloaded_feeds",
    documentation="Feeds sucessfully downloaded.",
    labelnames=("url",),
)
HANDLE_TICK_PROCESSED_BYTES = Counter(
    name="handled_bytes",
    documentation="Count of bytes fully handled (i.e. down/upload).",
    labelnames=("url",),
)
HANDLE_TICK_PROCESSING_DELAY = Summary(
    name="handle_tick_processing_delay_seconds",
    documentation="The slippage between a tick and full download of a feed.",
    labelnames=("url",),
)
HANDLE_TICK_PROCESSING_TIME = Summary(
    name="handle_tick_processing_time_seconds",
    documentation="Time spent processing a single tick.",
    labelnames=("url",),
)
TICKS = Counter(
    name="ticks",
    documentation="Ticks triggered by the scheduler.",
)
TASK_SIGNALS = Counter(
    name="huey_task_signals",
    documentation="All huey task signals.",
    labelnames=("signal", "exc_type"),
)
