from _lecture_data import *

print(orders.head(3))
print("行列数：", orders.shape)
print(orders.dtypes)
print(orders[["order_id", "amount"]].head())
