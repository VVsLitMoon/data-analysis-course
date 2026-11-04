WITH d AS (
  SELECT DISTINCT user_id,DATE(login_at) AS dt
  FROM logins)
SELECT u.signup_date,
  COUNT(*) AS new_users,
  COUNT(d.user_id) AS retained_users,
  ROUND(COUNT(d.user_id)/COUNT(*),4) AS d1_retention
FROM users u
LEFT JOIN d ON u.user_id=d.user_id AND d.dt=DATE_ADD(u.signup_date,INTERVAL 1 DAY)
WHERE u.signup_date < '2026-03-31'
GROUP BY u.signup_date
ORDER BY u.signup_date;
