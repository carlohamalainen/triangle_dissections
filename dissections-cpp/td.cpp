#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <set>
#include <vector>

#include <cstring>

#include "ratlib.h"

using namespace std;

#define MAX_OUTPUT_NR 50

// <globals>
bool only_separated;
FILE * output_files[MAX_OUTPUT_NR+1];
// </globals>


//////////// Globals for the reduced row echelon form algorithm ///////////
int __nr_rows;                                                           //
int __nr_cols;                                                           //
vector<Rational> __M;                                                    //
///////////////////////////////////////////////////////////////////////////

// Retrieve the value at M[row, col].
Rational get(int row, int col)
{
    return __M[row*__nr_cols + col];
}

// Set the value at M[row, col].
void __set(int row, int col, Rational value)
{
    __M[row*__nr_cols + col] = value;
}

// Pretty-print the matrix M.
void print_matrix()
{
    int r, c;

    for(r = 0; r < __nr_rows; r++) {
        for(c = 0; c < __nr_cols; c++) {
            print_rational(stdout, get(r, c)); printf(" ");
        }
        printf("\n");
    }
    printf("\n");
}

// M[row1, :], M[row2, :] = M[row2, :], M[row1, :]
void swap_rows(int row1, int row2)
{
    Rational tmp;
    int c;

    for(c = 0; c < __nr_cols; c++) {
        tmp = get(row1, c);           // tmp = M[row1, c]
        __set(row1, c, get(row2, c));   // M[row1, c] = M[row2, c]
        __set(row2, c, tmp);            // M[row2, c] = tmp
    }
}

// Divide each element of row r by value.
void divide_row(int r, Rational value)
{
    assert(value.numerator != 0);

    int c;

    for(c = 0; c < __nr_cols; c++) {
        __set(r, c, get(r, c)/value);
    }
}

// Convenience function for one of the steps in the
// rref algorithm.
void mult_and_sub(int i, int r, Rational lv)
{
    int c;

    for(c = 0; c < __nr_cols; c++) {
        __set(i, c, get(i, c) - get(r, c)*lv);
    }
}

// Direct translation of http://rosettacode.org/wiki/Reduced_row_echelon_form#Python
void rref()
{
    int i, r;
    int lead = 0;
    Rational lv;

    for(r = 0; r < __nr_rows; r++) {
        if (lead >= __nr_cols)
            return;

        i = r;
        while(get(i, lead).numerator == 0) {
            i += 1;
            if (i == __nr_rows) {
                i = r;
                lead += 1;
                if (__nr_cols == lead)
                    return;
            }
        }

        swap_rows(i, r); // M[i],M[r] = M[r],M[i]

        lv = get(r, lead);
        divide_row(r, lv); // M[r] = [ mrx / lv for mrx in M[r]]
        for(i = 0; i < __nr_rows; i++) {
            if (i != r) {
                lv = get(i, lead);
                mult_and_sub(i, r, lv); // M[i] = [ iv - lv*rv for rv,iv in zip(M[r],M[i])];
            }
        }
        lead += 1;
    }
}

typedef struct struct_triple {
    int r, c, s;
} Triple;

bool read_bitrade(int &nr_rows, int &nr_cols, int &nr_syms, int &nr_elements, vector<Triple> &T1, vector<Triple> &T2)
{
    unsigned char c_in;

    if (fread(&c_in, sizeof(unsigned char), 1, stdin) != 1)
        return false;
        
    nr_rows = c_in;

    assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    nr_cols     = c_in;
    assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    nr_syms     = c_in;
    assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    nr_elements = c_in;

    T1.resize(nr_elements);
    for(int i = 0; i < nr_elements; i++) {
        int r, c, s;

        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    r = c_in;
        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    c = c_in;
        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    s = c_in;

        Triple t = {r, c, s};

        T1[i] = t;
    }

    T2.resize(nr_elements);
    for(int i = 0; i < nr_elements; i++) {
        int r, c, s;

        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    r = c_in;
        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    c = c_in;
        assert(fread(&c_in, sizeof(unsigned char), 1, stdin) == 1);    s = c_in;

        Triple t = {r, c, s};

        T2[i] = t;
    }


    return true;
}

