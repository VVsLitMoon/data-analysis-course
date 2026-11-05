# python-05 · DataFrame：在 Python 中看一张表

## 两个对象先分清
Pandas 的 DataFrame 是二维表，Series 是一列带索引的数据。每次运行，讲义已准备 users、orders、logins、events、assignments、calendar 六张 DataFrame，与 SQL 用的是同一组数据。
## 先检查再分析
head() 看前几行，shape 看行列数量，columns 看列名，dtypes 看数据类型。info() 会直接打印摘要；describe() 描述数值分布，但不能替代业务理解。
## 与 SQL 对照
orders['amount'] 是一列；orders[['order_id','amount']] 是两列表。方括号里是列名列表；少一层括号时含义不同。示例日期最初是字符串，后面再转成日期。

## 可运行例子

```python
print(orders.head(3))
print("行列数：", orders.shape)
print(orders.dtypes)
print(orders[["order_id", "amount"]].head())
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

orders[['order_id','amount']] 返回？

1. 两行
2. 包含两列的表
3. 一个数字

<details><summary>答案与解释</summary>

答案：2。双层括号的内层是列名列表。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "   order_id  user_id             order_at  amount status category\n0       101        1  2026-01-01 10:00:00     100   paid        A\n1       102        1  2026-01-02 10:00:00      50   paid        B\n2       103        1  2026-01-05 10:00:00      50   paid        A\n行列数： (16, 6)\norder_id     int64\nuser_id      int64\norder_at    object\namount       int64\nstatus      object\ncategory    object\ndtype: object\n   order_id  amount\n0       101     100\n1       102      50\n2       103      50\n3       104     200\n4       105       0\n"
}
```
