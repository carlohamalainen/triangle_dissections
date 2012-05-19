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

import sys

import pyx
from sage.combinat.matrices.latin import *
from sage.misc.search import search
from sage.rings.rational_field import QQ
from sage.rings.arith import lcm
import math

from spherical import *
from triangle_dissections import *

import sympy

def aut_group_size(dissection_vertices):
    """
    Calculate the order of the automorphism group of a triangle
    dissection described by its vertices (this is the output from
    disk_count_dissections in unique_dissections.py). We try each of
    the five non-identity automorphisms directly.

    EXAMPLES::

        sage: aut_group_size(((0, 0), (1/6, 3**(1/2)/6), (1/3, 0), (1/3, 3**(1/2)/3), (1/2, 3**(1/2)/6), (1/2, 3**(1/2)/2), (2/3, 3**(1/2)/3), (1, 0)))
        2

        sage: aut_group_size(((0, 0), (1/12, 3**(1/2)/12), (1/6, 0), (1/6, 3**(1/2)/6), (1/4, 3**(1/2)/12), (1/3, 0), (1/3, 3**(1/2)/3), (1/2, 3**(1/2)/6), (1/2, 3**(1/2)/2), (2/3, 3**(1/2)/3), (1, 0)))
        1

        sage: aut_group_size(((0, 0), (1/6, 3**(1/2)/6), (1/4, 3**(1/2)/4), (1/3, 0), (1/3, 3**(1/2)/6), (1/3, 3**(1/2)/3), (5/12, 3**(1/2)/4), (1/2, 3**(1/2)/6), (1/2, 3**(1/2)/2), (2/3, 3**(1/2)/3), (1, 0)))
        2

        sage: aut_group_size(((0, 0), (1/12, 3**(1/2)/12), (1/6, 0), (1/6, 3**(1/2)/6), (1/4, 3**(1/2)/12), (1/3, 0), (1/3, 3**(1/2)/3), (1/2, 3**(1/2)/6), (1/2, 3**(1/2)/2), (2/3, 3**(1/2)/3), (1, 0)))
        1
    """

    aut_size = 1 # Aut(dissection_vertices) always has the identity element

    dissection_vertices = sorted(dissection_vertices)

    if sorted([reflect1(x, y) for (x, y) in dissection_vertices]) == dissection_vertices:                   aut_size += 1
    if sorted([reflect2(x, y) for (x, y) in dissection_vertices]) == dissection_vertices:                   aut_size += 1
    if sorted([reflect3(x, y) for (x, y) in dissection_vertices]) == dissection_vertices:                   aut_size += 1
    if sorted([rotate_equilateral(x, y) for (x, y) in dissection_vertices]) == dissection_vertices:         aut_size += 1
    if sorted([rotate_equilateral_inverse(x, y) for (x, y) in dissection_vertices]) == dissection_vertices: aut_size += 1

    return aut_size


# For usage see the script count_aut_groups.sh

if __name__ == "__main__":
    counts = {1:0, 2:0, 3:0, 6:0}

    total = 0

    for line in sys.stdin.readlines():
        d = sympy.sympify(line)

        s = aut_group_size(d)

        assert s in [1, 2, 3, 6]

        total += 1
        counts[s] = counts[s] + 1

    T_size = len(d) - 2

    print r"\hline " + str(T_size) + r" & " + str(counts[1]) + r" & " + str(counts[2]) + r" & " + str(counts[3]) + r" & " + str(counts[6]) + r" \\"

    assert sum(counts.values()) == total
