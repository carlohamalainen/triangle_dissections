#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <set>
#include <vector>

using namespace std;

int gcd(int u, int v)
{
    int t;
    while (v) {
        t = u; 
        u = v; 
        v = t % v;
    }
    if (u < 0) u *= -1;

    return u;
}

class Rational
{
    // Keep the negative number in the numerator and cancel out
    // any double negatives.
    void fix_signs()
    {
        if (this->numerator < 0 && this->denominator < 0) {
            this->numerator   *= -1;
            this->denominator *= -1;
        }
        else if (this->numerator >= 0 && this->denominator <  0) {
            this->numerator   *= -1;
            this->denominator *= -1;
        }
        else if (this->numerator <  0 && this->denominator >= 0) {
            // this is ok; do nothing 
        }
        else {
            assert(this->numerator   >= 0);
            assert(this->denominator >= 0);
        }
    }

    public:
    
    int numerator, denominator;

    Rational() {
        ;
    }

    Rational(int numerator) {
        this->numerator = numerator;
        this->denominator = 1;
    }

    Rational(int numerator, int denominator) {
        this->numerator = numerator;
        this->denominator = denominator;
    }

    Rational& operator=(const Rational &rhs) {
        this->numerator = rhs.numerator;
        this->denominator = rhs.denominator;
        return *this;
    }

    friend Rational operator-(const Rational &other);

    const Rational operator+(const Rational &right) const {
        Rational sum;
        Rational left = *this;
        int k, m1, m2;

        k = gcd(left.denominator, right.denominator);
        m1 = left.denominator/k;
        m2 = right.denominator/k;

        sum.numerator   = left.numerator*m2 + right.numerator*m1;
        sum.denominator = left.denominator*m2;

        sum.fix_signs();

        k = gcd(sum.numerator, sum.denominator);
        sum.numerator   /= k;
        sum.denominator /= k;

        return sum;
    }

    const Rational operator*(const Rational &right) const {
        Rational prod;
        int k;

        prod.numerator   = this->numerator   * right.numerator;
        prod.denominator = this->denominator * right.denominator;

        prod.fix_signs();

        k = gcd(prod.numerator, prod.denominator);
        prod.numerator   /= k;
        prod.denominator /= k;

        return prod;
    }

    const Rational operator/(const Rational &right) const {
        int k;
        Rational result;

        result.numerator   = this->numerator   * right.denominator;
        result.denominator = this->denominator * right.numerator;

        result.fix_signs();

        k = gcd(result.numerator, result.denominator);
        result.numerator   /= k;
        result.denominator /= k;

        return result;
    }

    const Rational operator-(const Rational &right) const {
        return *this + (-right);
    }

    bool operator==(const Rational &other) const {
        return this->numerator == other.numerator && this->denominator == other.denominator;
    }

    bool operator!=(const Rational &other) const {
        return !(*this == other);
    }

    bool operator<(const Rational &other) const {
        return ((double) this->numerator)/((double) this->denominator) < ((double) other.numerator)/((double) other.denominator);
    }

    bool operator>(const Rational &other) const {
        return ((double) this->numerator)/((double) this->denominator) > ((double) other.numerator)/((double) other.denominator);
    }
};

Rational operator-(const Rational &other)
{
    Rational neg;
    neg.numerator = -other.numerator;
    neg.denominator = other.denominator;
    return neg;
}

class QQ3
{
    public:
    
    Rational a, b;

    QQ3() {
        ;
    }

    QQ3(Rational a, Rational b) {
        this->a = a;
        this->b = b;
    }

    QQ3& operator=(const QQ3 &rhs) {
        this->a = rhs.a;
        this->b = rhs.b;
        return *this;
    }

    friend QQ3 operator-(const QQ3 &other);

    const QQ3 operator+(const QQ3 &right) const {
        return QQ3(this->a + right.a, this->b + right.b);
    }

    const QQ3 operator-(const QQ3 &right) const {
        return *this + (-right);
    }

    const QQ3 operator*(const QQ3 &y) const {
        return QQ3(this->a*y.a + Rational(3)*this->b*y.b, this->a*y.b + this->b*y.a);
    }

    bool operator==(const QQ3 &other) const {
        return this->a == other.a && this->b == other.b;
    }

    bool operator!=(const QQ3 &other) const {
        return !(*this == other);
    }

    bool operator<(const QQ3 &other) const {
        if (this->a < other.a)
            return true;
        
        if (this->a == other.a && this->b < other.b)
            return true;

        return false;
    }
};

