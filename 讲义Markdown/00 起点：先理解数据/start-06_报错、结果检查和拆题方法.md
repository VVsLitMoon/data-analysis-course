# start-06 · 报错、结果检查和拆题方法

## 先读错误，不要立刻重写
SQL 报 Unknown column，通常是列名拼错或别名作用阶段不对；syntax error 常见原因是漏逗号、括号或用了中文标点。Python NameError 是变量还不存在，IndentationError 是缩进不一致。先找错误位置，再一次改一个问题。
## 没报错也可能做错
结果能运行只是第一关。检查行数、主键是否唯一、金额总和有没有翻倍、比例是否在合理范围、没有订单的人是否被保留。用一个人和两三行手算，最容易发现口径错误。
## 通用四步
第一，写出输出一行代表什么。第二，写清分子分母及过滤条件。第三，拆成中间表逐步运行。第四，加入空值、并列、重复、无订单等边界情况。不要靠不停加 DISTINCT 掩盖连接错误。

## 可运行例子

```sql
SELECT COUNT(*) AS all_rows,
   COUNT(DISTINCT user_id) AS users_with_orders
FROM orders;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

SQL 不报错能证明答案正确吗？

1. 不能，还要检查口径和边界
2. 能
3. 只要加 DISTINCT 就能

<details><summary>答案与解释</summary>

答案：1。语法正确与业务正确是两回事。

</details>
