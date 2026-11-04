# sql-21 · 复购、首单和最后一单

## 先说明复购单位
同一天两单算不算复购？有的题定义两笔 paid 订单，有的要求不同购买日，有的关注首购后 30 天内再次购买。先定义，不能套一个公式到所有场景。
## 找首单与末单
ROW_NUMBER 按 order_at、order_id 升序取第一行为首单；降序取第一行为末单。MIN(order_at) 只给时间，不能自动拿到那笔订单的其他所有字段。
## 复购率的分母
一个观察窗内，复购买家 / 至少购买一次的买家，是一种常见定义。新客 30 日复购的分母必须只含有足够 30 天观察期的新客，否则低估。

## 可运行例子

```sql
WITH buyer AS (
  SELECT user_id,COUNT(*) AS paid_orders,COUNT(DISTINCT DATE(order_at)) AS paid_days
  FROM orders
  WHERE status='paid'
  GROUP BY user_id)
SELECT COUNT(*) AS buyers,
  SUM(paid_orders>=2) AS repeat_by_orders,
  SUM(paid_days>=2) AS repeat_by_days
FROM buyer;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

同一天两单是否复购由什么决定？

1. 题目的业务定义
2. SQL 自动决定
3. 永远不算

<details><summary>答案与解释</summary>

答案：1。先约定按订单数还是不同购买日。

</details>
