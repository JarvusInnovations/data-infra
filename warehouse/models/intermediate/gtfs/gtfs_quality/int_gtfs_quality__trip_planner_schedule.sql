WITH

idx AS (
    SELECT * FROM {{ ref('int_gtfs_quality__services_guideline_index') }}
),

services AS (
    SELECT * FROM {{ ref('dim_services') }}
),

int_gtfs_quality__trip_planner_schedule AS (
    SELECT
        idx.date,
        idx.service_key,
        {{ trip_planner_schedule() }} AS check,
        {{ compliance_schedule() }} AS feature,
        CASE manual_check__gtfs_schedule_data_ingested_in_trip_planner
            WHEN 'Yes' THEN 'PASS'
            WHEN 'No' THEN 'FAIL'
            ELSE {{ manual_check_needed_status() }}
        END AS status,
    FROM idx
    LEFT JOIN services
        ON idx.service_key = services.key
)

SELECT * FROM int_gtfs_quality__trip_planner_schedule