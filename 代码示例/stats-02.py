from _lecture_data import *

import numpy as np
x = np.array([10, 10, 20, 20, 200])
print("均值/中位数：", x.mean(), np.median(x))
print("总体方差：", x.var(ddof=0))
print("样本标准差：", x.std(ddof=1))
print("25/75 分位数：", np.quantile(x, [0.25, 0.75]))
