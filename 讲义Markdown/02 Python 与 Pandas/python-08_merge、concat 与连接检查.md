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

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "    user_id  order_id     _merge\n0         1     101.0       both\n1         1     102.0       both\n2         1     103.0       both\n3         1     104.0       both\n4         1     105.0       both\n5         2     106.0       both\n6         2     107.0       both\n7         2     114.0       both\n8         3     108.0       both\n9         3     109.0       both\n10        4     110.0       both\n11        4     111.0       both\n12        5       NaN  left_only\n13        6       NaN  left_only\n14        7     112.0       both\n15        7     113.0       both\n合并后金额： 1450.0\ncategory    A    B    C\nuser_id                \n1         150   50  200\n2         180   20    0\n3         100  100    0\n4           0  200   50\n7           0    0  400\n     users  conversion  gmv_per_user\narm                                 \nA        3    0.666667         200.0\nB        3    0.666667         150.0\n"
}
```
