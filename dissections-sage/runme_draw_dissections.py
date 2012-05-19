#!/usr/bin/env sage-python

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
import os
import sys

from unique_dissections import enumerate_unique_dissections

if __name__ == "__main__":
    # fixme manual handling of arguments
    if len(sys.argv) != 3:
        print
        print
        print 'Draw dissections (both separated and nonseparated) up to'
        print 'a specified size. Output consists of PDF files in the directory'
        print './output-dissections/ or ./output-dissections/ and have files with names'
        print 'like dissection10_i15_r4_c1.pdf. The terms represent (in order): a dissection'
        print 'of size 10, the 15th produced for this size, with base point (r, c) = (4, 1).'
        print
        print 'Examples:'
        print
        print 'Draw all dissections up to size 10:'
        print
        print './runme_draw_dissections.py 10 all'
        print
        print 'Draw perfect dissections up to size 10:'
        print
        print './runme_draw_dissections.py 10 perfect'
        print
        sys.exit(1)

    size = int(sys.argv[1]) 

    dissection_type = sys.argv[2]
    assert dissection_type in ['all', 'perfect']

    if dissection_type == 'all':
        prefix = "output-dissections/"
        assert os.path.isdir(prefix)
        enumerate_unique_dissections(prefix, max_size = size)

    if dissection_type == 'perfect':
        prefix = "output-dissections-perfect/"
        assert os.path.isdir(prefix)
        enumerate_unique_dissections(prefix, max_size = size, dissection_filter = lambda t: t.is_perfect_dissection())
