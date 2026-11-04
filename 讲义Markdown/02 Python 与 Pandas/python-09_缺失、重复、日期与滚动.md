# python-09 · 缺失、重复、日期与滚动

## 清洗要保留解释
isna() 找缺失，fillna() 补值，dropna() 删缺失。drop_duplicates(subset=[...]) 依据指定键去重，但先确认哪一行该保留，例如按更新时间排序保留最后一条。不能把真实重复购买删掉。
## 日期转成可计算的类型
pd.to_datetime 把字符串变日期时间；errors='coerce' 会把无效字符串变 NaT，随后必须检查数量。.dt.date 取日，.dt.to_period('M') 取月。统一时区后再比较。
## 排序后才移动
groupby().shift() 对应 LAG。rolling(7) 是七行；按时间索引的 rolling('7D') 是时间窗，端点由 closed 等参数控制。先补日历更容易解释每天的滚动金额。

## 可运行例子

```python
paid = orders.loc[orders["status"] == "paid"].copy()
paid["dt"] = pd.to_datetime(paid["order_at"]).dt.normalize()
daily = paid.groupby("dt")["amount"].sum()
days = pd.date_range("2026-01-01", "2026-01-10")
daily = daily.reindex(days, fill_value=0)
print(pd.DataFrame({"gmv": daily, "rolling7": daily.rolling(7, min_periods=1).sum()}))
print("城市缺失数：", users["city"].isna().sum())
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

rolling(7) 默认是指？

1. 7 行
2. 无条件代表 7 天
3. 7 个用户

<details><summary>答案与解释</summary>

答案：1。只有连续一日一行时才恰好对应七天。

</details>
