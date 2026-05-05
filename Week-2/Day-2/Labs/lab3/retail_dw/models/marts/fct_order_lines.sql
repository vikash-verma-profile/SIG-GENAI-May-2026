with lines as (
    select * from {{ ref("stg_order_lines") }}
),
orders as (
    select * from {{ ref("stg_orders") }}
)

select
    lines.order_line_id,
    lines.order_id,
    lines.product_id,
    orders.customer_id,
    orders.order_at,
    orders.order_status,
    lines.quantity,
    lines.line_total
from lines
inner join orders on orders.order_id = lines.order_id
