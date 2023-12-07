SELECT
  organization,
  reportstatus as api_report_status,
  TIMESTAMP_MILLIS(reportlastmodifieddate) as api_report_last_modified_date,
  reportperiod as api_report_period,
  a30.id as id,
  a30.VehicleId as vehicle_id,
  a30.NTDID as ntd_id,
  a30.VehicleLength as vehicle_length,
  a30.FuelType as fuel_type,
  a30.FundSource as fund_source,
  a30.ReportId as report_id,
  a30.AverageEstimatedServiceYearsWhenNew as average_estimated_service_years_when_new,
  a30.VehicleStatus as vehicle_status,
  a30.Vin as vin,
  a30.ADAAccess as ada_access,
  a30.VehicleType as vehicle_type,
  a30.AverageExpirationYearsWhenNew as average_expiration_years_when_new,
  a30.VehicleYear as vehicle_year,
  a30.UsefulLifeYearsRemaining as useful_life_years_remaining,
  a30.SeatingCapacity as seating_capacity,
  a30.OwnershipType as ownership_type,
  a30.ModesOperatedDisplayText as modes_operated_display_text,
  a30.ModesOperatedFullText as modes_operated_full_text,
  a30.LastModifiedDate as last_modified_date
FROM {{ source('ntd_report_validation', 'all_ntdreports') }},
 UNNEST(`ntdassetandresourceinfo_data`) as `a30`
