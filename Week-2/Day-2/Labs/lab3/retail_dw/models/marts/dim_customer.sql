with customers as (
    select * from {{ ref("stg_customers") }}
)

select
    customer_id,
    customer_name,
    region,
    signup_date
from customers
