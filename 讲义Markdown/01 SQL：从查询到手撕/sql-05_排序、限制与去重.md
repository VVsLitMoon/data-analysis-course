# sql-05 · 排序、限制与去重

## 行没有默认顺序
ORDER BY amount DESC 表示金额从大到小，ASC 是从小到大。金额并列时加 order_id，排序才稳定。LIMIT 3 返回排序后最多三行，并不是自动找前三名。
## DISTINCT 对整组列去重
SELECT DISTINCT user_id 得到不同用户。SELECT DISTINCT user_id, category 得到不同的“用户—品类”组合，同一个用户仍能出现多次。
## LIMIT 与排名的区别
LIMIT 3 只要三行；“前三种金额且保留并列”需要后面的 DENSE_RANK。数据很大时 OFFSET 分页可能慢，面试进阶可了解按索引键继续翻页。

## 可运行例子

```sql
SELECT order_id,
   amount
FROM orders
WHERE status='paid'
ORDER BY amount DESC,
   order_id
LIMIT 3;
SELECT DISTINCT user_id,
   category
FROM orders
ORDER BY user_id,
   category;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

改成最便宜的三笔 paid 订单。

提示：DESC 改成 ASC。

## 自测

DISTINCT user_id, category 对什么去重？

1. 只对 category
2. 整对值
3. 只对 user_id

<details><summary>答案与解释</summary>

答案：2。SELECT 中的全部选定列共同决定重复。

</details>
