from fractions import Fraction
from math import ceil

for n in range(4, 24 + 1):
    if n == 5: continue

    lines = [x.split() for x in open('pp_ratio_spectrum_%d.out' % n).readlines()]
    lines = [(float(Fraction(x[0])), float(Fraction(x[1]))) for x in lines]

    x = [line[0] for line in lines]
    y = [line[1] for line in lines]

    import pylab as plt

    plt.clf(); plt.cla();

    plt.plot(x, y, 'o')
    plt.title('Ratio of largest to smallest triangle, n = %d' % n)
    plt.xlabel('ratio')
    plt.ylabel('frequency')
    plt.xlim(0, ceil(1.2*max(x)))
    plt.ylim(0, ceil(1.2*max(y)))
    plt.savefig('pp_ratio_spectrum_%d.png' % n)
