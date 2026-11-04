SELECT order_id,
   user_id,
   amount
FROM orders
WHERE status = 'paid' AND amount >= 100;
