#!/usr/bin/env python

import pylab as plt

all_info = {}

for n in range(4, 24 + 1):
    if n == 5: continue

    lines = open('pp_dissection_element_sizes_%d.out' % n).readlines()
    lines = [x.split(' ') for x in lines]

    sizes  = [int(x[0]) for x in lines]
    counts = [int(x[1]) for x in lines]

    plt.clf(); plt.cla();

    plt.plot(sizes, counts, 'x', color='black')
    plt.title('Element sizes across n = %d.' % n)
    plt.xlabel('element size')
    plt.ylabel('nr')
    plt.yscale('log')

    plt.savefig('pp_element_sizes_%d.png' % (n,))
    plt.savefig('pp_element_sizes_%d.pdf' % (n,))

    for (size, count) in zip(sizes, counts):
        if size in all_info:
            all_info[size] += count
        else:
            all_info[size] = count

all_sizes = sorted(all_info.keys())
all_counts = [all_info[s] for s in all_sizes]

plt.clf(); plt.cla();

plt.plot(sizes, counts, 'x', color='black')
plt.title('Element sizes across all n.')
plt.xlabel('element size')
plt.ylabel('nr')
plt.yscale('log')

plt.savefig('pp_element_sizes_all.png')
plt.savefig('pp_element_sizes_all.pdf')


