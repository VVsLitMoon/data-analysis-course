SELECT u.user_id,
   COUNT(o.order_id) AS paid_orders,
   COALESCE(SUM(o.amount),0) AS gmv
FROM users u
LEFT JOIN orders o ON u.user_id=o.user_id AND o.status='paid'
GROUP BY u.user_id
ORDER BY u.user_id;
