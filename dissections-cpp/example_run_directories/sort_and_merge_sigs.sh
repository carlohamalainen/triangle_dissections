#!/bin/bash

N=$1

OUTFILE=all_sigs_${N}

# Sort each signature file and retain just the unique lines.
find . -iname 'sigs_*' -exec ../uniq_sigs.sh '{}' ';'

# Merge all of them together
sort -m sigs_* -o ${OUTFILE}

# Final pass to remove duplicates
../uniq_sigs.sh ${OUTFILE}

