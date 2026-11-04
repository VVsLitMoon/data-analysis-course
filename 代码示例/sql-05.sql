SELECT order_id,
   amount
FROM orders
WHERE status='paid'
ORDER BY amount DESC,
   order_id
LIMIT 3;
SELECT DISTINCT user_id,
   category
FROM orders
ORDER BY user_id,
   category;
