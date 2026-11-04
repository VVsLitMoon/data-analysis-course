from _lecture_data import *

import numpy as np
from scipy.stats import linregress, spearmanr
x = np.array([1,2,3,4,5])
y = np.array([3,5,6,9,11])
r = linregress(x,y)
print("斜率/截距：", r.slope, r.intercept)
print("R²：", r.rvalue**2)
print("Spearman：", spearmanr(x,y).statistic)