void zero_row(int row)
{
    const Rational rat0(0, 1);

    for(int c = 0; c < __nr_cols; c++)
        __set(row, c, rat0);
}

/*
Given an identity triple and a bitrade (T1, T2), calculate the solution to its associated linear
system of equations. The solution is placed in the vector 'solution', in the order rows,
columns, and then symbols. See triples_to_triangles() for how to unpack the solution.
 */
void calculate_bitrade_solution(int nr_rows, int nr_cols, int nr_syms, Triple identity_triple,
                                vector<Triple> &T1, vector<Triple> &T2, vector<Rational> &solution)
{
    const int nr_rows_matrix = 3 + T1.size() - 1; //  3 identity equations, |T1|-1 element equations
    const int nr_cols_matrix = nr_rows + nr_cols + nr_syms + 1;

    assert(solution.size() == (unsigned int) nr_rows_matrix);

    __M.resize(nr_rows_matrix*nr_cols_matrix);
    __nr_rows = nr_rows_matrix;
    __nr_cols = nr_cols_matrix;

    const Rational rat1(1, 1);
    const Rational ratneg1(-1, 1);

    int row = 0;

    // equation for identity row
    zero_row(row);
    __set(row, identity_triple.r, rat1); row++;

    // equation for identity column
    zero_row(row);
    __set(row, identity_triple.c + nr_rows, rat1); row++;

    // equation for identity symbol
    zero_row(row);
    __set(row, identity_triple.s + nr_rows + nr_cols, rat1);
    __set(row, nr_rows + nr_cols + nr_syms,           rat1); row++;

    for(vector<Triple>::iterator tIter = T1.begin(); tIter != T1.end(); tIter++) {
        if (tIter->r == identity_triple.r && tIter->c == identity_triple.c && tIter->s == identity_triple.s) continue;

        zero_row(row);
        __set(row, tIter->r,                     rat1);
        __set(row, tIter->c + nr_rows,           rat1);
        __set(row, tIter->s + nr_rows + nr_cols, ratneg1);

        row++;
    }

    // print_matrix();
    rref();
    
    for(int row = 0; row < __nr_rows; row++) {
        assert(get(row, row) == rat1);
        solution[row] = get(row, __nr_cols - 1);
    }

    // print_matrix();

    // printf("\n\n==============================\n\n");
}

bool is_separated_solution(vector<Rational> soln, int nr_rows, int nr_cols, int nr_syms)
{
    set<Rational> tmp;

    // Check row section
    tmp.clear();
    for(int i = 0; i < nr_rows; i++)
        tmp.insert(soln[i]);
    if (tmp.size() != (unsigned int) nr_rows)
        return false;

    // Check column section
    tmp.clear();
    for(int i = nr_rows; i < nr_rows + nr_cols; i++)
        tmp.insert(soln[i]);
    if (tmp.size() != (unsigned int) nr_cols)
        return false;

    // Check symbol section
    tmp.clear();
    for(int i = nr_rows + nr_cols; i < nr_rows + nr_cols + nr_syms; i++)
        tmp.insert(soln[i]);
    if (tmp.size() != (unsigned int) nr_syms)
        return false;

    return true;
}

QQ3 sdiv(QQ3 x, int y)
{
    return QQ3(x.a/Rational(y), x.b/Rational(y));
}

Rational triangle_size(Point pt1, Point pt2, Point pt3)
{
    /* Original docstring from Sage version of the triangle
    dissection code:

    Return one of the side lengths of a triangle
    with vertices p1, p2, p3. If the triangle degenerates, 
    that is pt1 == pt2 == pt3, then we return 0.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: triangle_size((0,0), (1,0), (0,1))
        1
        sage: triangle_size((1,0), (0,1), (0,0))
        1
        sage: triangle_size((1,1), (1,1), (1,1))
        0
    */

    // We are working with points that have not been transformed
    // into an equilateral triangle.
    assert(pt1.x.b == 0);
    assert(pt1.y.b == 0);
    assert(pt2.x.b == 0);
    assert(pt2.y.b == 0);
    assert(pt3.x.b == 0);
    assert(pt3.y.b == 0);

    if (pt1.x.a == pt2.x.a) return abs_rat(pt1.y.a - pt2.y.a);
    if (pt1.y.a == pt2.y.a) return abs_rat(pt1.x.a - pt2.x.a);

    return triangle_size(pt2, pt3, pt1);
}

