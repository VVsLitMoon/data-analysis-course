# python-08 · merge、concat 与连接检查

## 和 SQL JOIN 一样先检查键
merge(...,on='user_id',how='left') 左连接。validate='one_to_many' 表示期望左侧键唯一、右侧可重复；不满足时主动报错，有助于防止金额翻倍。
## 指标校验
连接前后比较订单数、总额和未匹配比例。indicator=True 增加匹配来源列。Pandas 缺失键之间的匹配行为与普通 SQL NULL 连接不同，遇到空键时要明确处理。
## 拼接与透视
concat 默认沿行方向拼接，列名不同会产生缺失。pivot 把唯一组合转为宽表，pivot_table 可先聚合；melt 把宽表拉成长表。行列结构是展示方式，不应偷偷改变指标定义。
## 实验按用户分析
先把 paid 订单汇成一人一行金额，再以 assignments 的入组用户为左表连接，没消费的金额填 0；is_buyer 在有 paid 订单时为 1（金额为零的支付订单也算买家）。最后按 arm 算用户数、购买率和人均金额，避免把订单当独立用户。

## 可运行例子

```python
paid = orders.loc[orders["status"] == "paid"]
joined = users.merge(paid, on="user_id", how="left", validate="one_to_many", indicator=True)
print(joined[["user_id", "order_id", "_merge"]])
print("合并后金额：", joined["amount"].sum())
print(paid.pivot_table(index="user_id", columns="category", values="amount", aggfunc="sum", fill_value=0))
spend = paid.groupby("user_id", as_index=False).agg(gmv=("amount", "sum"), paid_orders=("order_id", "size"))
experiment = assignments.merge(spend, on="user_id", how="left", validate="one_to_one")
experiment[["gmv", "paid_orders"]] = experiment[["gmv", "paid_orders"]].fillna(0)
experiment["is_buyer"] = (experiment["paid_orders"] > 0).astype(int)
print(experiment.groupby("arm").agg(users=("user_id", "size"), conversion=("is_buyer", "mean"), gmv_per_user=("gmv", "mean")))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

validate 参数为什么有用？

1. 只是让代码更快
2. 核对键的唯一性，及时发现意外关系
3. 自动保证所有业务正确

<details><summary>答案与解释</summary>

答案：2。它能防止本应一对多的连接悄悄变成多对多。

</details>
