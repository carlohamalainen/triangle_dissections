#include <map>
#include "csig.h"
#include "ratlib.h"

using namespace std;

void isomer_signature(vector<vector<Point> > &triangles, vector<int> &iso_sig)
{
    // The dissections are presented with side y = 0 along the interval [0, 1]. Compute the
    // size of this triangle dissection if each sub-triangle has integer side length. We can use
    // this as a multiplicative factor to work out the size of any sub-triangle.
    const int size_of_dissection = size_of_outer_triangle(triangles);

    iso_sig.clear();

    // For each triangle in this dissection...
    for(unsigned int i = 0; i < triangles.size(); i++) {
        iso_sig.push_back(size_of_triangle(triangles.at(i), size_of_dissection));
    }

    sort(iso_sig.begin(), iso_sig.end());
}

int main()
{
    std::string line;

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);

        vector<int> iso_sig;
        isomer_signature(triangles, iso_sig);

        for(vector<int>::iterator v_iter = iso_sig.begin(); v_iter != iso_sig.end(); v_iter++) {
            std::cout << *v_iter << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}

