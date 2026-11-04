from _lecture_data import *

paid = orders.loc[orders["status"] == "paid"].copy()
paid["dt"] = pd.to_datetime(paid["order_at"]).dt.normalize()
daily = paid.groupby("dt")["amount"].sum()
days = pd.date_range("2026-01-01", "2026-01-10")
daily = daily.reindex(days, fill_value=0)
print(pd.DataFrame({"gmv": daily, "rolling7": daily.rolling(7, min_periods=1).sum()}))
print("城市缺失数：", users["city"].isna().sum())