// A triangle is a length 3 vector of Points.
vector<vector<Point> > triples_to_triangles(int nr_rows, int nr_cols, vector<Triple> &T2, vector<Rational> &solution)
{
    vector<vector<Point> > result;

    for(vector<Triple>::iterator tIter = T2.begin(); tIter != T2.end(); tIter++) {
        Rational w1 = solution[tIter->r];
        Rational w2 = solution[tIter->c + nr_rows];
        Rational w3 = solution[tIter->s + nr_rows + nr_cols];

        Point pt1 = {QQ3(w2,      0), QQ3(w1,      0)};
        Point pt2 = {QQ3(w2,      0), QQ3(w3 - w2, 0)};
        Point pt3 = {QQ3(w3 - w1, 0), QQ3(w1,      0)};

        Rational t_size = triangle_size(pt1, pt2, pt3);
        if (only_separated) {
            assert(t_size > Rational(0));
        } else {
            if (t_size == Rational(0)) {
                continue;
            }
        }

        set<Point> triangle_vertices_set;
        triangle_vertices_set.insert(pt1);
        triangle_vertices_set.insert(pt2);
        triangle_vertices_set.insert(pt3);

        // Remove duplicates and sort
        // http://stackoverflow.com/questions/1041620/most-efficient-way-to-erase-duplicates-and-sort-a-c-vector
        vector<Point> new_triangle;
        new_triangle.assign(triangle_vertices_set.begin(), triangle_vertices_set.end());

        result.push_back(new_triangle);
    }

    return result;
}

void print_point(Point p)
{
    printf("[");
    print_qq3(p.x);
    printf(", ");
    print_qq3(p.y);
    printf("]");
}

void transform_to_equilateral(vector<Point> &points)
{
    for(vector<Point>::iterator p = points.begin(); p != points.end(); p++) {
        // print_point(*p); printf(" -> ");
        Point new_point = {sdiv(p->y, 2) + p->x, sdiv(QQ3(0, 1)*p->y, 2)};
        *p = new_point;
        // print_point(*p); printf("\n");
    }
}

void transform_triangles_to_equilateral(vector<vector<Point> > &triangles)
{
    for(vector<vector<Point> >::iterator t = triangles.begin(); t != triangles.end(); t++) {
        assert(t->size() == 3);

        for(int i = 0; i < 3; i++) {
            Point new_point = {sdiv((*t)[i].y, 2) + (*t)[i].x, sdiv(QQ3(0, 1)*(*t)[i].y, 2)};
            (*t)[i] = new_point;
        }
    }
}

typedef struct struct_4list {
    bool operator==(const struct_4list& rhs) const
    {
        return a == rhs.a && b == rhs.b && c == rhs.c && d == rhs.d;
    }

    bool operator<(const struct_4list& rhs) const
    {
        if (a > rhs.a) return false;
        if (a < rhs.a) return true;

        if (b > rhs.b) return false;
        if (b < rhs.b) return true;

        if (c > rhs.c) return false;
        if (c < rhs.c) return true;

        if (d > rhs.d) return false;
        if (d < rhs.d) return true;
        
        return false;
    }

    Rational a;
    Rational b;
    Rational c;
    Rational d;
} flist;

flist point_to_4list(Point p)
{
    flist result = {p.x.a, p.x.b, p.y.a, p.y.b};
    return result;
}

Point rotate_equilateral(Point p)
{
   QQ3 sqrt3(0, 1);
   Point new_point = {sdiv(-sqrt3*p.y, 2) - sdiv(p.x, 2) + QQ3(1, 0), sdiv(sqrt3*p.x, 2) - sdiv(p.y, 2)};

   return new_point;
}

