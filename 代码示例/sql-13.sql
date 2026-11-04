WITH paid AS (
  SELECT *
  FROM orders
  WHERE status='paid'),
   spend AS (
  SELECT user_id,SUM(amount) AS gmv
  FROM paid
  GROUP BY user_id)
SELECT *
FROM spend
WHERE gmv>=200
ORDER BY user_id;
SELECT 'A' AS label
UNION ALL
SELECT 'A';
