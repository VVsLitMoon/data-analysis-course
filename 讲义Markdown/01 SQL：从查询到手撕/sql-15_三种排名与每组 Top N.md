# sql-15 · 三种排名与每组 Top N

## 先用 100、100、80 理解
ROW_NUMBER 给出 1、2、3；RANK 给出 1、1、3；DENSE_RANK 给出 1、1、2。ROW_NUMBER 需要稳定的并列打破规则，例如 order_id；RANK/DENSE_RANK 如果把唯一编号加入排名排序，就破坏金额并列语义。
## “前 3”必须问清楚
恰好最多 3 行选 ROW_NUMBER<=3；前三种不同金额选 DENSE_RANK<=3；竞赛名次前三选 RANK<=3，可能不足三种金额。面试说明你采用哪一种。
## 查询结构
内层计算每个用户内的金额名次，外层筛 rn<=2。外层排序只是方便阅读，不改变名次定义。

## 可运行例子

```sql
WITH ranked AS (
  SELECT order_id,user_id,amount,ROW_NUMBER() OVER(PARTITION BY user_id
    ORDER BY amount DESC,order_id) AS rn
  FROM orders
  WHERE status='paid')
SELECT *
FROM ranked
WHERE rn<=2
ORDER BY user_id,
  rn;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

输出每个用户最大的两种金额，保留并列。

提示：用 DENSE_RANK，窗口排序只保留 amount DESC。

## 自测

100、100、80 的 DENSE_RANK 是？

1. 1、1、2
2. 1、2、3
3. 1、1、3

<details><summary>答案与解释</summary>

答案：1。密集排名保留并列且不跳号。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "order_id",
        "user_id",
        "amount",
        "rn"
      ],
      "rows": [
        [
          "104",
          "1",
          "200.00",
          "1"
        ],
        [
          "101",
          "1",
          "100.00",
          "2"
        ],
        [
          "114",
          "2",
          "100.00",
          "1"
        ],
        [
          "106",
          "2",
          "80.00",
          "2"
        ],
        [
          "108",
          "3",
          "100.00",
          "1"
        ],
        [
          "109",
          "3",
          "100.00",
          "2"
        ],
        [
          "110",
          "4",
          "200.00",
          "1"
        ],
        [
          "111",
          "4",
          "50.00",
          "2"
        ],
        [
          "112",
          "7",
          "300.00",
          "1"
        ],
        [
          "113",
          "7",
          "100.00",
          "2"
        ]
      ],
      "total": 10
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
