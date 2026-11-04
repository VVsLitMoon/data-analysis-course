# sql-18 · 日期、字符串、类型转换和数值精度

## 常用日期函数
DATE(datetime) 取日期；DATE_ADD(date,INTERVAL 1 DAY) 加一天；DATEDIFF(后,前) 返回日期天数差；TIMESTAMPDIFF(SECOND,前,后) 看更细时间差。DATE_FORMAT(date,'%Y-%m') 可做月份标签，展示字符串不等于日期类型。
## 字符串与转换
CONCAT 拼接文本，SUBSTRING 从 1 开始取片段，TRIM 去首尾空格，LOWER 转小写。CAST('123' AS UNSIGNED) 转整数，转换失败或截断可能受 SQL 模式影响，别用它掩盖脏数据。
## 钱和小数
DECIMAL 是定点小数，适合金额；FLOAT/DOUBLE 是近似浮点。ROUND 用于最终展示，过早四舍五入会累积误差。整数编号不应该拿来求平均；DATE、DATETIME 与带时区解释也要区分。

## 可运行例子

```sql
SELECT DATE('2026-01-31 13:20:00') AS dt,
  DATE_ADD('2026-01-31',INTERVAL 1 DAY) AS next_day,
  DATEDIFF('2026-02-02','2026-01-31') AS day_gap,
  DATE_FORMAT('2026-01-31','%Y-%m') AS month;
SELECT CONCAT('user-',CAST(7 AS CHAR)) AS label,
  ROUND(100.0/3,2) AS amount;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

DATEDIFF(后日期, 前日期) 的常见含义是？

1. 相差的天数
2. 相差的秒数
3. 两日期字符串拼接

<details><summary>答案与解释</summary>

答案：1。需要秒级差值时用 TIMESTAMPDIFF。

</details>
