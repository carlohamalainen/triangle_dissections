all: done_0_1 

binary_bitrades_4_0_1:
	/home/carlo/work/github/triangle_dissections/spherical_bitrade_generator/spherical_trades_binary -b -u 6 0/1 > binary_bitrades_4_0_1

done_0_1: binary_bitrades_4_0_1
	./run_slice.sh 4 0 1

