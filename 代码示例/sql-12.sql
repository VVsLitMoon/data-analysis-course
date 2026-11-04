SELECT u.user_id
FROM users u
WHERE NOT EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.user_id=u.user_id AND o.status='paid');
SELECT order_id,
  amount
FROM orders
WHERE status='paid' AND amount>(
  SELECT AVG(amount)
  FROM orders
  WHERE status='paid');
