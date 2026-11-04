from _lecture_data import *

import numpy as np
rng = np.random.default_rng(42)
for n in [10, 100, 1000]:
    means = rng.exponential(scale=10, size=(1000, n)).mean(axis=1)
    print(n, "均值的标准差：", round(means.std(ddof=1), 3), "理论近似：", round(10/np.sqrt(n), 3))
