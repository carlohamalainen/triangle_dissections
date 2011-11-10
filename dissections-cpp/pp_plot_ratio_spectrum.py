import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
from fractions import Fraction

counts_x = []
counts_y = []

for line in sys.stdin.readlines():
    counts_x.append(float(Fraction(line.split(' ')[0])))
    counts_y.append(float(Fraction(line.split(' ')[1])))

print counts_x
print counts_y

plt.plot(counts_x, counts_y)
plt.savefig('pp_ratios_test.png')
