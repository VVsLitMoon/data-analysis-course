from _lecture_data import *

buyers = [5, 10]
visitors = [10, 100]
rates = [buyers[i] / visitors[i] for i in range(2)]
print("错误的等权平均：", sum(rates) / 2)
print("整体转化率：", sum(buyers) / sum(visitors))
