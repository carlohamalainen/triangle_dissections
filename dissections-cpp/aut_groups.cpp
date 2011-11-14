#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <set>
#include <vector>

#include <cstring>

#include "ratlib.h"
#include "td.h"

using namespace std;

int main()
{
    std::string line;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
    }

    return 0;
}

