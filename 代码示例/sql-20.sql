WITH d AS (
  SELECT DISTINCT user_id,DATE(login_at) AS dt
  FROM logins),
   r AS (
  SELECT *,ROW_NUMBER() OVER(PARTITION BY user_id
    ORDER BY dt) AS rn
  FROM d),
   g AS (
  SELECT *,DATE_SUB(dt,INTERVAL rn DAY) AS anchor
  FROM r)
SELECT user_id,
  MIN(dt) AS start_date,
  MAX(dt) AS end_date,
  COUNT(*) AS streak_days
FROM g
GROUP BY user_id,
  anchor
HAVING COUNT(*)>=3
ORDER BY user_id,
  start_date;
