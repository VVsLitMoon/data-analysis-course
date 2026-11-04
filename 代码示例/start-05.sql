SELECT status,
   COUNT(*) AS n,
   SUM(amount) AS amount_sum
FROM orders
GROUP BY status;
SELECT *
FROM users
WHERE city IS NULL;
