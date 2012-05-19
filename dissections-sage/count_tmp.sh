#!/bin/bash

echo -n "4 "; cat "signatures_only_sep=False_4"  | sort | uniq | wc -l

for n in `seq 6 18`
do
    echo -n "$n "; cat "signatures_only_sep=False_$n"  | sort | uniq | wc -l
done



