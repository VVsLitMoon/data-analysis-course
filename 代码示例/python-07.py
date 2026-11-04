from _lecture_data import *

paid = orders.loc[orders["status"] == "paid"].copy()
summary = paid.groupby("user_id", as_index=False).agg(paid_orders=("order_id", "size"), gmv=("amount", "sum"))
paid["user_gmv"] = paid.groupby("user_id")["amount"].transform("sum")
paid["amount_rank"] = paid.groupby("user_id")["amount"].rank(method="dense", ascending=False)
latest = paid.sort_values(["user_id", "order_at", "order_id"]).drop_duplicates("user_id", keep="last")
print(summary)
print(paid[["order_id", "user_id", "amount", "user_gmv", "amount_rank"]].head())
print("每位用户最新订单：")
print(latest[["user_id", "order_id", "order_at"]])
