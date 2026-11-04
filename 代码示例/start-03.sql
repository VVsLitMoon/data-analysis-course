SELECT user_id,
   COUNT(*) AS order_rows
FROM orders
GROUP BY user_id;
