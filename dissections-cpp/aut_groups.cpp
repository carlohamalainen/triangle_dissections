#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <set>
#include <vector>

#include <cstring>

#include <time.h>

#include "ratlib.h"
#include "td.h"

using namespace std;

bool compare_point_lists(vector<vector<Point> > &a, vector<vector<Point> > &b)
{
    if (a.size() != b.size())
        return false;

    for(unsigned long long i = 0; i < a.size(); i++) {
        assert(a.at(i).size() == 3);
        assert(b.at(i).size() == 3);

        for(unsigned long long j = 0; j < a.at(i).size(); j++) {
            if (a.at(i).at(j) != b.at(i).at(j))
                return false;
        }
    }

    return true;
}


int aut_group_size(vector<vector<Point> > &triangles)
{
    const unsigned int n = triangles.size();
    
    vector<vector<Point> > &identity_image = triangles;
    vector<vector<Point> > rot_image(n), rot_inverse_image(n), reflect1_image(n), reflect2_image(n), reflect3_image(n);

    // Calculate the images under the group S_3.
    transform(triangles.begin(), triangles.end(), rot_image.begin(),            rotate_equilateral_on_triangle_points);
    transform(triangles.begin(), triangles.end(), rot_inverse_image.begin(),    rotate_equilateral_on_triangle_points_inverse);
    transform(triangles.begin(), triangles.end(), reflect1_image.begin(),       reflect1_on_triangle);
    transform(triangles.begin(), triangles.end(), reflect2_image.begin(),       reflect2_on_triangle);
    transform(triangles.begin(), triangles.end(), reflect3_image.begin(),       reflect3_on_triangle);

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




    int aut_size = 1; // there is always the identity

    // if (compare_point_lists(reflect1_image,     identity_image))    aut_size += 1;
    // if (compare_point_lists(reflect2_image,     identity_image))    aut_size += 1;
    // if (compare_point_lists(reflect3_image,     identity_image))    aut_size += 1;
    // if (compare_point_lists(rot_image,          identity_image))    aut_size += 1;
    // if (compare_point_lists(rot_inverse_image,  identity_image))    aut_size += 1;

    if (rot_image_12lists               == identity_image_12lists)  aut_size += 1;
    if (rot_inverse_image_12lists       == identity_image_12lists)  aut_size += 1;
    if (reflect1_image_12lists          == identity_image_12lists)  aut_size += 1;
    if (reflect2_image_12lists          == identity_image_12lists)  aut_size += 1;
    if (reflect3_image_12lists          == identity_image_12lists)  aut_size += 1;

    assert(aut_size == 1 || aut_size == 2 || aut_size == 3 || aut_size == 6); // yay group theory

    return aut_size;
}

#define nr_dissections_24 297894288

int main()
{
#ifdef SIZE_24_STATUS_OUTPUT
    time_t t_start, t_end;
#endif

    std::string line;

    unsigned long long aut_group_size_counts[7];
    aut_group_size_counts[1] = 0;
    aut_group_size_counts[2] = 0;
    aut_group_size_counts[3] = 0;
    aut_group_size_counts[6] = 0;

#ifdef SIZE_24_STATUS_OUTPUT
    unsigned long long counter = 0;
    time(&t_start);
#endif

    while (getline(cin, line)) {
        vector<vector<Point> > triangles = parse_csig_line(line);
        aut_group_size_counts[aut_group_size(triangles)] += 1;

#ifdef SIZE_24_STATUS_OUTPUT
        counter++;

        if (counter == 10000) {
            time(&t_end);

            double nr_processed = aut_group_size_counts[1] + aut_group_size_counts[2] + aut_group_size_counts[3] + aut_group_size_counts[6];
            double nr_to_go = nr_dissections_24 - nr_processed;
            double seconds_per_10000 = difftime(t_end, t_start);

            double hours_to_go = nr_to_go/10000*seconds_per_10000/60.0/60.0;
            double days_to_go  = hours_to_go/24;

            cout << "# " << hours_to_go << " hours to go (" << days_to_go << " days)" << " :: " \
                << aut_group_size_counts[1] << " " << aut_group_size_counts[2] << " " << aut_group_size_counts[3] << " " << aut_group_size_counts[6] << std::endl;

            counter = 0;
            time(&t_start);
        }
#endif
    }

    cout << aut_group_size_counts[1] << " " << aut_group_size_counts[2] << " " << aut_group_size_counts[3] << " " << aut_group_size_counts[6] << std::endl;

    return 0;
}

