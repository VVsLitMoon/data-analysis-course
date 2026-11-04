WITH buyer AS (
  SELECT user_id,COUNT(*) AS paid_orders,COUNT(DISTINCT DATE(order_at)) AS paid_days
  FROM orders
  WHERE status='paid'
  GROUP BY user_id)
SELECT COUNT(*) AS buyers,
  SUM(paid_orders>=2) AS repeat_by_orders,
  SUM(paid_days>=2) AS repeat_by_days
FROM buyer;
