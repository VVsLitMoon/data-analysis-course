from _lecture_data import *

from scipy.stats import binom, hypergeom
print("10 次、p=0.2，恰好 2 次：", binom.pmf(2, 10, 0.2))
print("至少 2 次：", binom.sf(1, 10, 0.2))
print("10 个中 3 个红球，抽 2 个都红：", hypergeom.pmf(2, 10, 3, 2))
