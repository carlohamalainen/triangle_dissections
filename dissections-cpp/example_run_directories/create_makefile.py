#!/usr/bin/env python

import sys

base_dir   = sys.argv[1]
N         = int(sys.argv[2])
nr_slices = int(sys.argv[3])

f = open('Makefile', 'w')

f.write('all: ')
for s in range(nr_slices):
    f.write('done_%d_%d ' % (s, nr_slices))
f.write('\n\n')

for s in range(nr_slices):
    f.write('binary_bitrades_%d_%d_%d:\n' % (N, s, nr_slices))
    f.write('\t%s/spherical_bitrade_generator/spherical_trades_binary -b -u %d %d/%d > binary_bitrades_%d_%d_%d\n\n' % (base_dir, N + 2, s, nr_slices, N, s, nr_slices))

    f.write('done_%d_%d: binary_bitrades_%d_%d_%d\n' % (s, nr_slices, N, s, nr_slices))
    f.write('\t./run_slice.sh %d %d %d\n\n' % (N, s, nr_slices))
