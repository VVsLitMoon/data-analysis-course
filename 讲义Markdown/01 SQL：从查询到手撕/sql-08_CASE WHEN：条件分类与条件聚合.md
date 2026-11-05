# sql-08 · CASE WHEN：条件分类与条件聚合

## 在 SQL 中表达“如果”
CASE WHEN 条件 THEN 结果 ELSE 其他结果 END。按顺序检查，第一个成立的分支生效，漏写 ELSE 时未匹配的行返回 NULL。不同分支尽量保持相同数据类型。
## 条件计数为什么成立
CASE WHEN status='paid' THEN 1 ELSE 0 END 把 paid 订单变成 1，其余变成 0；再 SUM 就是 paid 行数。COUNT(CASE WHEN 条件 THEN 1 END) 也可计数，因为未命中返回 NULL。
## 一个常见错误
COUNT(CASE WHEN 条件 THEN 1 ELSE 0 END) 会把 0 也计入，所以数的是全部非空行。条件金额用 SUM(CASE WHEN 条件 THEN amount ELSE 0 END)。

## 可运行例子

```sql
SELECT user_id,
   SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) AS paid_n,
   SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) AS paid_amount
FROM orders
GROUP BY user_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

增加取消订单数量。

提示：新增 SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END)。

## 自测

COUNT(CASE WHEN 条件 THEN 1 ELSE 0 END) 会？

1. 只计 0
2. 把 0 和 1 都计数
3. 只计 1

<details><summary>答案与解释</summary>

答案：2。COUNT 关心是不是 NULL，不关心是不是 0。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "user_id",
        "paid_n",
        "paid_amount"
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
          "7",
          "2",
          "400.00"
        ],
        [
          "5",
          "0",
          "0.00"
        ]
      ],
      "total": 6
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
