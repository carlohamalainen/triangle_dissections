Triangle Dissection Enumeration
===============================

This repo contains code that supports the paper "An enumeration of
equilateral triangle dissections", Ales Drapal and Carlo Hamalainen,
Discrete Applied Mathematics Volume 158, Issue 14, 28 July 2010,
Pages 1479-1495. An open access (and more up to date version) is
available on the arXiv: http://arxiv.org/abs/0910.5199

Carlo Hamalainen <carlo@carlo-hamalainen.net>

Summary of contents
-------------------

 * dissections-clojure:         Implementation in Clojure     (for testing only)
 * dissections-common-lisp:     Implementation in Common Lisp (for testing only)
 * dissections-cpp:             Implementation in C++         (for actual enumeration runs)
 * dissections-sage:            Original implementation in Sage (useful for exploratory work)
 * paper:                       Copy of the arXiv paper
 * plot:                        Python script (uses PyX) for drawing triangle dissections
 * spherical_bitrade_generator: Enumerator of spherical latin bitrades (uses "plantri")

How to run
----------

To run the enumerator for order 18 with 5 slices, output
going to /tmp/triangles/expt_18:

    git clone https://github.com/carlohamalainen/triangle_dissections.git
    cd triangle_dissections
    make

If this fails due to not being able to find the Boost C++ library, set its
location in triangle_dissections/dissections-cpp/Makefile
and then re-run make in the top-level directory.

### Running on a Mac in 2026

The Makefiles predate modern clang. Verified on macOS (Apple Silicon, clang 17)
with Homebrew Boost:

    brew install boost

    # plantri needs C89 leniency (implicit int, implicit strcpy/strcmp)
    cd spherical_bitrade_generator
    gcc -std=gnu89 -w -O3 -include string.h -include stdlib.h \
        '-DPLUGIN="spherical_trades_binary.c"' plantri.c -o spherical_trades_binary

    # td just needs Homebrew's Boost headers
    cd ../dissections-cpp
    g++ -w -O3 -I/opt/homebrew/include td.cpp -o td

Then a quick separated-and-nonseparated run for order N, using all 8 cores
(no run directory needed):

    N=16
    for s in $(seq 0 7); do
      ( ./spherical_trades_binary -b -u $((N+2)) $s/8 | ./td --separated-and-nonseparated | sort -u > sigs_${N}_$s ) &
    done; wait
    sort -u sigs_${N}_* | wc -l     # 19665 for N=16

On an 8-core Apple Silicon Mac this takes roughly 1s for N=16, 20s for N=18
and 70s for N=19.

Now create a directory for this run of order 18 with 5 slices, and set up
the Makefile which will run the main part of the enumeration:

    cd dissections-cpp/example_run_directories

    N=18
    NRSLICES=5

    SRCDIR=`pwd`

    OUTPUT_DIRECTORY=/tmp/triangles/expt_$N

    mkdir -p $OUTPUT_DIRECTORY
    cd $OUTPUT_DIRECTORY
    ln -s $SRCDIR/create_makefile.py
    ln -s $SRCDIR/run_slice.sh
    ln -s $SRCDIR/sort_and_merge_sigs.sh
    ln -s $SRCDIR/uniq_sigs.sh

    ./create_makefile.py $SRCDIR/../.. $N $NRSLICES

To run the first part of the enumeration, use the Makefile with a suitable 
number of threads, say 14 on a 16 core PC:

    make -j 14 # this would be at most the minimum of nr cores in PC and nr slices being produced

Once this finishes there will be $NRSLICES files of the form sigs_<slice nr>.
To merge them into a single file containing a unique list of signatures, run the
following script:

    ./sort_and_merge_sigs.sh $N

This will produce the file $OUTPUT_DIRECTORY/all_sigs_$N. This file can be used with
post-processing scripts, or to answer simple questions like "how many dissections are
there of order 18?":

    cat all_sigs_$N | wc -l

The answer should be:

    224708

Note that this is the count of separated and nonseparated dissections
(`td --separated-and-nonseparated`). It differs from Figure 7 of the published
paper (224700), which undercounts nonseparated dissections for n >= 16 because
the original code used only the set of vertex locations as a canonical
signature; see `dissections-cpp/find_nonsep_sig_problem.*` and
https://github.com/carlohamalainen/triangle_dissections/issues/1
Corrected values: n=16: 19665, 17: 66051, 18: 224708, 19: 771893, 20: 2674866.
The separated-only counts (Figure 6, `dissections-cpp/signature_counts_upto_24.txt`)
are unaffected.

Update (August 2026)
--------------------

[OEIS A299705](https://oeis.org/A299705) has been
corrected to the values above. The corrected values were obtained by two
independent enumerators (the plantri/bitrade route and a direct canonical
filling of the triangular grid) and then confirmed with the C++ code in
this repo.

The automorphism-group columns A(n,k) of Figure 7 were also affected for
n >= 16. Corrected values:

| n  | A(n,1)    | A(n,2) | A(n,3) | A(n,6) |
|---:|----------:|-------:|-------:|-------:|
| 16 |    19,380 |    278 |      2 |      5 |
| 17 |    65,490 |    561 |      0 |      0 |
| 18 |   223,630 |  1,073 |      0 |      5 |
| 19 |   769,875 |  2,001 |      8 |      9 |
| 20 | 2,670,849 |  4,017 |      0 |      0 |

The perfect dissection counts in Section 3.2 of the paper ([OEIS A290653](https://oeis.org/A290653))
are unaffected: none of the missed dissections is perfect, so there is
still no known nonseparated perfect dissection of size <= 20.
