from _lecture_data import *

import numpy as np
from scipy.stats import norm, chi2_contingency, fisher_exact
n_a = n_b = 1000
x_a, x_b = 100, 125
pool = (x_a+x_b)/(n_a+n_b)
se = np.sqrt(pool*(1-pool)*(1/n_a+1/n_b))
z = (x_b/n_b-x_a/n_a)/se
print("两比例双侧 p：", 2*norm.sf(abs(z)))
print("卡方：", chi2_contingency([[100,900],[125,875]], correction=False).pvalue)
print("小样本 Fisher：", fisher_exact([[1,9],[6,4]]).pvalue)
