from _lecture_data import *

import numpy as np
from scipy.stats import false_discovery_control
pvalues = np.array([0.001,0.01,0.03,0.2,0.6])
print("Bonferroni 调整：", np.minimum(pvalues*len(pvalues),1))
print("BH 调整：", false_discovery_control(pvalues,method="bh"))
