# sql-10 · LEFT JOIN：保留没有订单的用户

## 左表是你要保留的人群
LEFT JOIN 保留左表每一行。没有右表匹配时，右表列填 NULL。用户没有订单也应出现在报表时，用 users 作左表。
## 条件写错位置会丢人
右表的 paid 条件写在 ON 里，表示只匹配 paid 订单；若放 WHERE o.status='paid'，没有订单的人因为 NULL 比较不是 TRUE 而被过滤，失去保留作用。
## 计数也要配合
COUNT(*) 会把无订单用户那一行也数成 1；COUNT(o.order_id) 才是订单数。金额展示为 0 用 COALESCE(SUM(o.amount),0)。

## 可运行例子

```sql
SELECT u.user_id,
   COUNT(o.order_id) AS paid_orders,
   COALESCE(SUM(o.amount),0) AS gmv
FROM users u
LEFT JOIN orders o ON u.user_id=o.user_id AND o.status='paid'
GROUP BY u.user_id
ORDER BY u.user_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

只看没有 paid 订单的用户。

提示：在分组之后添加 HAVING COUNT(o.order_id)=0。

## 自测

保留零订单用户时 paid 条件应放哪里？

1. 一定放 WHERE 中
2. ORDER BY 中
3. JOIN 的 ON 中

<details><summary>答案与解释</summary>

答案：3。WHERE 对右表条件筛选会把未匹配的 NULL 行去掉。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "user_id",
        "paid_orders",
        "gmv"
      ],
      "rows": [
        [
          "1",
          "5",
          "400.00"
        ],
        [
          "2",
          "3",
          "200.00"
        ],
        [
          "3",
          "2",
          "200.00"
        ],
        [
          "4",
          "2",
          "250.00"
        ],
        [
          "5",
          "0",
          "0.00"
        ],
        [
          "6",
          "0",
          "0.00"
        ],
        [
          "7",
          "2",
          "400.00"
        ]
      ],
      "total": 7
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
