from _lecture_data import *

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
