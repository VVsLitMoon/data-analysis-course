SELECT user_id,
   COALESCE(city,'未知') AS city_label
FROM users;
SELECT 3.0 / NULLIF(0,0) AS safe_ratio;
