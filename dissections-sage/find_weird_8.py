from fractions import Fraction
import sys

vertex_lists = {}

for original_line in sys.stdin.readlines():
    line = map(Fraction, original_line.rstrip().split(' '))

    assert len(line) % (3*4) == 0

    points = [tuple(line[4*i:(4*(i+1))]) for i in range(len(line)/4)]
    points.sort()
    points = tuple(points)

    if points not in vertex_lists:
        vertex_lists[points] = []

    vertex_lists[points].append([original_line])

    if len(vertex_lists[points]) > 1:
        for l in vertex_lists[points]:
            print l
        sys.exit(0)

