printf "%d %d\n" 4  `bzcat /triangles/expt_4/all_sigs_4.bz2  | wc -l`

for N in `seq 6 24`
do
    printf "%d %d\n" ${N}  `bzcat /triangles/expt_${N}/pp_isomer_sigs_${N}.out_sorted_and_uniq.bz2  | wc -l`
done
