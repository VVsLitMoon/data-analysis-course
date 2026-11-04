from _lecture_data import *

treat_before,treat_after = 100,130
control_before,control_after = 80,95
did = (treat_after-treat_before)-(control_after-control_before)
print("DID 估计：",did)
