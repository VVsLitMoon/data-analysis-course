# sql-06 · 聚合：COUNT、SUM、AVG、MIN、MAX

## 把多行变成摘要
SUM(amount) 把金额相加，AVG 求平均，MIN/MAX 找最小最大。没有 GROUP BY 时，整个筛选结果作为一个组，通常返回一行摘要。
## 计数有三种
COUNT(*) 数所有行；COUNT(city) 数城市非空的行；COUNT(DISTINCT user_id) 数不同且非空的用户。订单数和购买人数因此不同。
## 没有数据怎么办
无符合记录时 COUNT 为 0，SUM 和 AVG 通常为 NULL。业务明确需要零时再 COALESCE(SUM(amount),0)。AVG 会忽略空值；把空值补零以后平均值会改变。

## 可运行例子

```sql
SELECT COUNT(*) AS paid_orders,
   COUNT(DISTINCT user_id) AS buyers,
   SUM(amount) AS gmv,
   AVG(amount) AS aov
FROM orders
WHERE status='paid';
SELECT COUNT(*) AS users,
   COUNT(city) AS known_city_users
FROM users;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

筛出 2026 年 2 月 paid 订单再算上述指标。

提示：WHERE 再追加左闭右开的日期范围。

## 自测

购买人数通常应该怎样统计？

1. COUNT(DISTINCT user_id)
2. COUNT(*) 一定可以
3. SUM(user_id)

<details><summary>答案与解释</summary>

答案：1。同一个买家可能有多笔订单。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "paid_orders",
        "buyers",
        "gmv",
        "aov"
      ],
      "rows": [
        [
          "14",
          "5",
          "1450.00",
          "103.571429"
        ]
      ],
      "total": 1
    },
    {
      "columns": [
        "users",
        "known_city_users"
      ],
      "rows": [
        [
          "7",
          "6"
        ]
      ],
      "total": 1
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
