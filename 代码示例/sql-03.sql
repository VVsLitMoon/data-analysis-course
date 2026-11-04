SELECT *
FROM users
WHERE city IN ('上海','北京');
SELECT order_id,
   order_at
FROM orders
WHERE order_at >= '2026-01-01' AND order_at < '2026-02-01';
