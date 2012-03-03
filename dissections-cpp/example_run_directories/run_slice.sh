#!/bin/bash

set -o nounset

N=$1
slice=$2
nr_slices=$3

cat binary_bitrades_${N}_${slice}_${nr_slices} | /home/carlo/work/github/triangle_dissections/dissections-cpp/td --separated-and-nonseparated > sigs_${slice}_out_${N}

if [ "$?" -ne 0 ]; then
    exit 1
fi 

sort -o sigs_${slice}_out_${N} sigs_${slice}_out_${N}

if [ "$?" -eq 0 ]; then
    touch done_${slice}_${nr_slices}
fi 
