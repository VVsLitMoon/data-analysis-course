from _lecture_data import *

base = 0.01
sensitivity = 0.90
false_positive = 0.05
true_alert = base * sensitivity
false_alert = (1 - base) * false_positive
print("告警为真概率：", true_alert / (true_alert + false_alert))
