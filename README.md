Triangle Dissection Enumeration
===============================

This repo contains code that supports the paper "An enumeration of
equilateral triangle dissections", Ales Drapal and Carlo Hamalainen,
Discrete Applied Mathematics Volume 158, Issue 14, 28 July 2010,
Pages 1479-1495. An open access (and more up to date version) is
available on the arXiv: http://arxiv.org/abs/0910.5199

Carlo Hamalainen <carlo.hamalainen@gmail.com>

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
