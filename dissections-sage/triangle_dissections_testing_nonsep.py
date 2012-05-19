from triangle_dissections import *

import copy
import sage.all
import sys

from spherical import spherical_iterator

b = spherical_iterator(4, 22)

smallest_generating_bitrade = {}

while True:
    T1, T2 = b.next()

    for r, c in cross(range(T1.nrows()), range(T1.ncols())):
        if T1[r, c] < 0: continue

        try:
            t = TriangleDissection(T1, T2, r, c, only_separated_solutions = False)
        except ValueError:
            continue # there was no (separated?) solution

        print 'T1 ='
        print T1
        print 'T2 ='
        print T2
        print '|T1| =', T1.nr_filled_cells()
        print

        T1_size = T1.nr_filled_cells()

        if len(t.six_way_points) > 0:
            csig = t.canonical_signature()

            if csig in smallest_generating_bitrade:
                assert smallest_generating_bitrade[csig] <= T1_size
            else:
                smallest_generating_bitrade[csig] = T1_size

            print 'T1_size =', T1_size, '|smallest_generating_bitrade| =', len(smallest_generating_bitrade)

            print
            print 'after doing dissection code:'
            print 't.T1 ='
            print t.T1
            print 't.T2 ='
            print t.T2
            print '|t.T1| =', t.T1.nr_filled_cells()

            # assert False
