from _lecture_data import *

import numpy as np
from scipy.stats import t
x = np.array([10, 12, 9, 13, 11, 14, 8, 12])
n = len(x)
se = x.std(ddof=1) / np.sqrt(n)
margin = t.ppf(0.975, df=n-1) * se
print("均值：", x.mean(), "95% 区间：", (x.mean()-margin, x.mean()+margin))
