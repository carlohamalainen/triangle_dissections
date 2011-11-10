/*

   Compute the integer size of the outer triangle for each dissection
   given in the canonical signature file (require parameter). For each
   triangle size we print the number of dissections with that size.

    ./pp_triangle_sizes  /triangles/expt_4/all_sigs_4 
    2 1 # one triangle of size 2

    ./pp_triangle_sizes  /triangles/expt_6/all_sigs_6 
    3 1 # one triangle of size 3

    ./pp_triangle_sizes  /triangles/expt_7/all_sigs_7 
    4 2 # two triangles of size 4
    ...

    ./pp_triangle_sizes  /triangles/expt_10/all_sigs_10 
    5 1
    7 5
    8 11 # eleven triangles of size 8
    9 3  # three triangles  of size 9

*/

#include <map>
#include "td.h"
#include "ratlib.h"

using namespace std;

int main()
{
    std::string line;

    std::map<unsigned long long, unsigned long long> triangle_size_counts;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);

        int t_size = size_of_outer_triangle(triangles);

        if (triangle_size_counts.find(t_size) == triangle_size_counts.end())
            triangle_size_counts[t_size] = 0;

        triangle_size_counts[t_size] += 1;
    }

    for(std::map<unsigned long long, unsigned long long>::iterator it = triangle_size_counts.begin(); it != triangle_size_counts.end(); it++) {
        printf("%llu %llu\n", it->first, it->second);
    }

    return 0;
}


