from _lecture_data import *

from scipy.stats import poisson, expon, norm
print("每分钟平均 3 次，零次概率：", poisson.pmf(0, 3))
print("等待超过 1 分钟：", expon.sf(1, scale=1/3))
print("标准正态落在 ±1.96：", norm.cdf(1.96)-norm.cdf(-1.96))
