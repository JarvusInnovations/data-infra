{{ config(materialized='table') }}

WITH stg_transit_database__data_schemas AS (
    SELECT * FROM {{ ref('stg_transit_database__data_schemas') }}
),

stg_transit_database__products AS (
    SELECT * FROM {{ ref('stg_transit_database__products') }}
),

map_data_schemas_x_products_inputs AS (
 {{ transit_database_many_to_many(
     table_a = 'stg_transit_database__data_schemas',
     table_a_key_col = 'key',
     table_a_key_col_name = 'data_schema_key',
     table_a_name_col = 'name',
     table_a_name_col_name = 'data_schema_name',
     table_a_join_col = 'input_products',
     table_b = 'stg_transit_database__products',
     table_b_key_col = 'key',
     table_b_key_col_name = 'product_key',
     table_b_name_col = 'name',
     table_b_name_col_name = 'product_name',
     table_b_join_col = 'accepted_input_components'
 ) }}
)

SELECT * FROM map_data_schemas_x_products_inputs