# sql-04 · NULL：IS NULL、COALESCE 与三值逻辑

## 未知参与比较仍可能未知
NULL = NULL 不返回 TRUE，NULL <> 1 也不是 TRUE。WHERE 只保留 TRUE，因此查询缺失值用 IS NULL，非缺失用 IS NOT NULL，不能用 = NULL。
## 给展示结果兜底
COALESCE(city, '未知') 返回从左到右第一个非空参数。它不修改原表，只替换当前结果的展示。NULLIF(a,b) 在二者相等时返回 NULL，常用 NULLIF(分母,0) 防止把除零当正常比例。
## 三个特别坑
COUNT(列) 不数空值，COUNT(*) 数行。NOT IN 的候选集合如果含 NULL，可能意外没有结果；需要时使用 NOT EXISTS。空字符串 '' 与 NULL 是不同概念。

## 可运行例子

```sql
SELECT user_id,
   COALESCE(city,'未知') AS city_label
FROM users;
SELECT 3.0 / NULLIF(0,0) AS safe_ratio;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

筛选缺失城市应写？

1. city = NULL
2. city = 'NULL'
3. city IS NULL

<details><summary>答案与解释</summary>

答案：3。NULL 是特殊空值标记，字符串 NULL 只是四个字母。

</details>
