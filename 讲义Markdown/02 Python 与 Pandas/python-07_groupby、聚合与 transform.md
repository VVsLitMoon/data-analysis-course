# python-07 · groupby、聚合与 transform

## 从明细到用户摘要
groupby('user_id') 按用户分组，agg 可以同时求订单数、金额总和、均值。size 计行数，count 计非空值，nunique 计不同值；与 SQL 计数的细节对照理解。
## 想保留每行怎么办
transform('sum') 把每组汇总值广播回每行，相当于 SQL 的 SUM OVER(PARTITION BY)。agg 会缩成组级结果，transform 保留原来长度。
## 最新行与组内排名
先按用户、时间、订单号排序，再按 user_id 去重保留最后一条，可以取最新订单；并列时间由订单号打破。groupby()['amount'].rank(method='dense',ascending=False) 对应金额稠密排名；method='min' 类似 RANK，method='first' 按现有行顺序打破并列，因此使用前需排序。
## 两个默认值
groupby 常默认把空分组键排除，需要时用 dropna=False。as_index=False 让分组列保留为普通列，初学更容易继续连接。

## 可运行例子

```python
paid = orders.loc[orders["status"] == "paid"].copy()
summary = paid.groupby("user_id", as_index=False).agg(paid_orders=("order_id", "size"), gmv=("amount", "sum"))
paid["user_gmv"] = paid.groupby("user_id")["amount"].transform("sum")
paid["amount_rank"] = paid.groupby("user_id")["amount"].rank(method="dense", ascending=False)
latest = paid.sort_values(["user_id", "order_at", "order_id"]).drop_duplicates("user_id", keep="last")
print(summary)
print(paid[["order_id", "user_id", "amount", "user_gmv", "amount_rank"]].head())
print("每位用户最新订单：")
print(latest[["user_id", "order_id", "order_at"]])
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

transform 与 agg 的主要区别是？

1. transform 只能计数
2. agg 一定保留每行
3. transform 通常保留原行数

<details><summary>答案与解释</summary>

答案：3。它把组内结果对应回明细行。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "   user_id  paid_orders  gmv\n0        1            5  400\n1        2            3  200\n2        3            2  200\n3        4            2  250\n4        7            2  400\n   order_id  user_id  amount  user_gmv  amount_rank\n0       101        1     100       400          2.0\n1       102        1      50       400          3.0\n2       103        1      50       400          3.0\n3       104        1     200       400          1.0\n4       105        1       0       400          4.0\n每位用户最新订单：\n    user_id  order_id             order_at\n4         1       105  2026-02-01 10:00:00\n13        2       114  2026-03-01 10:00:00\n8         3       109  2026-01-03 10:00:00\n10        4       111  2026-01-03 12:00:00\n12        7       113  2026-02-02 10:00:00\n"
}
```
