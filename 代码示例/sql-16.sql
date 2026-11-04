WITH t AS (
  SELECT order_id,user_id,order_at,LAG(order_at) OVER(PARTITION BY user_id
    ORDER BY order_at,order_id) AS previous_at
  FROM orders
  WHERE status='paid')
SELECT *,
  TIMESTAMPDIFF(HOUR,previous_at,order_at) AS gap_hours
FROM t
ORDER BY user_id,
  order_at,
  order_id;
