# sql-19 · 留存率：先定义 cohort 和观察窗

## 同一起点的人放在一组
cohort 是具有同一入组时间或特征的人群。注册次日留存率：某日注册用户中，在注册日后第 1 个自然日登录的人数 / 该日注册人数。它不是“所有今天活跃者里昨天也活跃的比例”。
## 为什么先去重
同一用户次日登录 5 次也只算 1 位留存用户。把登录明细先转为用户—日期唯一记录，再连接注册人群，防止分子分母被重复。
## 尚未观察不能当流失
数据只到 1 月 31 日时，1 月 31 日注册的次日留存还不可观察，应排除或标记未成熟，而不是按 0。D1、D7、7 日内回访和第 7 日回访是不同定义。

## 可运行例子

```sql
WITH d AS (
  SELECT DISTINCT user_id,DATE(login_at) AS dt
  FROM logins)
SELECT u.signup_date,
  COUNT(*) AS new_users,
  COUNT(d.user_id) AS retained_users,
  ROUND(COUNT(d.user_id)/COUNT(*),4) AS d1_retention
FROM users u
LEFT JOIN d ON u.user_id=d.user_id AND d.dt=DATE_ADD(u.signup_date,INTERVAL 1 DAY)
WHERE u.signup_date < '2026-03-31'
GROUP BY u.signup_date
ORDER BY u.signup_date;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

改成注册第 2 天登录的留存。

提示：INTERVAL 1 DAY 改成 2 DAY，并同步调整可观察边界。

## 自测

一个新用户次日登录 5 次，应计多少留存用户？

1. 5
2. 0
3. 1

<details><summary>答案与解释</summary>

答案：3。留存的计量单位是用户。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "signup_date",
        "new_users",
        "retained_users",
        "d1_retention"
      ],
      "rows": [
        [
          "2026-01-01",
          "2",
          "1",
          "0.5000"
        ],
        [
          "2026-01-02",
          "1",
          "1",
          "1.0000"
        ],
        [
          "2026-01-03",
          "1",
          "1",
          "1.0000"
        ],
        [
          "2026-01-05",
          "1",
          "0",
          "0.0000"
        ],
        [
          "2026-01-08",
          "1",
          "0",
          "0.0000"
        ],
        [
          "2026-01-31",
          "1",
          "1",
          "1.0000"
        ]
      ],
      "total": 6
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
