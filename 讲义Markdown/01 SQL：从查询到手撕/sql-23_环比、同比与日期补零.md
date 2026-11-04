# sql-23 · 环比、同比与日期补零

## 比较的基准是什么
环比是与上一个可比周期相比，同比增长是与去年同周期相比。增长率 = (本期 - 基期) / 基期。基期为 0 时标记不可直接计算，不要伪装成 0% 增长。
## 缺失月份不应跳过
先造月份表，左连接月度金额，将确实无订单的月份补零，再 LAG。数据未到齐的月份应标记不完整，不能随意补零。
## 可比性比公式重要
本月只有前 10 天，不能直接和上个月完整月比较；春节错位、天数不同、退款延迟也会影响结果。下面教学日历完整，因此可以示范补零。

## 可运行例子

```sql
WITH months AS (
  SELECT DISTINCT DATE_FORMAT(dt,'%Y-%m') AS mon
  FROM calendar),
   m AS (
  SELECT DATE_FORMAT(order_at,'%Y-%m') AS mon,SUM(amount) AS gmv
  FROM orders
  WHERE status='paid'
  GROUP BY mon),
   filled AS (
  SELECT months.mon,COALESCE(m.gmv,0) AS gmv
  FROM months
  LEFT JOIN m USING(mon)),
   lagged AS (
  SELECT *,LAG(gmv) OVER(
    ORDER BY mon) AS previous_gmv
  FROM filled)
SELECT *,
  ROUND((gmv-previous_gmv)/NULLIF(previous_gmv,0),4) AS mom
FROM lagged
ORDER BY mon;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

基期为 0 时，通常应该？

1. 增长率一定 100%
2. 标记相对增长不可直接计算
3. 增长率一定 0%

<details><summary>答案与解释</summary>

答案：2。公式分母为零，需要单独说明。

</details>
