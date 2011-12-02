
#include <map>
#include "td.h"
#include "ratlib.h"

using namespace std;

bool is_up_triangle(const vector<Point> &triangle)
{
    assert (triangle.size() == 3);

    int i, j;

    i = 0; j = 1;
    if (triangle.at(i).y == triangle.at(j).y)
        return triangle.at(i).y < triangle.at(2).y;

    i = 0; j = 2;
        return triangle.at(i).y < triangle.at(1).y;

    i = 1; j = 2;
        return triangle.at(i).y < triangle.at(0).y;
}


bool is_perfect_dissection(vector<vector<Point> > &triangles)
{
    // The dissections are presented with side y = 0 along the interval [0, 1]. Compute the
    // size of this triangle dissection if each sub-triangle has integer side length. We can use
    // this as a multiplicative factor to work out the size of any sub-triangle.
    const int size_of_dissection = size_of_outer_triangle(triangles);

    vector<bool> seen_up_sizes(size_of_dissection,   false);
    vector<bool> seen_down_sizes(size_of_dissection, false);

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < triangles.size(); i++) {
        const vector<Point> &triangle = triangles.at(i); 
        const int this_triangle_size  = size_of_triangle(triangle, size_of_dissection);

        if (is_up_triangle(triangle)) {
            if (seen_up_sizes.at(this_triangle_size))
                return false;
            else
                seen_up_sizes.at(this_triangle_size) = true;
        } else {
            if (seen_down_sizes.at(this_triangle_size))
                return false;
            else
                seen_down_sizes.at(this_triangle_size) = true;
        }

    }

    return true;
}

int main()
{
    std::string line;

    unsigned long long nr_perfect_disections = 0;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
    
        if (is_perfect_dissection(triangles))
            nr_perfect_disections++;
    }

    printf("%llu\n", nr_perfect_disections);

    return 0;
}

