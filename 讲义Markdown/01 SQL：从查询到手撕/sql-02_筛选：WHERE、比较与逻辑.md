# sql-02 · 筛选：WHERE、比较与逻辑

## 逐行决定保留谁
WHERE 对每行判断条件，只保留结果为 TRUE 的行。= 等于，<> 不等于，> 大于，>= 大于等于。SQL 比较相等是一个等号，Python 是两个。
## 同时与任选
AND 要求两个条件都成立，OR 只需至少一个，NOT 取否定。AND 通常比 OR 先计算，混用时直接加括号，避免错误理解。
## 例子的业务含义
只选 paid 且金额至少 100 的订单。先筛状态，再筛金额。若题目要“上海或者北京的自然流量用户”，应写 (city='上海' OR city='北京') AND channel='organic'。

## 可运行例子

```sql
SELECT order_id,
   user_id,
   amount
FROM orders
WHERE status = 'paid' AND amount >= 100;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

找 paid 且金额小于 100 的订单。

提示：把 >= 改为 <。

## 自测

AND 的意思是？

1. 删除符合条件的行
2. 两个条件都成立
3. 任意一个成立即可

<details><summary>答案与解释</summary>

答案：2。WHERE 只筛选结果，不会删除源表。

</details>
