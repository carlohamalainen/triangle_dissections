#!/bin/bash

set -x

bzcat /triangles/expt_4/all_sigs_4.bz2   | ./pp_isomer_sigs > /triangles/expt_4/pp_isomer_sigs_4.out

for N in `seq 6 24`
do
    bzcat /triangles/expt_${N}/all_sigs_${N}.bz2 | ./pp_isomer_sigs | bzip2 -c > /triangles/expt_${N}/pp_isomer_sigs_${N}.out.bz2
done
