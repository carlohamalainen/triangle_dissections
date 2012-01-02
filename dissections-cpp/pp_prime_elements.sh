bzcat /triangles/expt_4/all_sigs_4.bz2 | ./pp_prime_elements > pp_prime_elements.out_4

for n in `seq 6 24`
do
    bzcat /triangles/expt_${n}/all_sigs_${n}.bz2 | ./pp_prime_elements > pp_prime_elements.out_${n}
done
