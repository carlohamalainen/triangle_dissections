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
from sage.all import Rational

import sympy

from triangle_dissections import *
from draw_dissections import *


def enumerator_print_info(prefix, current_size, unique_dissections):
    for (t, i_uniq, r, c) in unique_dissections.itervalues():
        t.write_PDF(prefix + "dissection" + str(current_size) + "_i" + str(i_uniq) + "_r" + str(r)
                     + "_c" + str(c) + ".pdf", draw_labels = False)

def enumerate_unique_dissections(prefix = "output/", max_size = None, dissection_filter = (lambda x: True)):
    if max_size is not None:
        g = spherical_iterator(max_size = max_size)
    else:
        g = spherical_iterator()

    current_size = -1
    unique_dissections = {}

    i = -1

    while True:
        try:
            T1, T2 = g.next()
            i += 1
        except StopIteration:
            break

        if current_size < 0: current_size = T1.nr_filled_cells()

        if T1.nr_filled_cells() != current_size:
            current_size = T1.nr_filled_cells()
            print "looking at size", current_size

        for r, c in cross(range(T1.nrows()), range(T1.ncols())):
            if T1[r, c] < 0: continue

            try:
                t = TriangleDissection(T1, T2, r, c, only_separated_solutions = False)
            except ValueError:
                continue # there was no (separated?) solution

            if not dissection_filter(t): continue

            this_size = len(t.triangles)

            print T1.nr_filled_cells(), this_size

            if not unique_dissections.has_key(this_size):
                unique_dissections[this_size] = {}

            #import IPython
            #IPython.Shell.IPShell(user_ns=dict(globals(), **locals())).mainloop()

            unique_dissections[this_size][canonical_signature(t.points.keys())] = [t, i, r, c]

    for s in sorted(unique_dissections.keys()):
        print "    ", s, len(unique_dissections[s])
        enumerator_print_info(prefix, s, unique_dissections[s])

def disk_count_dissections(min_size, max_size, only_sep):
    g = spherical_iterator(min_size, max_size)

    i = -1

    current_perfect_dissection_size = -1
    perfect_dissections = {}

    signature_files = {}

    while True:
        try:
            T1, T2 = g.next()
            i += 1
        except StopIteration:
            break

        for r, c in cross(range(T1.nrows()), range(T1.ncols())):
            if T1[r, c] < 0: continue

            t = None

            try:
                t = TriangleDissection(T1, T2, r, c, only_separated_solutions = only_sep)
            except ValueError:
                continue # there was no (separated?) solution

            this_size = len(t.triangles)

            if False: # fixme pull this back in later
                if not lowerbound and t.is_perfect_dissection():
                    if this_size != current_perfect_dissection_size:
                        for (p, i_p, r_p, c_p) in perfect_dissections.itervalues():
                            p.write_PDF("perfect_dissection_size" + str(current_perfect_dissection_size)
                                + "_" + str(i_p) + "_r" + str(r_p) + "_c" + str(c_p)
                                + ".pdf", draw_labels = False, draw_sizes = True)

                        perfect_dissections = {}
                        current_perfect_dissection_size = this_size

                    perfect_dissections[t.canonical_signature()] = [t, i, r, c]

            sig = t.canonical_signature()
            sig = ' '.join(map(str, sig))

            sig_filename = "signatures_only_sep=" + str(only_sep) + "_" + str(this_size)
 
            if not signature_files.has_key(this_size):
                # Flush out any partial results
                for f in signature_files.itervalues(): f.flush()

                # Open a file for the new signatures
                signature_files[this_size] = open(sig_filename, 'w')

            signature_files[this_size].write(str(sig))
            signature_files[this_size].write('\n')
            
    for f in signature_files.itervalues(): f.close()

    # FIXME debugging, don't save perfect dissections at the moment
    return

    for (p, i_p, r_p, c_p) in perfect_dissections.itervalues():
        p.write_PDF("perfect_dissection_size" + str(current_perfect_dissection_size)
            + "_" + str(i_p) + "_r" + str(r_p) + "_c" + str(c_p)
            + ".pdf", draw_labels = False, draw_sizes = True)

def usage():
    print
    print "Examples of usage:"
    print
    print "Draw all unique dissections up to size 11:"
    print "$ sage unique_dissections.py -drawunique 11"
    print
    print "Enumerate dissections from size 11 to size 12 (inclusive) saving to"
    print "the files 'signatures_x'"
    print "$ sage unique_dissections.py -count 11 12"
    print
    print "Afterwards, count the number of unique dissections of some size using"
    print "a command like this:"
    print "$ sort signatures_12 | uniq | wc -l"
    print
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) == 1: usage()

    if len(sys.argv) == 3:
        if sys.argv[1] != '-drawunique': usage()
        try:
            size = int(sys.argv[2]) 
        except ValueError:
            usage()

        prefix = "output/"
        assert os.path.isdir(prefix)
        enumerate_unique_dissections(prefix, max_size = size)

        print "Now run 'pdflatex unique_dissections.tex"
        sys.exit(0)

    if len(sys.argv) == 4:
        if sys.argv[1] not in ['-count']: usage()

        try:
            min_size = int(sys.argv[2]) 
            max_size = int(sys.argv[3]) 
        except ValueError:
            usage()

        if sys.argv[1] == '-count':
            disk_count_dissections(min_size, max_size)
            sys.exit(0)

    usage()

