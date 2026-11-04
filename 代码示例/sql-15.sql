WITH ranked AS (
  SELECT order_id,user_id,amount,ROW_NUMBER() OVER(PARTITION BY user_id
    ORDER BY amount DESC,order_id) AS rn
  FROM orders
  WHERE status='paid')
SELECT *
FROM ranked
WHERE rn<=2
ORDER BY user_id,
  rn;
