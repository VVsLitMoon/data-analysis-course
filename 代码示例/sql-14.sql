SELECT order_id,
  user_id,
  amount,
  SUM(amount) OVER(PARTITION BY user_id) AS user_total
FROM orders
WHERE status='paid'
ORDER BY user_id,
  order_id;
