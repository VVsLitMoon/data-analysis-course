from _lecture_data import *

from scipy.stats import chisquare
print("5500/4500 对计划 5000/5000 的 SRM p：", chisquare([5500,4500], f_exp=[5000,5000]).pvalue)
