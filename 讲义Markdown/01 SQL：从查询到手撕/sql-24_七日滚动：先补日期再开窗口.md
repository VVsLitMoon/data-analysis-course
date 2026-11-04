# sql-24 · 七日滚动：先补日期再开窗口

## 把文字口径变成边界
“截至当天的近 7 个自然日”包含当天和前 6 天；“过去 7 天且不含当天”则是前 7 天至前 1 天。半开区间能避免午夜边界重复。
## 两层查询各做一件事
先以 calendar 为左表补全每日 paid 金额，再在这张一日一行表上做 ROWS 6 PRECEDING。因为 calendar 从 1 月 1 日开始，头 6 天窗口少于 7 个观察日。
## 筛日期的位置会改变窗口
若只想展示 1 月 7 日以后的结果，应先计算含前六天的窗口，再在外层筛日期。提前删掉历史日期会导致首行窗口不完整。

## 可运行例子

```sql
WITH daily AS (
  SELECT c.dt,COALESCE(SUM(o.amount),0) AS gmv
  FROM calendar c
  LEFT JOIN orders o ON DATE(o.order_at)=c.dt AND o.status='paid'
  GROUP BY c.dt),
   rolling AS (
  SELECT *,SUM(gmv) OVER(
    ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS gmv_7d
  FROM daily)
SELECT *
FROM rolling
WHERE dt BETWEEN '2026-01-07' AND '2026-01-12'
ORDER BY dt;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

展示日期筛选通常放在何时？

1. 计算完整窗口之后
2. 必须在窗口之前
3. 不能筛选

<details><summary>答案与解释</summary>

答案：1。否则历史行被提前移走，窗口起点会错误。

</details>
