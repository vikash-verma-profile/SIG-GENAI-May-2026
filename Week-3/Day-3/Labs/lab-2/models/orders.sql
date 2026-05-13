-- dbt-style model: upstream dependency raw_orders -> orders
SELECT *
FROM {{ ref('raw_orders') }}
