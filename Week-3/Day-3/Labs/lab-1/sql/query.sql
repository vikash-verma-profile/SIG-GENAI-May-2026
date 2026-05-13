SELECT c.customer_id,
       o.amount
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id;
