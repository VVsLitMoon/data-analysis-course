SELECT user_id,
   COUNT(*) AS paid_orders,
   SUM(amount) AS gmv
FROM orders
WHERE status='paid'
GROUP BY user_id
HAVING SUM(amount)>200
ORDER BY gmv DESC;
