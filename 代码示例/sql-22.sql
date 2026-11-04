SELECT COUNT(DISTINCT CASE WHEN event_type='view' THEN user_id END) AS viewers,
  COUNT(DISTINCT CASE WHEN event_type='cart' THEN user_id END) AS cart_users,
  COUNT(DISTINCT CASE WHEN event_type='pay' THEN user_id END) AS pay_users
FROM events
WHERE event_at>='2026-01-01' AND event_at<'2026-01-02';
