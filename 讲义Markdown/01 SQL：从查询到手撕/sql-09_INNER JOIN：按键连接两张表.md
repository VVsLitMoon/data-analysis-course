# sql-09 · INNER JOIN：按键连接两张表

## 为什么需要连接
订单里没有渠道，用户表里有渠道。要按渠道统计支付金额，需要把每笔订单对应的用户信息补上。JOIN 是按条件寻找匹配行，不是按行号拼接。
## 逐行理解
users u 中 u 是表的短名字；orders o 同理。ON u.user_id=o.user_id 指定相同用户才匹配。u.channel 表示来自用户表的 channel。INNER JOIN 只保留双方都能匹配的行。
## 连接后的一行是什么
在用户主键唯一的前提下，连接后每一行仍是一笔订单。用户会因为多笔订单重复出现。因此连接后求用户数通常需要 COUNT(DISTINCT u.user_id)。

## 可运行例子

```sql
SELECT u.channel,
   COUNT(*) AS paid_orders,
   SUM(o.amount) AS gmv
FROM users u
JOIN orders o ON u.user_id=o.user_id
WHERE o.status='paid'
GROUP BY u.channel;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

改为按城市统计。

提示：SELECT 和 GROUP BY 都改成 u.city。

## 自测

JOIN 的 ON 条件的作用是？

1. 规定哪些行互相匹配
2. 规定输出排序
3. 自动删除重复订单

<details><summary>答案与解释</summary>

答案：1。它表达关联关系。

</details>
