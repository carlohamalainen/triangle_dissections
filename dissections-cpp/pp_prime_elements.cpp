/*

    FIXME

*/

#include <stdlib.h>
#include <math.h>
#include <map>
#include "td.h"
#include "ratlib.h"

#define MAX_PRIME 10000

using namespace std;

// Very basic Sieve of Eratosthenes, taken from
// http://rosettacode.org/wiki/Sieve_of_Eratosthenes#C 
char* eratosthenes (int n, int *c)
{
  char* sieve;
  int i, j, m;
 
  *c = n-1;     /* primes count */
 
  /* calloc initializes to zero */
  sieve = (char *) calloc (n+1, sizeof(char));
  m = (int) sqrt ((double) n);
  sieve[0] = 1;
  sieve[1] = 1;
  for (i = 2; i <= m; i++) {
    if (sieve[i] == 0) {
      for (j = i*i; j <= n; j += i) {
        if (sieve[j] == 0) {
          sieve[j] = 1; 
          --(*c);
        }
      }
    }
  }
  return sieve;
}

char *__sieve;

void init_primes_list()
{
    int prime_count = 0;

    __sieve = eratosthenes(MAX_PRIME + 1, &prime_count);
}

bool is_prime(int n)
{
    assert(n <= MAX_PRIME);

    return __sieve[n] == 0;
}


void update_prime_counts(vector<vector<Point> > &triangles, std::map<unsigned long long, unsigned long long> &prime_counts, unsigned long long &max_prime)
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
        if (is_prime(i) && seen_sizes.at(i)) {
            if (prime_counts.find(i) == prime_counts.end())
                prime_counts[i] = 0;

            prime_counts.at(i) += 1;

            if ((unsigned long long) i > max_prime) max_prime = i;
        }
    }
}

int main()
{
    init_primes_list();

    std::string line;

    unsigned long long max_prime = 0;
    std::map<unsigned long long, unsigned long long> prime_counts;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
        update_prime_counts(triangles, prime_counts, max_prime);
    }

    for(unsigned long long p = 2; p <= max_prime; p++) {
        if (!is_prime(p)) continue;

        unsigned long long nr = -1;

        if (prime_counts.find(p) == prime_counts.end())
            nr = 0;
        else
            nr = prime_counts.at(p);

        printf("%llu %llu\n", p, nr);
    }

    return 0;
}


