from _lecture_data import *

import numpy as np
from scipy.stats import norm
a,na = 1000,10000
b,nb = 1200,10000
pa,pb = a/na,b/nb
diff = pb-pa
se = np.sqrt(pa*(1-pa)/na + pb*(1-pb)/nb)
print("差：", diff, "相对提升：", diff/pa)
print("大样本近似 95% 区间：", (diff-1.96*se, diff+1.96*se))
