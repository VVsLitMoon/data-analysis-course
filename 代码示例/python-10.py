from _lecture_data import *

import numpy as np
x = np.array([1, 2, 3])
print("数组乘法：", x * 2)
rng = np.random.default_rng(42)
print("抽 5 个 0 到 9 的整数：", rng.integers(0, 10, size=5))
print("均值：", x.mean())
print("分层：", np.where(x >= 2, "高", "低"))
numerator = pd.Series([10, 0])
denominator = pd.Series([100, 0])
print("安全比率：", numerator.div(denominator.where(denominator.ne(0))))