vector<Point> rotate_equilateral_on_triangle_points(vector<Point> triangle)
{
    vector<Point> result;

    for(vector<Point>::iterator iter = triangle.begin(); iter != triangle.end(); iter++) {
        result.push_back(rotate_equilateral(*iter));
    }

    return result;
}

Point rotate_equilateral_inverse(Point p)
{
   QQ3 sqrt3(0, 1);
   Point new_point = {sdiv(sqrt3*p.y, 2) - sdiv(p.x, 2) + QQ3(Rational(1, 2), Rational(0, 1)), sdiv(-sqrt3*p.x, 2) - sdiv(p.y, 2) + sdiv(sqrt3, 2)};

   return new_point;
}

vector<Point> rotate_equilateral_on_triangle_points_inverse(vector<Point> triangle)
{
    vector<Point> result;

    for(vector<Point>::iterator iter = triangle.begin(); iter != triangle.end(); iter++) {
        result.push_back(rotate_equilateral_inverse(*iter));
    }

    return result;
}


Point reflect1(Point p)
{
    QQ3 x0 = p.x;
    QQ3 y  = p.y;

    QQ3 x1 = x0 - QQ3(Rational(1, 2), 0);
    QQ3 x2 = QQ3(-x1.a, x1.b);
    QQ3 x3 = x2 + QQ3(Rational(1, 2), 0);

    Point result = {x3, y};
    return result;
}

vector<Point> reflect1_on_triangle(vector<Point> triangle)
{
    vector<Point> result;
    assert(triangle.size() == 3);

    for(unsigned int i = 0; i < triangle.size(); i++) {
        result.push_back(reflect1(triangle.at(i)));
    }

    return result;
}

Point reflect2(Point p)
{
    Point p2 = rotate_equilateral_inverse(p);
    Point p3 = reflect1(p2);
    Point p4 = rotate_equilateral(p3);

    return p4;
}

vector<Point> reflect2_on_triangle(vector<Point> triangle)
{
    vector<Point> result;
    assert(triangle.size() == 3);

    for(unsigned int i = 0; i < triangle.size(); i++) {
        result.push_back(reflect2(triangle.at(i)));
    }

    return result;
}

Point reflect3(Point p)
{
    Point p2 = rotate_equilateral(p);
    Point p3 = reflect1(p2);
    Point p4 = rotate_equilateral_inverse(p3);

    return p4;
}

vector<Point> reflect3_on_triangle(vector<Point> triangle)
{
    vector<Point> result;
    assert(triangle.size() == 3);

    for(unsigned int i = 0; i < triangle.size(); i++) {
        result.push_back(reflect3(triangle.at(i)));
    }

    return result;
}

vector<flist> points_to_4lists(vector<Point> pvec)
{
    vector<flist> result(pvec.size());
    transform(pvec.begin(), pvec.end(), result.begin(), point_to_4list);

    return result;
}

void print_list_of_4lists(vector<flist> lists)
{
    for(vector<flist>::iterator iter = lists.begin(); iter != lists.end(); iter++) {
        printf("[");
        print_rational(stdout, iter->a); printf(" ");
        print_rational(stdout, iter->b); printf(" ");
        print_rational(stdout, iter->c); printf(" ");
        print_rational(stdout, iter->d);
        printf("] ");
    }
    printf("\n");
}

void print_list_of_12lists(FILE *f, vector<vector<Rational> > lists)
{
    assert(f != NULL);

    for(unsigned int i = 0; i < lists.size(); i++) {
        assert(lists.at(i).size() == 12);
        for(unsigned int j = 0; j < 12; j++) {
            print_rational(f, lists.at(i).at(j)); fprintf(f, " ");
        }
    }

    fprintf(f, "\n");
}

void sort_individual_triangles(vector<vector<Point> > &triangles)
{
    for(unsigned int i = 0; i < triangles.size(); i++) {
        sort(triangles.at(i).begin(), triangles.at(i).end());
    }
}

