'''
Copyright 2010 Carlo Hamalainen <carlo.hamalainen@gmail.com>. All
rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer
      in the documentation and/or other materials provided with the
      distribution.

THIS SOFTWARE IS PROVIDED BY Carlo Hamalainen ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL Carlo Hamalainen OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation
are those of the authors and should not be interpreted as representing
official policies, either expressed or implied, of Carlo Hamalainen.
'''

import sage.all
from sage.combinat.matrices.latin import *
import os
import sys
from sage.misc.misc import tmp_filename

def _tau1(T1, T2, cells_map):
    # The cells_map has both directions, i.e. integer to
    # cell and cell to integer, so the size of T1 is
    # just half of len(cells_map).
    x = (int(len(cells_map)/2) + 1) * [-1]

    for r in range(T1.nrows()):
        for c in range(T1.ncols()):
            e = T1[r, c]

            if e < 0: continue

            (r2, c2, e2) = beta3( (r,c,e), T1, T2)
            (r3, c3, e3) = beta2( (r2,c2,e2), T2, T1)

            x[ cells_map[(r,c)] ] = cells_map[ (r3,c3) ]

    x.pop(0) # remove the head of the list since we
             # have permutations on 1..(something).

    return Permutation(x)

def _tau2(T1, T2, cells_map):
    # The cells_map has both directions, i.e. integer to
    # cell and cell to integer, so the size of T1 is
    # just half of len(cells_map).
    x = (int(len(cells_map)/2) + 1) * [-1]

    for r in range(T1.nrows()):
        for c in range(T1.ncols()):
            e = T1[r, c]

            if e < 0: continue

            (r2, c2, e2) = beta1( (r,c,e), T1, T2)
            (r3, c3, e3) = beta3( (r2,c2,e2), T2, T1)

            x[ cells_map[(r,c)] ] = cells_map[ (r3,c3) ]

    x.pop(0) # remove the head of the list since we
             # have permutations on 1..(something).

    return Permutation(x)

def _tau3(T1, T2, cells_map):
    # The cells_map has both directions, i.e. integer to
    # cell and cell to integer, so the size of T1 is
    # just half of len(cells_map).
    x = (int(len(cells_map)/2) + 1) * [-1]

    for r in range(T1.nrows()):
        for c in range(T1.ncols()):
            e = T1[r, c]

            if e < 0: continue

            (r2, c2, e2) = beta2( (r,c,e), T1, T2)
            (r3, c3, e3) = beta1( (r2,c2,e2), T2, T1)

            x[ cells_map[(r,c)] ] = cells_map[ (r3,c3) ]

    x.pop(0) # remove the head of the list since we
             # have permutations on 1..(something).

    return Permutation(x)


class Tau:
    def __init__(self, T1, cells_map, tau, i):
        self.i = i # i in [1,2,3]
        self.T1 = T1
        self.cells_map = cells_map
        self.tau = tau
        self.tau_inverse = tau.inverse()

    def _image_of_permutation(self, x, use_tau):
        if isinstance(x, Integer):
            return self._image_of_permutation(self.cells_map[x], use_tau)

        if isinstance(x, tuple):
            r = x[0]
            c = x[1]
            pt = self.cells_map[(r, c)]

            pt_im = use_tau[pt - 1]

            r_im, c_im = self.cells_map[pt_im]

            if len(x) == 2: return (r_im, c_im)
            return (r_im, c_im, self.T1[r_im, c_im])

        raise NotImplemented

    def image(self, x):
        return self._image_of_permutation(x, self.tau)

    def inverse(self, x):
        return self._image_of_permutation(x, self.tau_inverse)




b_for_testing = r"""4 2 4
8
0 0 0
0 1 1
1 1 0
1 0 2
2 0 3
3 0 1
3 1 3
2 1 2
8
0 0 1
0 1 0
1 0 0
2 0 2
3 0 3
3 1 1
2 1 3
1 1 2
"""

class Bitrade:
    """
    pair of partial latin squarres T1, T2

    permutations t1, t2, t3
    """

    def __init__(self):
        pass


def dump_to_tmpfile(s):
    """
    Utility function to dump a string to a temporary file.

    EXAMPLE:
        sage: from spherical import *
        sage: file_loc = dump_to_tmpfile("boo")
        sage: os.remove(file_loc)
    """

    file_loc = tmp_filename()
    f = open(file_loc,"w")
    f.write(s)
    f.close()
    return file_loc

