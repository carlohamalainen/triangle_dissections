//*****************************************************************************
//       Copyright (C) 2009 Carlo Hamalainen <carlo.hamalainen@gmail.com>,
//
//  Distributed under the terms of the GNU General Public License (GPL)
//
//    This code is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    General Public License for more details.
//
//  The full text of the GPL is available at:
//
//                  http://www.gnu.org/licenses/
//*****************************************************************************

/* 
Compile with 

    gcc -o spherical_bitrades_binary -O2 '-DPLUGIN="spherical_bitrades.c"' plantri.c

Run with

    ./spherical_bitrades_binary -b -u 6

to get a spherical bitrade on 6 vertices, with 6 - 2 = 4 entries. In general

    ./spherical_bitrades_binary -b -u n

will give a bitrade (T1, T2) where |T1| = n - 2.

To inspect the output, use od. For example:

$ od -t u1 binary_spherical_bitrades_4 
0000000   2   2   2   4   0   0   0   0   1   1   1   1   0   1   0   1
0000020   0   0   1   0   1   0   1   0   0   1   1   1
0000034

*/

#include <assert.h>

static int make_dual();

#define FILTER bitrade_filter

typedef struct triple_rec
{
    int x, y, z;
} triple;


// global for 3-colouring the vertices of the graph.
int *vertex_colour;
// global for labelling the rows, columns, and symbols on the 
// set {0, 1, ...}
int *row_label;
int *col_label;
int *sym_label;
int max_row_label, max_col_label, max_sym_label;
triple *T1, *T2;
int max_entry_index1, max_entry_index2;

void write_integer(int i)
{
    // To save space, write out unsigned chars instead of full ints.
    assert(i >= 0);
    assert(i < 256);
    assert(fwrite(&i, sizeof(unsigned char), 1, stdout) == 1);

    // assert(fwrite(&i, sizeof(int), 1, stdout) == 1);
}

void vertices_of_face(int i, int *v1, int *v2, int *v3)
{
    *v1 = facestart[i]->start;
    *v2 = facestart[i]->end;
    *v3 = facestart[i]->invers->prev->end;
}

int other_colour(int c1, int c2)
{
    int x;

    if (c1 > c2) {
        x = c1;
        c1 = c2;
        c2 = x;
    }

    if (c1 == 0 && c2 == 1) return 2;
    if (c1 == 0 && c2 == 2) return 1;
    if (c1 == 1 && c2 == 2) return 0;

    assert(FALSE);
}

void ordered_triple(int v1, int v2, int v3, int *r, int *c, int *s)
{
    int x[3];

    x[vertex_colour[v1]] = v1;
    x[vertex_colour[v2]] = v2;
    x[vertex_colour[v3]] = v3;

    *r = x[0];
    *c = x[1];
    *s = x[2];
}

