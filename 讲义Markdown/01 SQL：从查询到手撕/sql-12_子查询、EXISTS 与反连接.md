# sql-12 · 子查询、EXISTS 与反连接

## 查询也能当材料
子查询是括号里的查询。返回一个数的叫标量子查询，如全体平均金额；FROM 中的子查询像临时表，需要起别名。相关子查询会引用外层当前行的值。
## 有没有比连上多少更合适
EXISTS 只关心子查询是否存在至少一行。找有 paid 订单的用户时，不会因为多笔订单重复用户。NOT EXISTS 查没有匹配的用户，通常比含 NULL 风险的 NOT IN 更清楚。
## 别把“全体均值”和“用户均值”搞混
一笔订单高于全体订单均值，和一个用户总消费高于平均用户总消费，是两道不同问题。先确定比较粒度。

## 可运行例子

```sql
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
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

EXISTS 返回的核心含义是？

1. 是否存在匹配行
2. 匹配行的金额之和
3. 匹配行的第一列文字

<details><summary>答案与解释</summary>

答案：1。SELECT 1 是惯用写法，判断的是行是否存在。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "user_id"
      ],
      "rows": [
        [
          "5"
        ],
        [
          "6"
        ]
      ],
      "total": 2
    },
    {
      "columns": [
        "order_id",
        "amount"
      ],
      "rows": [
        [
          "104",
          "200.00"
        ],
        [
          "110",
          "200.00"
        ],
        [
          "112",
          "300.00"
        ]
      ],
      "total": 3
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