QQ3 operator-(const QQ3 &other)
{
    QQ3 neg(-other.a, -other.b);
    return neg;
}

#if 0
// Performs the division left/right.
Rational rat_div(Rational left, Rational right)
{
    int k;
    Rational result;

    result.numerator   = left.numerator   * right.denominator;
    result.denominator = left.denominator * right.numerator;

    fix_signs(&result);

    k = gcd(result.numerator, result.denominator);
    result.numerator   /= k;
    result.denominator /= k;

    return result;
}

#endif

// Pretty-print a rational number, shortening the
// output if x == 0 or x is an integer.
void print_rational(Rational x)
{
    if (x.numerator == 0)
        printf("%d", 0);
    else if (x.denominator == 1)
        printf("%d", x.numerator);
    else
        printf("%d/%d", x.numerator, x.denominator);
}

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
            print_rational(get(r, c)); printf(" ");
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

void blah(int nr_rows, int nr_cols, int nr_syms, Triple identity_triple, vector<Triple> &T1, vector<Triple> &T2, vector<Rational> &solution)
{
    const int nr_rows_matrix = 3 + T1.size() - 1; //  3 identity equations, |T1|-1 element equations
    const int nr_cols_matrix = nr_rows + nr_cols + nr_syms + 1;

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

typedef struct struct_point {
    bool operator<(const struct_point& rhs) const
    {
        if (x < rhs.x)
            return true;

        if (x == rhs.x && y < rhs.y)
            return true;

        return false;
    }

    QQ3 x, y;
} Point;

QQ3 sdiv(QQ3 x, int y)
{
    return QQ3(x.a/Rational(y), x.b/Rational(y));
}

void print_qq3(QQ3 q)
{
    printf("(");
    print_rational(q.a);
    printf(" + ");
    print_rational(q.b);
    printf("*sqrt(3)");
}

vector<Point> triples_to_points(int nr_rows, int nr_cols, vector<Triple> &T2, vector<Rational> &solution)
{
    vector<Point> result;

    for(vector<Triple>::iterator tIter = T2.begin(); tIter != T2.end(); tIter++) {
        Rational w1 = solution[tIter->r];
        Rational w2 = solution[tIter->c + nr_rows];
        Rational w3 = solution[tIter->s + nr_rows + nr_cols];

        Point pt1 = {QQ3(w2,      0), QQ3(w1,      0)};
        Point pt2 = {QQ3(w2,      0), QQ3(w3 - w2, 0)};
        Point pt3 = {QQ3(w3 - w1, 0), QQ3(w1,      0)};

        result.push_back(pt1);
        result.push_back(pt2);
        result.push_back(pt3);
    }

    // Remove duplicates and sort
    // http://stackoverflow.com/questions/1041620/most-efficient-way-to-erase-duplicates-and-sort-a-c-vector
    set<Point> s(result.begin(), result.end());
    result.assign(s.begin(), s.end());

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

Point rotate_equilateral_inverse(Point p)
{
   QQ3 sqrt3(0, 1);
   Point new_point = {sdiv(sqrt3*p.y, 2) - sdiv(p.x, 2) + QQ3(Rational(1, 2), Rational(0, 1)), sdiv(-sqrt3*p.x, 2) - sdiv(p.y, 2) + sdiv(sqrt3, 2)};

   return new_point;
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

Point reflect2(Point p)
{
    Point p2 = rotate_equilateral_inverse(p);
    Point p3 = reflect1(p2);
    Point p4 = rotate_equilateral(p3);

    return p4;
}

Point reflect3(Point p)
{
    Point p2 = rotate_equilateral(p);
    Point p3 = reflect1(p2);
    Point p4 = rotate_equilateral_inverse(p3);

    return p4;
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
        print_rational(iter->a); printf(" ");
        print_rational(iter->b); printf(" ");
        print_rational(iter->c); printf(" ");
        print_rational(iter->d);
        printf("] ");
    }
    printf("\n");
}

void towards_csig(vector<Point> &points)
{
    const unsigned int n = points.size();

    // Transform the input points to the equilateral space.
    transform_to_equilateral(points);

    vector<Point> &identity_image = points;
    vector<Point> rot_image(n), rot_inverse_image(n), reflect1_image(n), reflect2_image(n), reflect3_image(n);

    // Calculate the images under the group S_3.
    transform(points.begin(), points.end(), rot_image.begin(),          rotate_equilateral);
    transform(points.begin(), points.end(), rot_inverse_image.begin(),  rotate_equilateral_inverse);
    transform(points.begin(), points.end(), reflect1_image.begin(),     reflect1);
    transform(points.begin(), points.end(), reflect2_image.begin(),     reflect2);
    transform(points.begin(), points.end(), reflect3_image.begin(),     reflect3);

    // Convert these into lists of 4-tuples.
    vector<flist> identity_image_4lists       = points_to_4lists(identity_image);
    vector<flist> rot_image_4lists            = points_to_4lists(rot_image);
    vector<flist> rot_inverse_image_4lists    = points_to_4lists(rot_inverse_image);
    vector<flist> reflect1_image_4lists       = points_to_4lists(reflect1_image);
    vector<flist> reflect2_image_4lists       = points_to_4lists(reflect2_image);
    vector<flist> reflect3_image_4lists       = points_to_4lists(reflect3_image);

    // Sort these 4-tuples.
    sort(identity_image_4lists.begin(),     identity_image_4lists.end());
    sort(rot_image_4lists.begin(),          rot_image_4lists.end());
    sort(rot_inverse_image_4lists.begin(),  rot_inverse_image_4lists.end());
    sort(reflect1_image_4lists.begin(),     reflect1_image_4lists.end());
    sort(reflect2_image_4lists.begin(),     reflect2_image_4lists.end());
    sort(reflect3_image_4lists.begin(),     reflect3_image_4lists.end());

    // Choose the lexicographically minimal signature.
    // print_list_of_4lists(identity_image_4lists);
    // print_list_of_4lists(rot_image_4lists);
    // print_list_of_4lists(rot_inverse_image_4lists);
    // print_list_of_4lists(reflect1_image_4lists);
    // print_list_of_4lists(reflect2_image_4lists);
    // print_list_of_4lists(reflect3_image_4lists);
    vector<vector<flist> > all_images;
    all_images.push_back(identity_image_4lists);
    all_images.push_back(rot_image_4lists);
    all_images.push_back(rot_inverse_image_4lists);
    all_images.push_back(reflect1_image_4lists);
    all_images.push_back(reflect2_image_4lists);
    all_images.push_back(reflect3_image_4lists);

    sort(all_images.begin(), all_images.end());
    print_list_of_4lists(all_images[0]);
}

int main()
{
    int nr_rows, nr_cols, nr_syms, nr_elements;
    vector<Triple> T1, T2;

    while(read_bitrade(nr_rows, nr_cols, nr_syms, nr_elements, T1, T2)) {
        // printf("%d %d %d %d\n", nr_rows, nr_cols, nr_syms, nr_elements);

        for(vector<Triple>::iterator tIter = T1.begin(); tIter != T1.end(); tIter++) {
            vector<Rational> solution(3 + T1.size() - 1);
            blah(nr_rows, nr_cols, nr_syms, *tIter, T1, T2, solution);
            if (!is_separated_solution(solution, nr_rows, nr_cols, nr_syms)) continue;

            #if 0
            printf("solution: ");
            for(vector<Rational>::iterator ratIter = solution.begin(); ratIter != solution.end(); ratIter++) {
                print_rational(*ratIter); printf(" ");
            }
            printf("\n");
            #endif

            vector<Point> points = triples_to_points(nr_rows, nr_cols, T2, solution);
            #if 0
            transform_to_equilateral(points);
            printf("points from solution: ");
            for(vector<Point>::iterator pIter = points.begin(); pIter != points.end(); pIter++) {
                print_point(*pIter); printf(" ");
            }
            printf("\n");
            #endif
            towards_csig(points);
        }

        for(vector<Triple>::iterator tIter = T2.begin(); tIter != T2.end(); tIter++) {
            vector<Rational> solution(3 + T2.size() - 1);
            blah(nr_rows, nr_cols, nr_syms, *tIter, T2, T1, solution);
            if (!is_separated_solution(solution, nr_rows, nr_cols, nr_syms)) continue;

            #if 0
            printf("solution: ");
            for(vector<Rational>::iterator ratIter = solution.begin(); ratIter != solution.end(); ratIter++) {
                print_rational(*ratIter); printf(" ");
            }
            printf("\n");
            #endif

            vector<Point> points = triples_to_points(nr_rows, nr_cols, T1, solution);
            #if 0
            transform_to_equilateral(points);
            printf("points from solution: ");
            for(vector<Point>::iterator pIter = points.begin(); pIter != points.end(); pIter++) {
                print_point(*pIter); printf(" ");
            }
            printf("\n");
            #endif
            towards_csig(points);
        }
    }

    return 0;
}




