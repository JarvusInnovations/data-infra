WITH source AS (
    SELECT * FROM {{ littlepay_source('external_littlepay', 'product_data') }}
),

stg_littlepay__product_data AS (
    SELECT
        participant_id,
        product_id,
        product_code,
        product_description,
        product_type,
        activation_type,
        product_status,
        created_date,
        capping_type,
        {{ safe_cast('multi_operator', type_boolean()) }} AS multi_operator,
        {{ safe_cast('capping_start_time', 'TIME') }} AS capping_start_time,
        {{ safe_cast('capping_end_time', 'TIME') }} AS capping_end_time,
        rules_transaction_types,
        rules_default_limit,
        rules_max_fare_value,
        {{ safe_cast('scheduled_start_date_time', 'DATE') }} AS scheduled_start_date_time,
        {{ safe_cast('scheduled_end_date_time', 'DATE') }} AS scheduled_end_date_time,
        {{ safe_cast('all_day', type_boolean()) }} AS all_day,
        weekly_cap_start_day,
        {{ safe_cast('number_of_days_in_cap_window', type_float()) }} AS number_of_days_in_cap_window,
        {{ safe_cast('capping_duration', type_float()) }} AS capping_duration,
        {{ safe_cast('number_of_transfer', type_float()) }} AS number_of_transfer,
        capping_time_zone,
        {{ safe_cast('capping_overlap', 'TIME') }} AS capping_overlap,
        capping_application_level,
        _line_number,
        `instance`,
        extract_filename,
        ts,
    FROM source
    QUALIFY ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY littlepay_export_ts DESC) = 1
)

SELECT * FROM stg_littlepay__product_data