#include <map>
#include <set>
#include "td.h"
#include "ratlib.h"

using namespace std;

Rational ratio_of_largest_to_smallest(vector<vector<Point> > &triangles)
{
    const int size_of_dissection = size_of_outer_triangle(triangles);

    int smallest_triangle = size_of_triangle(triangles.at(0), size_of_dissection);
    int largest_triangle  = size_of_triangle(triangles.at(0), size_of_dissection);

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < triangles.size(); i++) {
        const vector<Point> &triangle = triangles.at(i); 
        const int this_triangle_size  = size_of_triangle(triangle, size_of_dissection);

        if (this_triangle_size < smallest_triangle)
            smallest_triangle = this_triangle_size;

        if (this_triangle_size > largest_triangle)
            largest_triangle = this_triangle_size;
    }

    return Rational(largest_triangle)/Rational(smallest_triangle);
}

int main()
{
    std::string line;

    std::map<int, int> element_size_counts;

    map<Rational, unsigned long long> ratio_counts;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
        Rational r = ratio_of_largest_to_smallest(triangles);

        if (ratio_counts.find(r) == ratio_counts.end())
            ratio_counts[r] = 0;

        ratio_counts[r] += 1;
    }

    for(map<Rational, unsigned long long>::iterator it = ratio_counts.begin(); it != ratio_counts.end(); it++) {
        print_rational(stdout, it->first); printf(" %llu\n", it->second);
    }

    return 0;
}

