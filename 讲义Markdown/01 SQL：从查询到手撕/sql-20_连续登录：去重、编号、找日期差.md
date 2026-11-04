# sql-20 · 连续登录：去重、编号、找日期差

## 连续天数不是登录次数
某人在 1 日登录两次、2 日一次、3 日一次，连续是 3 天，不能说 4 天。第一层先取 DISTINCT user_id, DATE(login_at)。
## 连续日期减连续编号得到同一个锚点
1 月 1、2、3 日的序号是 1、2、3，各自减序号天都指向同一天。5、6 日减后续序号得到另一个锚点。按用户与锚点分组，就得到每段连续区间。
## 面试讲法
先说明每日去重，再用 ROW_NUMBER 按日编号，再用 DATE_SUB 生成分组锚点，最后 COUNT 得连续长度。可进一步取每人最大长度或筛至少三天。

## 可运行例子

```sql
WITH d AS (
  SELECT DISTINCT user_id,DATE(login_at) AS dt
  FROM logins),
   r AS (
  SELECT *,ROW_NUMBER() OVER(PARTITION BY user_id
    ORDER BY dt) AS rn
  FROM d),
   g AS (
  SELECT *,DATE_SUB(dt,INTERVAL rn DAY) AS anchor
  FROM r)
SELECT user_id,
  MIN(dt) AS start_date,
  MAX(dt) AS end_date,
  COUNT(*) AS streak_days
FROM g
GROUP BY user_id,
  anchor
HAVING COUNT(*)>=3
ORDER BY user_id,
  start_date;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

找至少连续 2 天的区间。

提示：修改 HAVING 阈值即可。

## 自测

连续登录题的第一步是什么？

1. 只保留每人第一天
2. 按用户和自然日去重
3. 直接数登录行数

<details><summary>答案与解释</summary>

答案：2。一天的多次登录不能增加连续天数。

</details>
