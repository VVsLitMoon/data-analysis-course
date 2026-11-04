from _lecture_data import *

import numpy as np
rng = np.random.default_rng(42)
x = np.array([10,12,9,13,11,14,8,12])
boot = rng.choice(x, size=(2000,len(x)), replace=True).mean(axis=1)
print("Bootstrap 均值区间：", np.quantile(boot,[0.025,0.975]))
