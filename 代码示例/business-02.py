from _lecture_data import *

a0,b0 = 1000,100
a1,b1 = 900,110
delta_a = (a1-a0)*b0
delta_b = a1*(b1-b0)
print("A 贡献：",delta_a,"B 贡献：",delta_b)
print("合计：",delta_a+delta_b,"实际变化：",a1*b1-a0*b0)
