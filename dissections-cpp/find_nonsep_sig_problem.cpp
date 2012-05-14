#include <stdio.h>

#include <map>
#include <set>
#include <vector>
#include <boost/algorithm/string.hpp>

#include <iostream>
using namespace std;

int main()
{
    map<vector<string>, vector<string> > sig_map;

    string line;

    while(cin.good()) {
        getline(cin, line);
        boost::trim(line);

        vector<string> strs;
        boost::split(strs, line, boost::is_any_of(" "));

        if (strs.size() == 1) {
            // hit the end of the file
            break;
        }

        assert(strs.size() % 12 == 0);
        assert(strs.size() %  4 == 0);

        vector<string> points;

        for(unsigned int i = 0; i < strs.size()/4; i++) {
            string p = strs.at(4*i + 0) + "_"
                     + strs.at(4*i + 1) + "_"
                     + strs.at(4*i + 2) + "_"
                     + strs.at(4*i + 3);
            points.push_back(p);
        }

        // Remove duplicates and sort
        // http://stackoverflow.com/questions/1041620/most-efficient-way-to-erase-duplicates-and-sort-a-c-vector
        set<string> s(points.begin(), points.end() );
        vector<string> unique_points;
        unique_points.assign(s.begin(), s.end());

        #if 0
        cout << "zzz ";
        for(unsigned int i = 0; i < unique_points.size(); i++) {
            cout << unique_points.at(i) << " ";
        }
        cout << endl;
        #endif

        if (sig_map.find(unique_points) != sig_map.end()) {
            sig_map[unique_points].push_back(line);
        } else {
            vector<string> v;
            v.push_back(line);
            sig_map[unique_points] = v;
        }
    }

    for(map<vector<string>, vector<string> >::iterator iter = sig_map.begin(); iter != sig_map.end(); iter++) {
        vector<string> csig = iter->first;

        for(vector<string>::iterator siter = csig.begin(); siter != csig.end(); siter++) {
            cout << *siter << " ";
        }
        cout << endl;
    }

    // print one line of each
    #if 0
    for(map<vector<string>, vector<string> >::iterator iter = sig_map.begin(); iter != sig_map.end(); iter++) {
        vector<string> original_lines = iter->second;

        for(vector<string>::iterator siter = original_lines.begin(); siter != original_lines.end(); siter++) {
            cout << *siter << " " << endl; // need a trailing space to compare against the main enumeration code
            break;
        }
    }
    #endif

    #if 0
    for(map<vector<string>, vector<string> >::iterator iter = sig_map.begin(); iter != sig_map.end(); iter++) {
        if (iter->second.size() > 1) {
            vector<string> original_lines = iter->second;

            cout << "nr in this set: " << iter->second.size() << endl;

            for(vector<string>::iterator siter = original_lines.begin(); siter != original_lines.end(); siter++) {
                cout << *siter << endl;
            }
        }
    }
    #endif

    return 0;
}




