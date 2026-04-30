-- Total revenue per region
SELECT
  c.region,
  SUM(o.order_total) AS total_revenue
FROM orders o
JOIN customers c
  ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

-- Customer details against each order (with region total)
SELECT
  o.order_id,
  o.order_date,
  o.order_total,
  c.customer_id,
  c.customer_name,
  c.email,
  c.region,
  SUM(o.order_total) OVER (PARTITION BY c.region) AS region_total_revenue
FROM orders o
JOIN customers c
  ON c.customer_id = o.customer_id
ORDER BY c.region, o.order_date, o.order_id;