vector<Rational> triangle_to_12list(vector<Point> triangle)
{
    vector<Rational> result;

    assert(triangle.size() == 3);

    for(unsigned int t = 0; t < 3; t++) {
        result.push_back(triangle.at(t).x.a);
        result.push_back(triangle.at(t).x.b);
        result.push_back(triangle.at(t).y.a);
        result.push_back(triangle.at(t).y.b);
    }

    return result;
}

void print_canonical_signature(vector<vector<Point> > &triangles, const char *output_prefix)
{
    const unsigned int n = triangles.size();

    if (output_files[n] == NULL) {
        char filename[1000];
        sprintf(filename, "%sout_%d", output_prefix, n);

        output_files[n] = fopen(filename, "w");
    }
    // fprintf(stderr, "%d\n", n);

    assert(output_files[n] != NULL);

    // Transform the input points to the equilateral space.
    transform_triangles_to_equilateral(triangles);

    assert(triangles.size() == n);

    vector<vector<Point> > &identity_image = triangles;
    vector<vector<Point> > rot_image(n), rot_inverse_image(n), reflect1_image(n), reflect2_image(n), reflect3_image(n);

    // Calculate the images under the group S_3.
    transform(triangles.begin(), triangles.end(), rot_image.begin(),        rotate_equilateral_on_triangle_points);
    transform(triangles.begin(), triangles.end(), rot_inverse_image.begin(),        rotate_equilateral_on_triangle_points_inverse);
    transform(triangles.begin(), triangles.end(), reflect1_image.begin(),   reflect1_on_triangle);
    transform(triangles.begin(), triangles.end(), reflect2_image.begin(),   reflect2_on_triangle);
    transform(triangles.begin(), triangles.end(), reflect3_image.begin(),   reflect3_on_triangle);

    sort_individual_triangles(identity_image);
    sort_individual_triangles(rot_image);
    sort_individual_triangles(rot_inverse_image);
    sort_individual_triangles(reflect1_image);
    sort_individual_triangles(reflect2_image);
    sort_individual_triangles(reflect3_image);

    // A point (x, y) is equivalent to a 4-tuple (xa, xb, ya, yb).
    // I want to store the whole triangle in the canonical signature, so that's going to be 3 4-tuples:
    // (x1a, x1b, y1a, y1b) (x2a, x2b, y2a, y2b) (x3a, x3b, y3a, y3b)
    //
    // A triangle is a list of 3-tuples:
    //
    // t = [(x1a, x1b, y1a, y1b) (x2a, x2b, y2a, y2b) (x3a, x3b, y3a, y3b)]
    //
    // An image is a list of these triangles:
    //
    // im = [t1, t2, t3, t4]
    //
    // So we need to convert a triangle into a 12-list

    vector<vector<Rational> > identity_image_12lists(n), rot_image_12lists(n), rot_inverse_image_12lists(n),
                              reflect1_image_12lists(n), reflect2_image_12lists(n), reflect3_image_12lists(n);

    transform(identity_image.begin(),       identity_image.end(),       identity_image_12lists.begin(),         triangle_to_12list);
    transform(rot_image.begin(),            rot_image.end(),            rot_image_12lists.begin(),              triangle_to_12list);
    transform(rot_inverse_image.begin(),    rot_inverse_image.end(),    rot_inverse_image_12lists.begin(),      triangle_to_12list);
    transform(reflect1_image.begin(),       reflect1_image.end(),       reflect1_image_12lists.begin(),         triangle_to_12list);
    transform(reflect2_image.begin(),       reflect2_image.end(),       reflect2_image_12lists.begin(),         triangle_to_12list);
    transform(reflect3_image.begin(),       reflect3_image.end(),       reflect3_image_12lists.begin(),         triangle_to_12list);


    sort(identity_image_12lists.begin(),        identity_image_12lists.end());
    sort(rot_image_12lists.begin(),             rot_image_12lists.end());
    sort(rot_inverse_image_12lists.begin(),     rot_inverse_image_12lists.end());
    sort(reflect1_image_12lists.begin(),        reflect1_image_12lists.end());
    sort(reflect2_image_12lists.begin(),        reflect2_image_12lists.end());
    sort(reflect3_image_12lists.begin(),        reflect3_image_12lists.end());

    // Choose the lexicographically minimal signature.
    vector<vector<vector<Rational> > > all_images;
    all_images.push_back(identity_image_12lists);
    all_images.push_back(rot_image_12lists);
    all_images.push_back(rot_inverse_image_12lists);
    all_images.push_back(reflect1_image_12lists);
    all_images.push_back(reflect2_image_12lists);
    all_images.push_back(reflect3_image_12lists);

    sort(all_images.begin(), all_images.end());

    assert(output_files[n] != NULL);
    print_list_of_12lists(output_files[n], all_images[0]);
}

