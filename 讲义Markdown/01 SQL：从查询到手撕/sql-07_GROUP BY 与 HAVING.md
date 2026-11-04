# sql-07 · GROUP BY 与 HAVING

## 先分组，再分别计算
GROUP BY channel 表示按渠道分组，每组做 COUNT 或 SUM。最终一行代表一个渠道，不再是一位用户。SELECT 中普通列应该是分组键，其余列应聚合；MySQL 的严格分组模式会阻止许多不明确写法。
## 筛行与筛组
WHERE 在聚合前筛明细，HAVING 在聚合后筛组。找“paid 订单总额超过 200 的用户”，paid 写 WHERE，总额超过 200 写 HAVING。
## 逻辑执行顺序
理解为 FROM/JOIN → WHERE → GROUP BY → HAVING → 窗口计算 → SELECT → DISTINCT → ORDER BY → LIMIT。优化器实际执行可调整，但这个顺序能解释为什么 WHERE 不能用窗口结果。

## 可运行例子

```sql
SELECT user_id,
   COUNT(*) AS paid_orders,
   SUM(amount) AS gmv
FROM orders
WHERE status='paid'
GROUP BY user_id
HAVING SUM(amount)>200
ORDER BY gmv DESC;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

只保留至少 3 笔 paid 订单的用户。

提示：HAVING COUNT(*) >= 3。

## 自测

筛选总额超过 200 的用户用？

1. WHERE SUM(amount)>200
2. LIMIT 200
3. HAVING SUM(amount)>200

<details><summary>答案与解释</summary>

答案：3。聚合之后才有每个用户的总额。

</details>
