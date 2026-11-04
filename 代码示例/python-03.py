from _lecture_data import *

amounts = [100, 50, 0, 80]
total = 0
for amount in amounts:
    if amount > 0:
        total += amount
        print("计入：", amount)
print("合计：", total)
