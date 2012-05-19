#!/bin/bash

# The automorphism group of a triangle dissection has order 1, 2, 3,
# or 6.  This script counts, for each dissection size, the number of
# automorphism groups of size 1, 2, 3, and 6.
# 
# The signatures_* files have at least one distinct line for each
# triangle dissection of a certain type (separate or nonseparated). We
# just pipe the unique lines to count_aut_groups.py, which does the
# automorphism group calculations.

export SAGE_PATH=$HOME/pyxinstall

mkdir dissection_counts

rm dissection_counts/count_aut_ALL.out
rm dissection_counts/count_aut_SEPARATED.out

cat signatures_only_sep=False_4  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_6  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_7  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_8  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_9  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_10 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_11 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_12 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_13 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_14 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_15 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_16 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_17 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_18 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_19 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out
cat signatures_only_sep=False_20 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_ALL.out

cat signatures_only_sep=True_4  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_6  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_7  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_8  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_9  | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_10 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_11 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_12 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_13 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_14 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_15 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_16 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_17 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_18 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_19 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out
cat signatures_only_sep=True_20 | sort | uniq | sage count_aut_groups.py >> dissection_counts/count_aut_SEPARATED.out


