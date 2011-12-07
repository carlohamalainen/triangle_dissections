#!/bin/bash

set -x

bzcat /triangles/expt_4/all_sigs_4.bz2   | ./pp_perfect_dissections > pp_perfect_dissections_4.out

for N in `seq 6 24`
do
    bzcat /triangles/expt_${N}/all_sigs_${N}.bz2 | ./pp_perfect_dissections > pp_perfect_dissections_${N}.out
done
