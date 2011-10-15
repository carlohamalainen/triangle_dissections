all: td pp_triangle_sizes pp_dissection_element_sizes

td: td.cpp ratlib.h
	g++ -Wall -O4 -I/opt/boost_1_47_0/ td.cpp -o td

pp_triangle_sizes: pp_triangle_sizes.cpp csig.h ratlib.h
	g++ -Wall -O4 -I/opt/boost_1_47_0/ pp_triangle_sizes.cpp -o pp_triangle_sizes

pp_dissection_element_sizes: pp_dissection_element_sizes.cpp csig.h ratlib.h
	g++ -Wall -O4 -I/opt/boost_1_47_0/ pp_dissection_element_sizes.cpp -o pp_dissection_element_sizes

pp_largest_in_interior: pp_largest_in_interior.cpp csig.h ratlib.h
	g++ -Wall -O4 -I/opt/boost_1_47_0/ -lm pp_largest_in_interior.cpp -o pp_largest_in_interior

clean:
	rm -f td pp_dissection_element_sizes pp_largest_in_interior pp_triangle_sizes separated_test_out_*
