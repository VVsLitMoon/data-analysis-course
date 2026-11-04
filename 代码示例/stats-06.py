from _lecture_data import *

import numpy as np
x = np.array([0, 100])
p = np.array([0.9, 0.1])
mean = (x * p).sum()
variance = ((x - mean) ** 2 * p).sum()
print("期望：", mean, "方差：", variance)
