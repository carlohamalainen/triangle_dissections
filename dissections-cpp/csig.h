#ifndef __CSIG__
#define __CSIG__

#include <vector>
#include "ratlib.h"

vector<vector<Point> > parse_csig_line(string line)
{
    std::vector<std::string> strs;
    boost::split(strs, line, boost::is_any_of(" "));

    assert(strs.at(strs.size() - 1) == ""); // this is the trailing newline

    unsigned int i = 0;

    vector<vector<Point> > triangles;

    while(i < strs.size() - 1) {
        vector<Point> new_triangle;

        for(unsigned int t = 0; t < 3; t++) {
            Rational r_1  = parse_rational(strs.at(i++));
            Rational r_2  = parse_rational(strs.at(i++));
            Rational r_3  = parse_rational(strs.at(i++));
            Rational r_4  = parse_rational(strs.at(i++));

            Point p = {QQ3(r_1, r_2), QQ3(r_3, r_4)};

            new_triangle.push_back(p);
        }

        assert(new_triangle.size() == 3);
        triangles.push_back(new_triangle);
    }

    // Make sure that we consumed the whole line.
    assert(i == strs.size() - 1);

    return triangles;
}

int size_of_outer_triangle(vector<vector<Point> > &triangles)
{
    const QQ3 QQ3_zero = QQ3(0, 0);
    const Rational Rational_zero = Rational(0);

    vector<int> denominators;

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < triangles.size(); i++) {
        vector<Point> &triangle = triangles.at(i); 
        assert(triangle.size() == 3);

        // Find the two vertices that are along the line y = c for some constant c
        int a, b;

        if (triangle.at(0).y == triangle.at(1).y) {
            a = 0; b = 1;
        } else if (triangle.at(0).y == triangle.at(2).y) {
            a = 0; b = 2;
        } else if (triangle.at(1).y == triangle.at(2).y) {
            a = 1; b = 2;
        } else {
            // Oh dear - this triangle doesn't have a horizontal line?
            assert(false);
        }

        assert(triangle.at(a).y == triangle.at(b).y);

        // side length of this triangle
        QQ3 s = triangle.at(a).x - triangle.at(b).x;
        assert(s.b == Rational_zero);
        Rational side_length = abs_rat(s.a);

        denominators.push_back(side_length.denominator);
    }

    return lcm(denominators);
}

int size_of_triangle(const vector<Point> &triangle, const int size_of_dissection)
{
    const Rational Rational_zero = Rational(0);

    assert(triangle.size() == 3);
    assert(size_of_dissection > 1);

    // Find the two vertices that are along the line y = c for some constant c
    int a, b;

    if (triangle.at(0).y == triangle.at(1).y) {
        a = 0; b = 1;
    } else if (triangle.at(0).y == triangle.at(2).y) {
        a = 0; b = 2;
    } else if (triangle.at(1).y == triangle.at(2).y) {
        a = 1; b = 2;
    } else {
        // Oh dear - this triangle doesn't have a horizontal line?
        assert(false);
    }

    assert(triangle.at(a).y == triangle.at(b).y);

    // Rational s = size_of_dissection*(triangle.at(a).x - triangle.at(b).x);
    QQ3 s = triangle.at(a).x - triangle.at(b).x;

    assert(s.b == Rational_zero);

    Rational result = abs_rat(Rational(size_of_dissection)*s.a);
    assert(result.denominator == 1);

    return result.numerator;
}

#endif
