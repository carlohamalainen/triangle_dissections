#include <map>
#include "td.h"
#include "ratlib.h"
#include <math.h>

using namespace std;

const QQ3 QQ3_zero = QQ3(0, 0);

bool is_on_line_0(Point &p)
{
    // is p on the line y = 0?
    return p.y == QQ3_zero;
}

bool is_on_line_1(Point &p)
{
    // is p on the line from (0, 0) to (1/2, sqrt(3)/2)?

    // First, we have to be in the left half of the dissection.
    if (qq3_gt(p.x, QQ3(Rational(1, 2), 0))) return false;

    // Now check if we are on y = sqrt(3)*x
    return p.y == QQ3(0, 1)*p.x;
}

bool is_on_line_2(Point &p)
{
    // is p on the line from (1/2, sqrt(3)/2) to (1, 0)?

    // First, we have to be in the right half of the dissection.
    if (qq3_lt(p.x, QQ3(Rational(1, 2), 0))) return false;

    // Now check if we are on y = -sqrt(3)*x + sqrt(3)
    return p.y == QQ3(0, -1)*p.x + QQ3(0, 1);
}

bool is_interior_triangle(vector<Point> &triangle)
{
    assert(triangle.size() == 3);

    for(unsigned int i = 0; i < 3; i++) {
        Point &p = triangle.at(i);

        if (is_on_line_0(p) || is_on_line_1(p) || is_on_line_2(p))
            return false;
    }

    return true;
}

bool poop(vector<vector<Point> > &dissection)
{
    const int size_of_dissection = size_of_outer_triangle(dissection);

    int max_triangle_size = -1;
    vector<vector<Point> > largest_triangles;

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < dissection.size(); i++) {
        const vector<Point> &triangle = dissection.at(i); 
        const int this_triangle_size  = size_of_triangle(triangle, size_of_dissection);

        if (this_triangle_size > max_triangle_size) {
            largest_triangles.clear();
            max_triangle_size = this_triangle_size;
            largest_triangles.push_back(triangle);
        }
    }

    // Now check if any of these largest triangles are 
    // completely in the interior of the dissection.
    for(vector<vector<Point> >::iterator it = largest_triangles.begin(); it != largest_triangles.end(); it++) {
        if (is_interior_triangle(*it))
            return true;
    }

    return false;
}


int main()
{
    std::string line;

    while (getline(cin, line)) {
        vector<vector<Point> > dissection = parse_csig_line(line);
        if (poop(dissection)) {
            std::cout << line << std::endl;
        }
    }

    return 0;
}

