from fractions import Fraction
from sets import Set

lines = open('find_nonsep_sig_problem.out').readlines()
lines = [x.rstrip().split() for x in lines]

for x in lines:
    assert len(x) % 12 == 0
    assert len(x) %  4 == 0

for x in lines:
    vertices = list(set([' '.join(x[4*i:(4*i + 4)]) for i in range(len(x)/4)]))
    vertices.sort()

    print ' '.join(vertices)