int main(int argc, const char* argv[])
{
    if (argc != 3) {
        fprintf(stderr, "Usage: just the separated dissections: td --separated <prefix>\nseparated and nonseparated dissections: td --separated-and-nonseparated <prefix>\n\n");
        exit(1);
    }

    const char *sep_or_nonsep = argv[1];
    const char *output_prefix = argv[2];

    if (strcmp(sep_or_nonsep, "--separated") == 0) {
       only_separated = true;
    } else if (strcmp(sep_or_nonsep, "--separated-and-nonseparated") == 0) {
       only_separated = false;
    } else {
        fprintf(stderr, "Usage: just the separated dissections: td --separated <prefix>\nseparated and nonseparated dissections: td --separated-and-nonseparated <prefix>\n\n");
        exit(1);
    }

    for(int i = 0; i <= MAX_OUTPUT_NR; i++)
        output_files[i] = NULL;

    int nr_rows, nr_cols, nr_syms, nr_elements;
    vector<Triple> T1, T2;

    while(read_bitrade(nr_rows, nr_cols, nr_syms, nr_elements, T1, T2)) {
        // printf("%d %d %d %d\n", nr_rows, nr_cols, nr_syms, nr_elements);

        for(vector<Triple>::iterator tIter = T1.begin(); tIter != T1.end(); tIter++) {
            vector<Rational> solution(3 + T1.size() - 1);
            calculate_bitrade_solution(nr_rows, nr_cols, nr_syms, *tIter, T1, T2, solution);
            if (only_separated && !is_separated_solution(solution, nr_rows, nr_cols, nr_syms)) continue;

            #if 0
            printf("solution: ");
            for(vector<Rational>::iterator ratIter = solution.begin(); ratIter != solution.end(); ratIter++) {
                print_rational(*ratIter); printf(" ");
            }
            printf("\n");
            #endif

            vector<vector<Point> > triangles = triples_to_triangles(nr_rows, nr_cols, T2, solution);

            #if 0
            transform_to_equilateral(points);
            printf("points from solution: ");
            for(vector<Point>::iterator pIter = points.begin(); pIter != points.end(); pIter++) {
                print_point(*pIter); printf(" ");
            }
            printf("\n");
            #endif

            print_canonical_signature(triangles, output_prefix);
        }

        for(vector<Triple>::iterator tIter = T2.begin(); tIter != T2.end(); tIter++) {
            vector<Rational> solution(3 + T2.size() - 1);
            calculate_bitrade_solution(nr_rows, nr_cols, nr_syms, *tIter, T2, T1, solution);
            if (only_separated && !is_separated_solution(solution, nr_rows, nr_cols, nr_syms)) continue;

            #if 0
            printf("solution: ");
            for(vector<Rational>::iterator ratIter = solution.begin(); ratIter != solution.end(); ratIter++) {
                print_rational(*ratIter); printf(" ");
            }
            printf("\n");
            #endif

            vector<vector<Point> > triangles = triples_to_triangles(nr_rows, nr_cols, T1, solution);

            #if 0
            transform_to_equilateral(points);
            printf("points from solution: ");
            for(vector<Point>::iterator pIter = points.begin(); pIter != points.end(); pIter++) {
                print_point(*pIter); printf(" ");
            }
            printf("\n");
            #endif
           
            print_canonical_signature(triangles, output_prefix);
        }
    }

    return 0;
}




