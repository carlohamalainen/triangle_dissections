#ifndef __RATLIB__
#define __RATLIB__

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <set>
#include <vector>

#include <cstring>

#include <boost/algorithm/string.hpp>
#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

#include <math.h>

using namespace std;

int gcd(int u, int v);

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

Rational abs_rat(const Rational &other)
{
    Rational result;

    result.numerator   = abs(other.numerator);
    result.denominator = abs(other.denominator);

    return result;
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

QQ3 operator-(const QQ3 &other);

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


int gcd(int u, int v);
void print_rational(FILE *f, Rational x);

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

 
int lcm(int m, int n)
{
    return m/gcd(m, n)*n;
}

int lcm(vector<int> v)
{
    assert(v.size() > 0);

    if (v.size() == 1) return v.at(0);

    if (v.size() == 2) return lcm(v.at(0), v.at(1));

    int tmp = lcm(v.at(0), v.at(1));

    for(unsigned int i = 2; i < v.size(); i++)
        tmp = lcm(tmp, v.at(i));

    return tmp;
}


// Pretty-print a rational number, shortening the
// output if x == 0 or x is an integer.
void print_rational(FILE *f, Rational x)
{
    if (x.numerator == 0)
        fprintf(f, "%d", 0);
    else if (x.denominator == 1)
        fprintf(f, "%d", x.numerator);
    else
        fprintf(f, "%d/%d", x.numerator, x.denominator);
}

QQ3 operator-(const QQ3 &other)
{
    QQ3 neg(-other.a, -other.b);
    return neg;
}

void print_qq3(QQ3 q)
{
    printf("(");
    print_rational(stdout, q.a);
    printf(" + ");
    print_rational(stdout, q.b);
    printf("*sqrt(3)");
}


// "3/4" -> Rational(3, 4)
Rational parse_rational(string s)
{
    std::vector<std::string> strs;
    boost::split(strs, s, boost::is_any_of("/"));

    assert(strs.size() == 1 || strs.size() == 2);

    int n, d;

    if (strs.size() == 1) {
        std::istringstream numerator(strs.at(0));

        numerator >> n;
        d = 1;
    } else if (strs.size() == 2) {
        std::istringstream numerator(strs.at(0));
        std::istringstream denominator(strs.at(1));

        numerator >> n;
        denominator >> d;
    } else {
        assert(false);
    }

    return Rational(n, d);
}

double rational_to_double(Rational &r)
{
    return 1.0*r.numerator/r.denominator;
}

double qq3_to_double(QQ3 &q)
{
    return rational_to_double(q.a) + rational_to_double(q.b)*sqrt(3);
}

// uhh, these should be operators!
bool qq3_lt(QQ3 q0, QQ3 q1)
{
    return qq3_to_double(q0) < qq3_to_double(q1);
}

bool qq3_gt(QQ3 q0, QQ3 q1)
{
    return qq3_to_double(q0) > qq3_to_double(q1);
}



#endif

