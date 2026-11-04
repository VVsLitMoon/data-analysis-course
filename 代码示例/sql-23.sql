WITH months AS (
  SELECT DISTINCT DATE_FORMAT(dt,'%Y-%m') AS mon
  FROM calendar),
   m AS (
  SELECT DATE_FORMAT(order_at,'%Y-%m') AS mon,SUM(amount) AS gmv
  FROM orders
  WHERE status='paid'
  GROUP BY mon),
   filled AS (
  SELECT months.mon,COALESCE(m.gmv,0) AS gmv
  FROM months
  LEFT JOIN m USING(mon)),
   lagged AS (
  SELECT *,LAG(gmv) OVER(
    ORDER BY mon) AS previous_gmv
  FROM filled)
SELECT *,
  ROUND((gmv-previous_gmv)/NULLIF(previous_gmv,0),4) AS mom
FROM lagged
ORDER BY mon;
