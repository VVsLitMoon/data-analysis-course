WITH daily AS (
  SELECT c.dt,COALESCE(SUM(o.amount),0) AS gmv
  FROM calendar c
  LEFT JOIN orders o ON DATE(o.order_at)=c.dt AND o.status='paid'
  GROUP BY c.dt),
   rolling AS (
  SELECT *,SUM(gmv) OVER(
    ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS gmv_7d
  FROM daily)
SELECT *
FROM rolling
WHERE dt BETWEEN '2026-01-07' AND '2026-01-12'
ORDER BY dt;
