select
    order_id,
    customer_id,
    order_date::timestamp_ntz as order_at,
    lower(trim(status)) as order_status
from {{ source("raw_store", "orders") }}
