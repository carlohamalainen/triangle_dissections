# Run some tests with only source separated bitrades up to size 13 or 14.

rm -f test_upto_*

A=13
B=14

./td --separated-and-nonseparated test_upto_$A < ../spherical_bitrade_generator/binary_spherical_bitrades_4
for n in `seq 6 $A`
do
    # cat /triangles/expt_${n}/binary_bitrades_${n}_* | ./td --separated-and-nonseparated test_upto_$A 
    cat ../spherical_bitrade_generator/binary_spherical_bitrades_${n} | ./td --separated-and-nonseparated test_upto_$A 
done

# Now count this enumeration:
echo -n "4 "
cat test_upto_${A}out_4 | sort | uniq | wc -l

for n in `seq 6 ${A}`
do
    echo -n "${n} "
    cat test_upto_${A}out_${n} | sort | uniq | wc -l
done

echo
echo



# Run some tests with only source separated bitrades up to size 16:

./td --separated-and-nonseparated test_upto_${B} < ../spherical_bitrade_generator/binary_spherical_bitrades_4
for n in `seq 6 ${B}`
do
    # cat /triangles/expt_${n}/binary_bitrades_${n}_* | ./td --separated-and-nonseparated test_upto_${B} 
    cat ../spherical_bitrade_generator/binary_spherical_bitrades_${n} | ./td --separated-and-nonseparated test_upto_${B} 
done

# Now count this enumeration:
echo -n "4 "
cat test_upto_${B}out_4 | sort | uniq | wc -l

for n in `seq 6 ${B}`
do
    echo -n "${n} "
    cat test_upto_${B}out_${n} | sort | uniq | wc -l
done

