SELECT u.channel,
   COUNT(*) AS paid_orders,
   SUM(o.amount) AS gmv
FROM users u
JOIN orders o ON u.user_id=o.user_id
WHERE o.status='paid'
GROUP BY u.channel;
