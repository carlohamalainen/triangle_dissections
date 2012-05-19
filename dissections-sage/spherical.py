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

import os
import sys
import sage.all

from itertools import *
from sage.combinat.matrices.latin import *
from sage.misc.misc import tmp_filename

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
        sage: bitrades = process_spherical_file("spherical_bitrades/spherical_bitrades_8")
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
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_4")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_6")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_7")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_8")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_9")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_10")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_11")
    b += process_spherical_file("spherical_bitrades/spherical_bitrades_12")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_13")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_14")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_15")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_16")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_17")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_18")
    #b += process_spherical_file("spherical_bitrades/spherical_bitrades_19")

    return b

def spherical_iterator(min_size = 4, max_size = None):
    """
    An iterator to spherical bitrades. We expect files of the form
    spherical_bitrades_n where the bitrade has size n.
   
    EXAMPLE:
        sage: from spherical import *
        sage: g = spherical_iterator()
        sage: list(islice(g, 5))
        [([0 1]
        [1 0], [1 0]
        [0 1]), ([ 0  1 -1]
        [ 2  0 -1]
        [ 1  2 -1], [ 1  0 -1]
        [ 0  2 -1]
        [ 2  1 -1]), ([ 0  1  2]
        [ 1 -1  0]
        [-1  2  1], [ 1  2  0]
        [ 0 -1  1]
        [-1  1  2]), ([ 0  1 -1 -1]
        [ 2  0 -1 -1]
        [ 3  2 -1 -1]
        [ 1  3 -1 -1], [ 1  0 -1 -1]
        [ 0  2 -1 -1]
        [ 2  3 -1 -1]
        [ 3  1 -1 -1]), ([ 0  1  2 -1]
        [ 3 -1  0 -1]
        [ 1  2  3 -1]
        [-1 -1 -1 -1], [ 1  2  0 -1]
        [ 0 -1  3 -1]
        [ 3  1  2 -1]
        [-1 -1 -1 -1])]

    The first bitrade of size 10:

        sage: g = spherical_iterator(min_size = 10)
        sage: g.next()
        ([ 0  1 -1 -1 -1]
        [ 2  0 -1 -1 -1]
        [ 3  2 -1 -1 -1]
        [ 4  3 -1 -1 -1]
        [ 1  4 -1 -1 -1], [ 1  0 -1 -1 -1]
        [ 0  2 -1 -1 -1]
        [ 2  3 -1 -1 -1]
        [ 3  4 -1 -1 -1]
        [ 4  1 -1 -1 -1])


    """


    current_size = min_size

    assert min_size != 5 # no bitrades of size 5
    assert max_size != 5 # no bitrades of size 5

    f = None

    while True:
        if max_size is not None and current_size > max_size: break

        if f is None:
            try:
                f = open("spherical_bitrades/spherical_bitrades_" + str(current_size), 'r')
            except IOError:
                return

        try:
            (T1, T2) = read_spherical_bitrade(f)
        except ValueError:
            # We hit the end of file so move on to the next file.
            # Note that there is no bitrade of size 5.
            if current_size == 4:
                current_size = 6
            else:
                current_size += 1
            f.close()
            f = None
            continue

        yield (T1, T2)
        yield (T2, T1)

    if f is not None: f.close()


if __name__ == "__main__":
    b = some_spherical_bitrades()

    i = 0
    while i < 10:
        print "T1 ="
        print b[i][0]
        print "T2 ="
        print b[i][1]
        print
        print

        i += 1

