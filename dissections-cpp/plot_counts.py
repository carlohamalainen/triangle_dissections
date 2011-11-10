lines = [x.split() for x in open('signature_counts_upto_24.txt').readlines()]
lines = [(int(x[0]), int(x[1])) for x in lines]
x = [line[0] for line in lines]
y = [line[1] for line in lines]

import pylab as plt

plt.clf(); plt.cla();

plt.plot(x, y, 'o')
plt.title('Number of separated triangle dissections')
plt.xlabel('n')
plt.ylabel('nr dissections (log scale)')
plt.yscale('log')

plt.savefig('signature_counts.png')
