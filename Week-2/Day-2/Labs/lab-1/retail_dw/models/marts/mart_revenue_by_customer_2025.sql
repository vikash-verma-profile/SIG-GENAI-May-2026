with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
),
lines as (
    select * from {{ ref('stg_order_lines') }}
)
select
    customers.customer_id,
    customers.customer_name,
    sum(lines.line_total) as revenue
from customers
inner join orders on orders.customer_id = customers.customer_id
inner join lines on lines.order_id = orders.order_id
where orders.order_at >= '2025-01-01' and orders.order_at < '2026-01-01'
group by customers.customer_id, customers.customer_name
order by revenue desc
limit 5
