all: spherical_trades spherical_trades_binary spherical_bitrades_upto_14

spherical_trades: plantri.c spherical_trades.c
	gcc -o spherical_trades -O4 '-DPLUGIN="spherical_trades.c"' plantri.c

spherical_trades_binary: plantri.c spherical_trades_binary.c
	gcc -o spherical_trades_binary -O4 '-DPLUGIN="spherical_trades_binary.c"' plantri.c

spherical_bitrades_upto_14: spherical_trades spherical_trades_binary
	./spherical_trades -b -u 6  > spherical_bitrades_4
	./spherical_trades -b -u 8  > spherical_bitrades_6
	./spherical_trades -b -u 9  > spherical_bitrades_7
	./spherical_trades -b -u 10 > spherical_bitrades_8
	./spherical_trades -b -u 11 > spherical_bitrades_9
	./spherical_trades -b -u 12 > spherical_bitrades_10
	./spherical_trades -b -u 13 > spherical_bitrades_11
	./spherical_trades -b -u 14 > spherical_bitrades_12
	./spherical_trades -b -u 15 > spherical_bitrades_13
	./spherical_trades -b -u 16 > spherical_bitrades_14
	./spherical_trades_binary -b -u 6  > binary_spherical_bitrades_4
	./spherical_trades_binary -b -u 8  > binary_spherical_bitrades_6
	./spherical_trades_binary -b -u 9  > binary_spherical_bitrades_7
	./spherical_trades_binary -b -u 10 > binary_spherical_bitrades_8
	./spherical_trades_binary -b -u 11 > binary_spherical_bitrades_9
	./spherical_trades_binary -b -u 12 > binary_spherical_bitrades_10
	./spherical_trades_binary -b -u 13 > binary_spherical_bitrades_11
	./spherical_trades_binary -b -u 14 > binary_spherical_bitrades_12
	./spherical_trades_binary -b -u 15 > binary_spherical_bitrades_13
	./spherical_trades_binary -b -u 16 > binary_spherical_bitrades_14
	./spherical_trades_binary -b -u 17 > binary_spherical_bitrades_15
	./spherical_trades_binary -b -u 18 > binary_spherical_bitrades_16
	./spherical_trades_binary -b -u 19 > binary_spherical_bitrades_17
	./spherical_trades_binary -b -u 20 > binary_spherical_bitrades_18
	touch spherical_bitrades_upto_14
	
clean:
	rm -f spherical_trades spherical_trades_binary spherical_bitrades_* binary_spherical_bitrades_*
