from _lecture_data import *

amounts = [100, 50, 80]
channels = {"organic": 100, "paid": 80}
print(amounts[0], amounts[-1], amounts[:2])
print(sum(amounts), len(amounts))
print(channels.get("new_channel", 0))
