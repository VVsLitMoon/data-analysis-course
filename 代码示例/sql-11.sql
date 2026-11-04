WITH a AS (
  SELECT user_id,SUM(amount) AS gmv
  FROM orders
  WHERE status='paid'
  GROUP BY user_id),
   b AS (
  SELECT user_id,COUNT(*) AS login_n
  FROM logins
  GROUP BY user_id)
SELECT u.user_id,
  COALESCE(a.gmv,0) AS gmv,
  COALESCE(b.login_n,0) AS login_n
FROM users u
LEFT JOIN a ON u.user_id=a.user_id
LEFT JOIN b ON u.user_id=b.user_id;
