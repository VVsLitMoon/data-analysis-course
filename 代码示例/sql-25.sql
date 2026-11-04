WITH r AS (
  SELECT amount,ROW_NUMBER() OVER(
    ORDER BY amount,order_id) AS rn,COUNT(*) OVER() AS n
  FROM orders
  WHERE status='paid')
SELECT AVG(amount) AS median_amount
FROM r
WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2));
