# sql-11 · 连接翻倍、自连接与笛卡尔积

## 为什么金额突然变大
一个用户有 3 笔订单、4 条登录。直接按 user_id 把两张明细连接，产生 3×4=12 行，每笔订单被重复 4 次。SUM 就会翻倍。DISTINCT 金额会误删不同订单的相同金额，无法正确修复。
## 先聚合到需要的粒度
先把订单变成一人一行金额、登录变成一人一行次数，再按用户连接。连接前先问每边的键是否唯一。
## 另外两种连接
自连接是同一张表使用两个别名，可比较同一用户前后订单；记得用时间和编号限制配对，避免自己连自己和重复对。CROSS JOIN 得到全部组合，例如日期×渠道补零框架；行数等于两侧行数相乘。
MySQL 8.0 没有原生 FULL OUTER JOIN，可用左连接加右侧未匹配行 UNION ALL 模拟，先掌握左连接即可。

## 可运行例子

```sql
WITH a AS (
  SELECT user_id,SUM(amount) AS gmv
  FROM orders
  WHERE status='paid'
  GROUP BY user_id),
   b AS (
  SELECT user_id,COUNT(*) AS login_n
  FROM logins
  GROUP BY user_id)
SELECT u.user_id,
  COALESCE(a.gmv,0) AS gmv,
  COALESCE(b.login_n,0) AS login_n
FROM users u
LEFT JOIN a ON u.user_id=a.user_id
LEFT JOIN b ON u.user_id=b.user_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

用代码结果手算用户 1 的金额是否正确。

提示：只把 paid 订单金额加一次。

## 自测

3 笔订单和 4 条登录直接按用户连接有几行？

1. 3 行
2. 12 行
3. 7 行

<details><summary>答案与解释</summary>

答案：2。每笔订单会匹配该用户的全部 4 条登录。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "user_id",
        "gmv",
        "login_n"
      ],
      "rows": [
        [
          "1",
          "400.00",
          "7"
        ],
        [
          "2",
          "200.00",
          "3"
        ],
        [
          "3",
          "200.00",
          "2"
        ],
        [
          "4",
          "250.00",
          "4"
        ],
        [
          "5",
          "0.00",
          "1"
        ],
        [
          "6",
          "0.00",
          "1"
        ],
        [
          "7",
          "400.00",
          "3"
        ]
      ],
      "total": 7
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
