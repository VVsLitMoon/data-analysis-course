# python-06 · 筛选、排序与新列

## 布尔条件像一列开关
orders['status']=='paid' 得到每行 True/False，把它放进 orders[...] 就只保留 True 的行。多个条件用 &、|、~，每个比较都加括号，不用 Python 的 and/or 连接整列。
## loc 与 iloc
.loc[行条件,列名] 按标签选取；.iloc[0:3,0:2] 按位置选取，右端不包含。sort_values 指定排序列和升降序。
## 安全添加新列
筛选后准备修改，先 .copy()。新列可以用整列运算生成，不必逐行循环。避免 chained assignment：不要连续两次方括号后直接赋值，使用 .loc 或明确副本。

## 可运行例子

```python
paid = orders.loc[(orders["status"] == "paid") & (orders["amount"] >= 100)].copy()
paid["amount_after_10pct_discount"] = paid["amount"] * 0.9
print(paid.sort_values(["amount", "order_id"], ascending=[False, True]))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

改成金额在 50 到 100 之间。

提示：两个金额比较都加括号后用 & 连接。

## 自测

Pandas 两个整列条件通常用？

1. &，每个比较加括号
2. and 且不用括号
3. 英文逗号

<details><summary>答案与解释</summary>

答案：1。整列逐元素逻辑与使用 &。

</details>