def read_spherical_bitrade(f):
    """
    Read a spherical bitrade from the stream f, assuming input is
    given by the spherical_bitrades program (uses plantri).

    For example, the intercalate appears as follows:

        2 2 2
        4
        0 0 0
        0 1 1
        1 1 0
        1 0 1
        4
        0 0 1
        0 1 0
        1 0 0
        1 1 1

    This means: 2 row labels, 2 column labels, 2 symbol labels
    size of trade is 4
    {triples for T1}
    size of trade is 4
    {triples for T2}

    EXAMPLE:
        sage: from spherical import *
        sage: filename = dump_to_tmpfile(b_for_testing)
        sage: f = open(filename, "r")
        sage: T1, T2 = read_spherical_bitrade(f)
        sage: f.close()
        sage: os.remove(filename)
    """

    n = max(map(int, f.readline().split()))

    T1 = LatinSquare(n, n)
    T2 = LatinSquare(n, n)

    for r in range(n):
        for c in range(n):
            T1[r, c] = -1
            T2[r, c] = -1

    nr_entries = int(f.readline().split()[0])
    for _ in range(nr_entries):
        [r, c, e] = map(int, f.readline().split())
        T1[r, c] = e

    nr_entries = int(f.readline().split()[0])
    for _ in range(nr_entries):
        [r, c, e] = map(int, f.readline().split())
        T2[r, c] = e

    return (T1, T2)

def process_spherical_file(file_name):
    """
    Opens a file and reads all the bitrades (see read_spherical_bitrade
    for the format).

    EXAMPLE:
        sage: from spherical import *
        sage: bitrades = process_spherical_file("spherical_bitrades_8")
        sage: len(bitrades)
        2
        sage: bitrades[0][0]
        [ 0  1 -1 -1]
        [ 2  0 -1 -1]
        [ 3  2 -1 -1]
        [ 1  3 -1 -1]
    """

    f = open(file_name,'r')

    bitrades = []

    while True:
        try:
            (T1, T2) = read_spherical_bitrade(f)
        except ValueError:
            # We actually hit the end of file in f.
            break

        assert is_bitrade(T1, T2)

        #g = genus(T1, T2)
        #assert g == _sage_const_0

        bitrades.append((T1, T2))

    f.close()

    return bitrades

def some_spherical_bitrades():
    """
    I saved some spherical bitrades (output from spherical_bitrades) in
    the files b6, b8, etc, where bn has bitrades of size n-2.

    todo: this should really be an iterator to the data. We shouldn't
    have to read in the whole list of bitrades before processing.

    EXAMPLE:
        sage: from spherical import *
        sage: bitrades = some_spherical_bitrades()
        sage: bitrades[10][0]
        [ 0  1  2 -1 -1]
        [ 3 -1  0  4 -1]
        [ 1  2  4  3 -1]
        [-1 -1 -1 -1 -1]
        [-1 -1 -1 -1 -1]
    """

    b = []
    b += process_spherical_file("spherical_bitrades_4")
    b += process_spherical_file("spherical_bitrades_6")
    b += process_spherical_file("spherical_bitrades_7")
    b += process_spherical_file("spherical_bitrades_8")
    b += process_spherical_file("spherical_bitrades_9")
    b += process_spherical_file("spherical_bitrades_10")
    b += process_spherical_file("spherical_bitrades_11")
    b += process_spherical_file("spherical_bitrades_12")
    #b += process_spherical_file("spherical_bitrades_13")
    #b += process_spherical_file("spherical_bitrades_14")
    #b += process_spherical_file("spherical_bitrades_15")
    #b += process_spherical_file("spherical_bitrades_16")
    #b += process_spherical_file("spherical_bitrades_17")
    #b += process_spherical_file("spherical_bitrades_18")
    #b += process_spherical_file("spherical_bitrades_19")

    return b

if __name__ == "__main__":
    b = some_spherical_bitrades()

    i = 0
    while i < 10:
        T1 = b[i][0]
        T2 = b[i][1]

        cells_map = T1.filled_cells_map()
        t1 = Tau(T1, cells_map, _tau1(T1, T2, cells_map), 1)
        t2 = Tau(T1, cells_map, _tau2(T1, T2, cells_map), 2)
        t3 = Tau(T1, cells_map, _tau3(T1, T2, cells_map), 3)

        print i, t1, t2, t3

        i += 1

