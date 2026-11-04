SELECT order_id,
  user_id,
  amount,
  SUM(amount) OVER(PARTITION BY user_id
  ORDER BY order_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_gmv
FROM orders
WHERE status='paid'
ORDER BY user_id,
  order_at,
  order_id;
