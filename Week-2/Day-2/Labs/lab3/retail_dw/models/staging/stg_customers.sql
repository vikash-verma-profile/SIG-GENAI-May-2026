select
    customer_id,
    trim(name) as customer_name,
    region,
    signup_date::date as signup_date
from {{ source("raw_store", "customers") }}
