SELECT COUNT(*) AS all_rows,
   COUNT(DISTINCT user_id) AS users_with_orders
FROM orders;
