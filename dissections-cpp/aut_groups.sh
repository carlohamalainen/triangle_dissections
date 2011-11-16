#!/bin/bash


echo -n "4 "; bzcat /triangles/expt_4/all_sigs_4.bz2  | ./aut_groups

for n in `seq 6 24`
do
    echo -n "${n} "; bzcat /triangles/expt_${n}/all_sigs_${n}.bz2  | ./aut_groups
done
