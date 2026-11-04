SELECT user_id,
   SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) AS paid_n,
   SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) AS paid_amount
FROM orders
GROUP BY user_id;
