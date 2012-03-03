BOOST_PATH = /home/carlo/opt/boost_1_47_0/

all: td aut_groups pp_triangle_sizes pp_dissection_element_sizes pp_largest_in_interior pp_ratio_spectrum pp_isomer_sigs pp_perfect_dissections

td: td.cpp td.h ratlib.h
	g++ -std=gnu++0x -Wall -O4 -I$(BOOST_PATH) td.cpp -o td

aut_groups: aut_groups.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) aut_groups.cpp -o aut_groups

pp_triangle_sizes: pp_triangle_sizes.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) pp_triangle_sizes.cpp -o pp_triangle_sizes

pp_dissection_element_sizes: pp_dissection_element_sizes.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) pp_dissection_element_sizes.cpp -o pp_dissection_element_sizes

pp_largest_in_interior: pp_largest_in_interior.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) -lm pp_largest_in_interior.cpp -o pp_largest_in_interior

pp_ratio_spectrum: pp_ratio_spectrum.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) -lm pp_ratio_spectrum.cpp -o pp_ratio_spectrum

pp_isomer_sigs: pp_isomer_sigs.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) -lm pp_isomer_sigs.cpp -o pp_isomer_sigs

pp_perfect_dissections: pp_perfect_dissections.cpp td.h ratlib.h
	g++ -Wall -O4 -I$(BOOST_PATH) -lm pp_perfect_dissections.cpp -o pp_perfect_dissections

clean:
	rm -f td pp_dissection_element_sizes pp_largest_in_interior pp_triangle_sizes pp_ratio_spectrum pp_isomer_sigs separated_test_out_*
