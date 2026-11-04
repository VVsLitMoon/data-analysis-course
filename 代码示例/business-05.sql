SELECT user_id,
  DATEDIFF('2026-04-01',MAX(DATE(order_at))) AS recency_days,
  COUNT(*) AS frequency,
  SUM(amount) AS monetary
FROM orders
WHERE status='paid' AND order_at<'2026-04-01'
GROUP BY user_id
ORDER BY user_id;
