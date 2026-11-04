SELECT COUNT(*) AS paid_orders,
   COUNT(DISTINCT user_id) AS buyers,
   SUM(amount) AS gmv,
   AVG(amount) AS aov
FROM orders
WHERE status='paid';
SELECT COUNT(*) AS users,
   COUNT(city) AS known_city_users
FROM users;
