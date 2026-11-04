# sql-13 · CTE 与 UNION：把复杂查询拆开

## 给中间结果起名字
WITH paid AS (...) 定义只在本条语句里可用的公共表表达式，简称 CTE。它不是永久表。多个 CTE 用逗号分隔，后面的可以引用前面的。
## 按问题的层次拆
先得到用户金额，再筛高价值用户，最后汇总渠道。每一层写出粒度，比一口气嵌套很多括号更易检查。CTE 不保证一定物化或更快，优化器会选择。
## 上下拼接与左右连接
UNION ALL 上下拼接并保留重复；UNION 会去重。两边列数相同，对应类型兼容，按列的位置对应，不是按列名。JOIN 是横向补列，不能混淆。

## 可运行例子

```sql
WITH paid AS (
  SELECT *
  FROM orders
  WHERE status='paid'),
   spend AS (
  SELECT user_id,SUM(amount) AS gmv
  FROM paid
  GROUP BY user_id)
SELECT *
FROM spend
WHERE gmv>=200
ORDER BY user_id;
SELECT 'A' AS label
UNION ALL
SELECT 'A';
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

把 UNION ALL 改成 UNION，观察变化。

提示：两行相同文字会变成一行。

## 自测

UNION ALL 的特点是？

1. 横向按键匹配
2. 一定去重
3. 上下拼接并保留重复

<details><summary>答案与解释</summary>

答案：3。ALL 表示保留所有输入行。

</details>
