from _lecture_data import *

from scipy.stats import ttest_ind, ttest_rel
a = [10, 12, 9, 13, 11, 14]
b = [12, 15, 10, 16, 13, 18]
print("独立样本 Welch：", ttest_ind(a, b, equal_var=False))
print("若确实是同一人前后配对：", ttest_rel(a, b))
