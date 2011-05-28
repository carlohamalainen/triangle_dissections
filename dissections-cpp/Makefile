all: td td-binary-output

td: td.cpp
	g++ -Wall -O4 td.cpp -o td

td-binary-output: td-binary-output.cpp
	g++ -Wall -O4 td-binary-output.cpp -o td-binary-output

clean:
	rm -f td td-binary-output separated-signatures-*
