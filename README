This repo contains code that supports the paper "An enumeration of
equilateral triangle dissections", Ales Drapal and Carlo Hamalainen,
Discrete Applied Mathematics Volume 158, Issue 14, 28 July 2010,
Pages 1479-1495. An open access (and more up to date version) is
available on the arXiv: http://arxiv.org/abs/0910.5199

Carlo Hamalainen <carlo.hamalainen@gmail.com>

2011-05-28

---------------------------------------------------------------

Example for running an enumeration of order 20 with 100 slices, with
output going to /scratch/triangles/...

    git clone https://github.com/carlohamalainen/triangle_dissections.git
    cd triangle_dissections
    make

If this fails due to not being able to find the Boost C++ library, set its
location in triangle_dissections/dissections-cpp/Makefile
and then re-run make in the top-level directory.

    cd dissections-cpp/example_run_directories

    N=20
    NRSLICES=100

    SRCDIR=`pwd`

    OUTPUT_DIRECTORY=/scratch/triangles/expt_$N

    mkdir -p $OUTPUT_DIRECTORY
    cd $OUTPUT_DIRECTORY
    ln -s $SRCDIR/create_makefile.py
    ln -s $SRCDIR/run_slice.sh
    ln -s $SRCDIR/sort_and_merge_sigs.sh
    ln -s $SRCDIR/uniq_sigs.sh

    ./create_makefile.py $SRCDIR/../.. $N $NRSLICES

To run the first part of the enumeration, use the Makefile with a suitable 
number of threads, say 14 on a 16 core PC:

    make -j 14

Once this finishes there will be $NRSLICES files of the form sigs_<slice nr>.
To merge them into a single file containing a unique list of signatures, run the
following script:

    ./sort_and_merge_sigs.sh $N

This will produce the file $OUTPUT_DIRECTORY/all_sigs_$N.



