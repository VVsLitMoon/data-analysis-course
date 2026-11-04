# sql-16 · LAG、LEAD 与相邻比较

## 向前看和向后看
LAG(value) 取排序后上一行的值，LEAD 取下一行。第一行没有上一行通常返回 NULL。PARTITION BY 决定在哪个人或哪类商品内部移动。
## 上一行不等于昨天
如果某用户只在 1 日和 5 日下单，LAG 得到的是上一笔订单日期 1 日，不是 4 日。月度数据缺了 2 月时，3 月上一行可能是 1 月，做环比要先补全月份。
## 稳定排序
按时间再按订单号排列，才能在同一时刻多笔订单时保持确定。相邻时间差用 TIMESTAMPDIFF(单位,先前,当前)。

## 可运行例子

```sql
WITH t AS (
  SELECT order_id,user_id,order_at,LAG(order_at) OVER(PARTITION BY user_id
    ORDER BY order_at,order_id) AS previous_at
  FROM orders
  WHERE status='paid')
SELECT *,
  TIMESTAMPDIFF(HOUR,previous_at,order_at) AS gap_hours
FROM t
ORDER BY user_id,
  order_at,
  order_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

LAG 取到的必定是昨天吗？

1. 是
2. 只取最小值
3. 不是，是排序后的上一行

<details><summary>答案与解释</summary>

答案：3。日历连续性必须另行保证。

</details>
