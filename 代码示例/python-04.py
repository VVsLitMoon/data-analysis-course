from _lecture_data import *

def conversion_rate(buyers, visitors):
    if visitors == 0:
        return None
    return buyers / visitors

print(conversion_rate(12, 100))
print(conversion_rate(0, 0))
import math
print(math.sqrt(16))
