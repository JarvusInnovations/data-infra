{{ config(materialized='table') }}

WITH type2 as (
    select *
    from {{ source('gtfs_type2', 'transfers') }}
)

, transfers_clean as (

    -- Trim all string fields
    -- Incoming schema explicitly defined in gtfs_schedule_history external table definition

    SELECT
        calitp_itp_id
        , calitp_url_number
        , TRIM(from_stop_id) as from_stop_id
        , TRIM(to_stop_id) as to_stop_id
        , TRIM(transfer_type) as transfer_type
        , calitp_extracted_at
        , calitp_hash
        , FARM_FINGERPRINT(CONCAT(CAST(calitp_hash AS STRING), "___", CAST(calitp_extracted_at AS STRING))) AS transfer_key
        , COALESCE(calitp_deleted_at, "2099-01-01") AS calitp_deleted_at
    FROM type2
)

SELECT * FROM transfers_clean
