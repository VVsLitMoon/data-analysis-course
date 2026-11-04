# sql-25 · 中位数、分位数与分布

## 中位数怎么手算
先排序，奇数个取中间一个，偶数个取中间两个的平均。中位数受极端大值影响较小，但不能代替总额；分位数描述低于某个值的比例，不同软件的插值定义可能不同。
## MySQL 8.0 的实现思路
MySQL 8.0 没有通用内置 MEDIAN 聚合。用 ROW_NUMBER 排序，同时 COUNT(*) OVER() 得总数，挑出 FLOOR((n+1)/2) 和 FLOOR((n+2)/2) 两个位置，最后 AVG。
## 进阶认识
NTILE(4) 尽量按行数分四桶，相同金额可能拆桶；PERCENT_RANK 与 CUME_DIST 的并列规则不同。做金额分层先约定边界，不能把所有“分位”函数当成同义词。

## 可运行例子

```sql
WITH r AS (
  SELECT amount,ROW_NUMBER() OVER(
    ORDER BY amount,order_id) AS rn,COUNT(*) OVER() AS n
  FROM orders
  WHERE status='paid')
SELECT AVG(amount) AS median_amount
FROM r
WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2));
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

偶数个数的中位数通常取？

1. 最大的数
2. 最小的数
3. 中间两数平均

<details><summary>答案与解释</summary>

答案：3。先排序，再取中间两个。

</details>
