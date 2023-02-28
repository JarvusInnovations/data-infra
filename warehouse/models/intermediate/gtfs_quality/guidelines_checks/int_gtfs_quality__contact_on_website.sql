WITH

idx AS (
    SELECT * FROM {{ ref('int_gtfs_quality__organization_guideline_index') }}
),

organizations AS (
    SELECT * FROM {{ ref('dim_organizations') }}
),

int_gtfs_quality__contact_on_website AS (
    SELECT
        idx.date,
        idx.organization_key,
        {{ organization_has_contact_info() }} AS check,
        {{ technical_contact_availability() }} AS feature,
        CASE manual_check__contact_on_website
            WHEN 'Yes' THEN {{ guidelines_pass_status() }}
            WHEN 'No' THEN {{ guidelines_fail_status() }}
            ELSE {{ guidelines_manual_check_needed_status() }}
        END AS status,
    FROM idx
    LEFT JOIN organizations
        ON idx.organization_key = organizations.key
)

SELECT * FROM int_gtfs_quality__contact_on_website