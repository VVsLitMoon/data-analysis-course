# sql-14 · 窗口函数：保留明细，也看组内信息

## 聚合和窗口的差别
GROUP BY 会把多行收成一行；窗口函数给每行增加组内计算结果，保留原来明细。想同时看每笔订单金额和该用户总额时，窗口很合适。
## 三个组成部分
SUM(amount) OVER(PARTITION BY user_id) 中 SUM 是计算，PARTITION BY 按用户分区，OVER 告诉数据库这是窗口计算。窗口内 ORDER BY 指定计算顺序；最终输出顺序仍需查询末尾 ORDER BY。
## 先筛再算
WHERE status='paid' 会先筛掉非支付订单，窗口只看筛后的行。窗口结果不能直接写在同层 WHERE，先放 CTE，再由外层筛选。

## 可运行例子

```sql
SELECT order_id,
  user_id,
  amount,
  SUM(amount) OVER(PARTITION BY user_id) AS user_total
FROM orders
WHERE status='paid'
ORDER BY user_id,
  order_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

去掉 PARTITION BY user_id，观察每行总额。

提示：OVER() 表示把全部输入行当同一窗口。

## 自测

窗口 SUM 默认会把每个用户压成一行吗？

1. 只能用在一张一行的表
2. 不会，保留输入行
3. 会

<details><summary>答案与解释</summary>

答案：2。这正是窗口和 GROUP BY 的关键区别。

</details>
