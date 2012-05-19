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

from unique_dissections import disk_count_dissections

if __name__ == "__main__":
    # fixme manual handling of arguments
    if len(sys.argv) != 3:
        print 'Count separated or nonseparated dissections up to a specified size.'
        print
        print 'Examples:'
        print
        print 'Count separated dissections up to size 13:'
        print '$ ./runme_count_dissections.py 13 separated'
        print
        print 'Count nonseparated dissections up to size 13:'
        print '$ ./runme_count_dissections.py 13 nonseparated'
        print
        print 'In both cases, process the output files signatures_* using'
        print 'the script count_aut_groups.sh'
        print
        sys.exit(1)

    max_size = int(sys.argv[1]) 
    only_sep = sys.argv[2]
    assert only_sep in ['separated', 'nonseparated']
    only_sep = only_sep == 'separated'

    disk_count_dissections(4, max_size, only_sep)





