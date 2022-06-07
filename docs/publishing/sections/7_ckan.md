(publishing-ckan)=
# Publishing data to California Open Data aka CKAN

NOTE: Only non-spatial data should be directly published to CKAN. Spatial data
(i.e. data keyed by location in some manner) has to go through the Caltrans
geoportal and is subsequently synced to CKAN.

## What is the California Open Data Portal?

The state of California hosts its own instance of CKAN, called the [California Open Data Portal](https://data.ca.gov/).
[CKAN](https://ckan.org/) is an open-source data management tool; in other words,
it allows organizations such as Caltrans to host data so that users can search
for and download data sets that might be useful for analysis or research. Among
other agencies, Caltrans publishes [many data sets](https://data.ca.gov/organization/caltrans) to CKAN.
Data is generally published as flat files (typically CSV) alongside required
metadata and a data dictionary.

## Cal-ITP data sets
* [Cal-ITP GTFS Schedule Data](https://data.ca.gov/dataset/cal-itp-gtfs-ingest-pipeline-dataset)

## General process
### Develop data models
Generally, data models should be built in dbt/BigQuery if possible. For example,
we have [latest-only GTFS schedule models](https://github.com/cal-itp/data-infra/tree/main/warehouse/models/gtfs_schedule_latest_only)
we can use to update and expand the existing [CKAN dataset](https://data.ca.gov/dataset/cal-itp-gtfs-ingest-pipeline-dataset)
[latest-only agency](https://dbt-docs.calitp.org/#!/model/model.calitp_warehouse.agency)

### Document data
California Open Data requires two documentation files for published datasets.
1. `metadata.csv` - one row per resource (i.e. file) to be published
2. `dictionary.csv` - one row per column across all resources

If you are using dbt exposure-based data publishing, you can automatically generate
these two files using the main `publish.py` script (specifically the `generate-exposure-documentation`
subcommand). The documentation from the dbt models' corresponding YAML will be
converted into appropriate CSVs and written out locally.

Run this command inside the `warehouse` folder, assuming you have local dbt
artifacts in `target/` from a `dbt run` or `dbt compile`.
```bash
poetry run python scripts/publish.py generate-exposure-documentation california_open_data
```

Generally, we recommend executing the dbt models locally and using your local
artifacts to produce the data to be generated; this ensures the data is
up-to-date and fits nicely into a tool-enabled manual workflow.

### Create dataset and metadata
Once you've generated the necessary metadata and dictionary CSV, you need to get
approval from Chad Baker. Send the CSVs via email, preferably CC'ing somebody
with a Caltrans email.

Once approved, a CKAN dataset will be created with UUIDs corresponding to each
model that will be published. If you are using dbt exposures, you will need to
update the `meta` field to map the dbt models to the appropriate UUIDs.

An example from the latest-only GTFS data exposure.
```yaml
meta:
  destinations:
    - type: ckan
      bucket: gs://calitp-publish
      format: csv
      url: https://data.ca.gov/api/3/action/resource_update
      ids:
        agency: e8f9d49e-2bb6-400b-b01f-28bc2e0e7df2
        routes: c6bbb637-988f-431c-8444-aef7277297f8
```

### Publish the data!
Either create an Airflow job to refresh/update the data at the specified
frequency, or do it manually. You can use flags to execute a dry run or write to
GCS without also uploading to CKAN.

Example dry run:
```bash
poetry run python scripts/publish.py publish-exposure california_open_data --dry-run
```

Example production deployment:
```bash
poetry run python scripts/publish.py publish-exposure california_open_data --project=cal-itp-data-infra --bucket="gs://calitp-publish" --deploy
```


If you are using dbt-based publishing, the `publish_exposure` subcommand of `publish.py`
will query BigQuery, write out CSV files, and upload those files to CKAN.