from _lecture_data import *

paid = orders.loc[(orders["status"] == "paid") & (orders["amount"] >= 100)].copy()
paid["amount_after_10pct_discount"] = paid["amount"] * 0.9
print(paid.sort_values(["amount", "order_id"], ascending=[False, True]))
