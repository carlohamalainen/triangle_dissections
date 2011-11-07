/*

   Compute the integer size of the each triangle in each dissection
   given in the canonical signature file (require parameter). For
   each element size we print the number of dissections with that
   size element.


*/

#include <map>
#include "csig.h"
#include "ratlib.h"

using namespace std;

void size_of_inner_triangles(vector<vector<Point> > &triangles, std::map<unsigned long long, unsigned long long> &element_size_counts)
{
    // The dissections are presented with side y = 0 along the interval [0, 1]. Compute the
    // size of this triangle dissection if each sub-triangle has integer side length. We can use
    // this as a multiplicative factor to work out the size of any sub-triangle.
    const int size_of_dissection = size_of_outer_triangle(triangles);

    vector<bool> seen_sizes(size_of_dissection, 0);

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < triangles.size(); i++) {
        const vector<Point> &triangle = triangles.at(i); 
        const int this_triangle_size  = size_of_triangle(triangle, size_of_dissection);

        seen_sizes.at(this_triangle_size) = true;
    }

    for(int i = 0; i < size_of_dissection; i++) {
        if (seen_sizes.at(i)) {
            if (element_size_counts.find(i) == element_size_counts.end())
                element_size_counts[i] = 0;

            element_size_counts.at(i) += 1;
        }
    }
}

int main()
{
    std::string line;

    std::map<unsigned long long, unsigned long long> element_size_counts;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
        size_of_inner_triangles(triangles, element_size_counts);
    }

    for(std::map<unsigned long long, unsigned long long>::iterator it = element_size_counts.begin(); it != element_size_counts.end(); it++) {
        printf("%llu %llu\n", it->first, it->second);
    }

    return 0;
}