void walk_faces(int i, int face_colour)
{
    int r, c, s;
    int v1, v2, v3;
    int a1, a2, a3;

    vertices_of_face(i, &v1, &v2, &v3);

    // If we have already visited this face then there
    // is nothing to do here so leave.
    if (ISMARKED(facestart[i])) return;

    // Otherwise we tag this face and recurse on the 
    // three neighbours.
    MARKLO(facestart[i]);
    // printf("marking face %d\n", i);

    // If all three vertices of this face are uncoloured
    // then we are entering walk_faces for for the first time
    // so we arbitrarily 3-colour the vertices of this face.
    if (vertex_colour[v1] < 0 && vertex_colour[v2] < 0 && vertex_colour[v3] < 0) {
        vertex_colour[v1] = 0;
        vertex_colour[v2] = 1;
        vertex_colour[v3] = 2;
    } else if (vertex_colour[v1] >= 0 && vertex_colour[v2] >= 0 && vertex_colour[v3] >= 0) {
        // Terminating case, do nothing.
    } else {
        // Two vertices must be coloured so we can colour the third.
        if (vertex_colour[v1] >= 0 && vertex_colour[v2] >= 0) {
            assert(vertex_colour[v3] < 0);
            vertex_colour[v3] = other_colour(vertex_colour[v1], vertex_colour[v2]);
        } else if (vertex_colour[v1] >= 0 && vertex_colour[v3] >= 0) {
            assert(vertex_colour[v2] < 0);
            vertex_colour[v2] = other_colour(vertex_colour[v1], vertex_colour[v3]);
        } else if (vertex_colour[v2] >= 0 && vertex_colour[v3] >= 0) {
            assert(vertex_colour[v1] < 0);
            vertex_colour[v1] = other_colour(vertex_colour[v2], vertex_colour[v3]);
        } else {
	    printf("%d, %d, %d\n", vertex_colour[v1], vertex_colour[v2], vertex_colour[v3]);
            assert(FALSE);
        }
    }

    ordered_triple(v1, v2, v3, &r, &c, &s);

    // Have we seen the row label r before? If not, make a note of how
    // we will really present it.
    if (row_label[r] < 0) {
        row_label[r] = max_row_label;
        max_row_label++;
    } 
    if (col_label[c] < 0) {
        col_label[c] = max_col_label;
        max_col_label++;
    } 
    if (sym_label[s] < 0) {
        sym_label[s] = max_sym_label;
        max_sym_label++;
    } 

    triple e;
    e.x = row_label[r];
    e.y = col_label[c];
    e.z = sym_label[s];

    if (face_colour == 0) {
        T1[max_entry_index1] = e;
        max_entry_index1++;
    } else { // face_colour == 1
        T2[max_entry_index2] = e;
        max_entry_index2++;
    }

    // tags of the three adjacent faces
    a1 = facestart[i]->invers->tag;
    a2 = facestart[i]->invers->prev->invers->tag;
    a3 = facestart[i]->invers->prev->invers->prev->invers->tag;

    if (face_colour == 0)   face_colour = 1;
    else                    face_colour = 0;

    walk_faces(a1, face_colour);
    walk_faces(a2, face_colour);
    walk_faces(a3, face_colour);
}

static int
bitrade_filter(int nbtot, int nbop, int doflip)
{
    // int v1, v2, v3;
    int nf;
    register int i;
    // EDGE *e,*elast;

    nf = make_dual();

    RESETMARKS;

    for(i = 0; i < nf; ++i) {
        // Tag the three edges in this clockwise face:
        facestart[i]->tag = i;
        facestart[i]->invers->prev->tag = i;
        facestart[i]->invers->prev->invers->prev->tag = i;
    }

    // fixme not checking if malloc succeeded
    vertex_colour = (int *) malloc(sizeof(int)*nv);

    row_label = (int *) malloc(sizeof(int)*nf);
    col_label = (int *) malloc(sizeof(int)*nf);
    sym_label = (int *) malloc(sizeof(int)*nf);

    T1 = (triple *) malloc(sizeof(triple)*(nv-2));
    T2 = (triple *) malloc(sizeof(triple)*(nv-2));

    max_row_label = max_col_label = max_sym_label = 0;
    max_entry_index1 = max_entry_index2 = 0;

    for (i = 0; i < nv; ++i) {
        vertex_colour[i] = -1;
        row_label[i] = -1;
        col_label[i] = -1;
        sym_label[i] = -1;
    }

    walk_faces(0, 0);

    // printf("%d %d %d\n", max_row_label, max_col_label, max_sym_label);
    write_integer(max_row_label);
    write_integer(max_col_label);
    write_integer(max_sym_label);

    assert(nv - 2 == max_entry_index1);
    assert(nv - 2 == max_entry_index2);

    // printf("%d\n", nv - 2);
    write_integer(nv - 2);
    for (i = 0; i < max_entry_index1; ++i) {
      // printf("%d %d %d\n", T1[i].x, T1[i].y, T1[i].z);
      write_integer(T1[i].x);
      write_integer(T1[i].y);
      write_integer(T1[i].z);
    }
    // printf("%d\n", nv - 2);
    // write_integer(nv - 2);
    for (i = 0; i < max_entry_index2; ++i) {
        // printf("%d %d %d\n", T2[i].x, T2[i].y, T2[i].z);
      write_integer(T2[i].x);
      write_integer(T2[i].y);
      write_integer(T2[i].z);
    }

    free(vertex_colour);
    free(row_label);
    free(col_label);
    free(sym_label);

    free(T1);
    free(T2);

    return TRUE;
}

