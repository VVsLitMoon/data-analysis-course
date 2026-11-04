from _lecture_data import *

import numpy as np
rng = np.random.default_rng(42)
for n in [100, 1000, 10000]:
    sample = rng.binomial(1, 0.12, size=n)
    print(n, "人的样本购买率：", sample.mean())
