WITH

idx AS (
    SELECT * FROM {{ ref('int_gtfs_quality__gtfs_dataset_schedule_guideline_index') }}
),

gtfs_datasets AS (
    SELECT * FROM {{ ref('dim_gtfs_datasets') }}
),

int_gtfs_quality__data_license AS (
    SELECT
        idx.date,
        idx.gtfs_dataset_key,
        {{ data_license() }} AS check,
        {{ compliance_schedule() }} AS feature,
        CASE manual_check__data_license
            WHEN 'Yes' THEN 'PASS'
            WHEN 'No' THEN 'FAIL'
            ELSE {{ manual_check_needed_status() }}
        END AS status,
    FROM idx
    LEFT JOIN gtfs_datasets
        ON idx.gtfs_dataset_key = gtfs_datasets.key
)

SELECT * FROM int_gtfs_quality__data_license
