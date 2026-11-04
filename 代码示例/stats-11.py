from _lecture_data import *

from scipy.stats import binomtest
result = binomtest(k=65, n=100, p=0.5, alternative="two-sided")
print("100 次正面 65 次，H0:p=0.5，p 值：", result.pvalue)
