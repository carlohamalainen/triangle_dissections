#!/bin/bash

set -x

bzcat /triangles/expt_4/all_sigs_4.bz2   | ./pp_dissection_element_sizes > pp_dissection_element_sizes_4.out

for N in `seq 6 24`
do
    bzcat /triangles/expt_${N}/all_sigs_${N}.bz2 | ./pp_dissection_element_sizes > pp_dissection_element_sizes_${N}.out
done
