from _lecture_data import *

import math
from scipy.stats import norm
p = 0.10
delta = 0.01
alpha = 0.05
power = 0.80
n = math.ceil(2*p*(1-p)*(norm.ppf(1-alpha/2)+norm.ppf(power))**2/delta**2)
print("近似每组样本：", n, "总样本：", 2*n)
