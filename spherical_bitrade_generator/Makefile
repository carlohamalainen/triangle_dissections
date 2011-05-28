all: spherical_trades spherical_trades_binary

spherical_trades: plantri.c spherical_trades.c
	gcc -o spherical_trades -O4 '-DPLUGIN="spherical_trades.c"' plantri.c

spherical_trades_binary: plantri.c spherical_trades_binary.c
	gcc -o spherical_trades_binary -O4 '-DPLUGIN="spherical_trades_binary.c"' plantri.c

clean:
	rm spherical_trades spherical_trades_binary
