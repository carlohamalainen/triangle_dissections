'''
Copyright 2010 Carlo Hamalainen <carlo.hamalainen@gmail.com>. All 
rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions
are met:

   1. Redistributions of source code must retain the above copyright 
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright 
      notice, this list of conditions and the following disclaimer
      in the documentation and/or other materials provided with the
      distribution.

THIS SOFTWARE IS PROVIDED BY Carlo Hamalainen ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL Carlo Hamalainen OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation 
are those of the authors and should not be interpreted as representing
official policies, either expressed or implied, of Carlo Hamalainen.
'''

import copy

import sage.all

import sys

try: import pyx
except ImportError: pass # ugh

from sage.combinat.matrices.latin import *
from sage.misc.search import search
from sage.rings.rational_field import QQ
from sage.rings.arith import lcm
import math

from spherical import *

import sympy

def centroid_of_triangle(pt1, pt2, pt3):
    """
    Find the centroid (barycentric centre) of a triangle.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: centroid_of_triangle((0,0), (1,0), (0,1))
        (1/3, 1/3)
    """

    return ((pt1[0] + pt2[0] + pt3[0])/3, (pt1[1] + pt2[1] + pt3[1])/3)

def up_triangle(pt1, pt2, pt3):
    r"""
    An "up" triangle looks like this:

          /\
         /  \           |\         /|
        /    \          | \       / |
        -------     or  |__\  or /__|

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: up_triangle((0,0), (1,0), (0,1))
        True
        sage: up_triangle((0,1), (1,1), (0,0))
        False
    """

    # Find the vertices on the horizontal
    h1 = None
    h2 = None
    for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
        if r[1] == s[1]:
            h1 = r
            h2 = s
            break

    assert h1 is not None
    assert h2 is not None

    pts = [pt1, pt2, pt3]
    pts.remove(h1)
    pts.remove(h2)
    assert len(pts) == 1
    h3 = pts[0]

    if h3[1] > h1[1]: return True # up triangle
    return False

def horizontal_length(pt1, pt2, pt3):
    """
    Length of the horizontal line of the triangle with 
    vertices pt1, pt2, pt3.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: horizontal_length((0,0), (1,0), (0,1))
        1
    """

    for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
        if r[1] == s[1]:
            return abs(r[0] - s[0])

    raise ValueError, "No horizontal side to this triangle."

def reflect1(x, y):
    """
    Reflect along the line x = 1/2.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: reflect1(1/4, 0)
        (3/4, 0)
    """

    # Shift everything left by 1/2
    x -= sympy.Rational(1, 2)

    # Reflect along x = 0 line
    x = -x

    # Shift back
    x += sympy.Rational(1, 2)

    return (x, y)

def reflect2(x, y):
    """
    The reflection of the equilateral triangle that fixes (0, 0).

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: reflect2(0, 0)
        (0, 0)
        sage: reflect2(1, 0)
        (1/2, 1/2*sqrt(3))
    """

    x, y = rotate_equilateral_inverse(x, y)
    x, y = reflect1(x, y)
    return rotate_equilateral(x, y)

def reflect3(x, y):
    """
    The reflection of the equilateral triangle that fixes (1, 0).

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: reflect3(1, 0)
        (1, 0)
        sage: reflect3(0, 0)
        (1/2, 1/2*sqrt(3))
    """

    x, y = rotate_equilateral(x, y)
    x, y = reflect1(x, y)
    return rotate_equilateral_inverse(x, y)

def rotate_equilateral(x, y, theta = 2*sympy.pi/3):
    """
    Perform a rotation on (x, y) anticlockwise by angle theta.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: rotate_equilateral(0, 0)
        (1, 0)
        sage: rotate_equilateral(1, 0)
        (1/2, 1/2*sqrt(3))
        sage: rotate_equilateral(sympy.Rational(1,2), 1/2*sympy.sqrt(3))
        (0, 0)

    Rotate ; reflect along x = 1/2; rotate^-1. Fixes (0,0) and swaps 
    the other two vertices:
        sage: x, y = rotate_equilateral_inverse(0, 0)
        sage: x, y = reflect1(x, y)
        sage: rotate_equilateral(x, y)
        (0, 0)

        sage: x, y = rotate_equilateral_inverse(1, 0)
        sage: x, y = reflect1(x, y)
        sage: rotate_equilateral(x, y)
        (1/2, 1/2*sqrt(3))

        sage: x, y = rotate_equilateral_inverse(sympy.Rational(1,2), 1/2*sympy.sqrt(3))
        sage: x, y = reflect1(x, y)
        sage: rotate_equilateral(x, y)
        (1, 0)
    """

    # Centre of the equilateral triangle:
    pt_x = sympy.Rational(1,2)
    pt_y = sympy.sqrt(3)/6

    x -= pt_x
    y -= pt_y

    x, y = (x*sympy.cos(theta) - y*sympy.sin(theta), x*sympy.sin(theta) + y*sympy.cos(theta))

    x += pt_x
    y += pt_y

    return (x, y)

def rotate_equilateral_inverse(x, y):
    """
    Inverse of rotate_equilateral(x, y).

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: rotate_equilateral_inverse(0, 0)
        (1/2, 1/2*sqrt(3))
    """
    return rotate_equilateral(x, y, theta = -2*sympy.pi/3)


def cross(*args): 
    """
    Mathematical cross product of parameters.

    EXAMPLE:
        sage: from triangle_dissections import *
        sage: cross(range(3), range(5))
        [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4]]
    """

    # http://code.activestate.com/recipes/159975/ 
    # At 1:55 a.m. on 21 nov 2002, Raymond Hettinger  said: 
    ans = [[]] 
    for arg in args: 
        ans = [x+[y] for x in ans for y in arg] 
    return ans 

def has_side_below(pt1, pt2, pt3, six):
    """
    Does the triangle (pt1, pt2, pt3) have a vertical side S which, if extended, intersects the point six,
    and the segment S is strictly below the point six.

    EXAMPLE:
        sage: from triangle_dissections import *
        sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
        sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
        sage: u = TriangleDissection(U1, U2, id_row = 2, id_col = 3, only_separated_solutions = False)
        sage: assert len(u.six_way_points) > 0
        sage: six = u.six_way_points.keys()[0]
        sage: [has_side_below(pt1, pt2, pt3, six) for (pt1, pt2, pt3) in u.points[six]]
        [True, False, False, False, True, False]
    """

    for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
        if line_type(r, s) != "vertical": continue

        if r[0] == six[0] and (r[1] < six[1] or s[1] < six[1]):
            return True 

    return False

def has_side_below_right(pt1, pt2, pt3, six):
    """
    Does the triangle (pt1, pt2, pt3) have a diagonal side S which, if extended, intersects the point six,
    and the segment S is strictly below-right of the point six.

    EXAMPLE:
        sage: from triangle_dissections import *
        sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
        sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
        sage: u = TriangleDissection(U1, U2, id_row = 2, id_col = 3, only_separated_solutions = False)
        sage: assert len(u.six_way_points) > 0
        sage: six = u.six_way_points.keys()[0]
        sage: [has_side_below_right(pt1, pt2, pt3, six) for (pt1, pt2, pt3) in u.points[six]]
        [False, False, False, False, True, True]
    """
    if (pt1, pt2, pt3) == ((1/2, 0), (1/2, 1/6), (2/3, 0)): debug = True
    else: debug = False

    for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
        if line_type(r, s) != "diagonal": continue

        if six == r:
            if s[0] > six[0]: return True
        if six == s:
            if r[0] > six[0]: return True

        if not is_down_right(six, r): return False
        if not is_down_right(six, s): return False

        if colinear(six, r, s):
            return True 

    return False


def is_down_right(pt1, pt2):
    """
    EXAMPLES:
        sage: from triangle_dissections import *
        sage: is_down_right((0,0), (0, 0))
        False
        sage: is_down_right((0,0), (1, 0))
        False
        sage: is_down_right((0,0), (1, 1))
        False
        sage: is_down_right((0,0), (-1, -1))
        False
        sage: is_down_right((-1, -1), (0, 0))
        False
        sage: is_down_right((0, 0), (1, -1))
        True
    """


    if pt1[0] >= pt2[0]: return False
    if pt1[1] <= pt2[1]: return False

    return True

def distance(pt1, pt2):
    """
    Square of the euclidean distance between two points.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: distance((0,0), (1,1))
        2
    """

    return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2

def arg_relative(origin_x, origin_y, x, y):
    """
    Returns the argument of x + y*I relative to the
    origin origin_x + origin_y*I.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: arg_relative(0, 0, 0, 1)
        1.5707963267948966
        sage: arg_relative(0, 0, 1, 1)
        0.78539816339744828
        sage: arg_relative(1, 1, 1, 1)
        0.0
        sage: arg_relative(1, 1, 2, 2)
        0.78539816339744828
    """

    theta = math.atan2(y - origin_y, x - origin_x)
    if theta < 0: theta += 2*math.pi
    return theta 

def disjoint_mate_dlxcpp_rows_and_map(P, allow_subtrade):
    """
    Sets up a 0-1 matrix such that a solution to the exact cover problem
    on the matrix corresponds exactly to a disjoint mate of P. This is a
    utility function for dlxcpp_find_mates().

    EXAMPLE:
        sage: from sage.combinat.matrices.latin import *
        sage: B = back_circulant(4)
        sage: disjoint_mate_dlxcpp_rows_and_map(B, allow_subtrade = True)
        ([[0, 16, 32], [1, 17, 32], [2, 18, 32], [3, 19, 32], [4, 16, 33], [5, 17, 33], [6, 18, 33], [7, 19, 33], [8, 16, 34], [9, 17, 34], [10, 18, 34], [11, 19, 34], [12, 16, 35], [13, 17, 35], [14, 18, 35], [15, 19, 35], [0, 20, 36], [1, 21, 36], [2, 22, 36], [3, 23, 36], [4, 20, 37], [5, 21, 37], [6, 22, 37], [7, 23, 37], [8, 20, 38], [9, 21, 38], [10, 22, 38], [11, 23, 38], [12, 20, 39], [13, 21, 39], [14, 22, 39], [15, 23, 39], [0, 24, 40], [1, 25, 40], [2, 26, 40], [3, 27, 40], [4, 24, 41], [5, 25, 41], [6, 26, 41], [7, 27, 41], [8, 24, 42], [9, 25, 42], [10, 26, 42], [11, 27, 42], [12, 24, 43], [13, 25, 43], [14, 26, 43], [15, 27, 43], [0, 28, 44], [1, 29, 44], [2, 30, 44], [3, 31, 44], [4, 28, 45], [5, 29, 45], [6, 30, 45], [7, 31, 45], [8, 28, 46], [9, 29, 46], [10, 30, 46], [11, 31, 46], [12, 28, 47], [13, 29, 47], [14, 30, 47], [15, 31, 47]], {(9, 29, 46): (3, 2, 1), (13, 17, 35): (0, 3, 1), (7, 19, 33): (0, 1, 3), (14, 26, 43): (2, 3, 2), (0, 28, 44): (3, 0, 0), (5, 25, 41): (2, 1, 1), (11, 31, 46): (3, 2, 3), (14, 18, 35): (0, 3, 2), (11, 23, 38): (1, 2, 3), (5, 29, 45): (3, 1, 1), (13, 21, 39): (1, 3, 1), (1, 29, 44): (3, 0, 1), (0, 20, 36): (1, 0, 0), (12, 24, 43): (2, 3, 0), (8, 28, 46): (3, 2, 0), (12, 20, 39): (1, 3, 0), (11, 27, 42): (2, 2, 3), (6, 22, 37): (1, 1, 2), (1, 17, 32): (0, 0, 1), (10, 18, 34): (0, 2, 2), (12, 28, 47): (3, 3, 0), (1, 25, 40): (2, 0, 1), (10, 22, 38): (1, 2, 2), (5, 17, 33): (0, 1, 1), (3, 23, 36): (1, 0, 3), (6, 26, 41): (2, 1, 2), (9, 25, 42): (2, 2, 1), (7, 31, 45): (3, 1, 3), (15, 27, 43): (2, 3, 3), (3, 31, 44): (3, 0, 3), (8, 20, 38): (1, 2, 0), (2, 22, 36): (1, 0, 2), (3, 19, 32): (0, 0, 3), (9, 17, 34): (0, 2, 1), (15, 31, 47): (3, 3, 3), (8, 16, 34): (0, 2, 0), (14, 22, 39): (1, 3, 2), (4, 16, 33): (0, 1, 0), (14, 30, 47): (3, 3, 2), (2, 30, 44): (3, 0, 2), (4, 20, 37): (1, 1, 0), (6, 30, 45): (3, 1, 2), (12, 16, 35): (0, 3, 0), (15, 19, 35): (0, 3, 3), (5, 21, 37): (1, 1, 1), (4, 24, 41): (2, 1, 0), (13, 25, 43): (2, 3, 1), (0, 16, 32): (0, 0, 0), (15, 23, 39): (1, 3, 3), (7, 23, 37): (1, 1, 3), (6, 18, 33): (0, 1, 2), (10, 30, 46): (3, 2, 2), (13, 29, 47): (3, 3, 1), (11, 19, 34): (0, 2, 3), (1, 21, 36): (1, 0, 1), (7, 27, 41): (2, 1, 3), (0, 24, 40): (2, 0, 0), (10, 26, 42): (2, 2, 2), (3, 27, 40): (2, 0, 3), (2, 26, 40): (2, 0, 2), (9, 21, 38): (1, 2, 1), (8, 24, 42): (2, 2, 0), (4, 28, 45): (3, 1, 0), (2, 18, 32): (0, 0, 2)})
    """

    assert P.nrows() == P.ncols()

    n = P.nrows()

    # We will need 3n^2 columns in total:
    #
    # n^2 for the xCy columns
    # n^2 for the xRy columns
    # n^2 for the xy columns

    dlx_rows = []
    cmap = {}

    max_column_nr = -1

    for r in range(n):
        valsrow = P.vals_in_row(r)

        for c in range(n):
            valscol = P.vals_in_col(c)

            # If this is an empty cell of P then we do nothing.
            if P[r, c] < 0: continue

            for e in uniq(valsrow.keys() + valscol.keys()):
                # These should be constants
                c_OFFSET  = e + c*n
                r_OFFSET  = e + r*n + n*n
                xy_OFFSET = 2*n*n + r*n + c

                cmap[(c_OFFSET, r_OFFSET, xy_OFFSET)] = (r,c,e)

                # The disjoint mate has to be disjoint.
                if (not allow_subtrade) and P[r, c] == e: continue
                # fixme by not skipping on equality here we are allowing
                # for the search into sub-trades!!!!!

                # The permissible symbols must come from this row/column.
                if not(valsrow.has_key(e)): continue
                if not(valscol.has_key(e)): continue


                dlx_rows.append([c_OFFSET, r_OFFSET, xy_OFFSET])

                if max_column_nr < max(c_OFFSET, r_OFFSET, xy_OFFSET):
                    max_column_nr = max(c_OFFSET, r_OFFSET, xy_OFFSET)

    # We will have missed some columns. My old C++ code would cover the
    # empty columns before finding a solution, but now it doesn't. So we
    # have to add 'dummy' rows to fill things out.
    used_columns = flatten(dlx_rows)
    for i in range(0, max_column_nr+1):
        if not i in used_columns:
            dlx_rows.append([i])

    return dlx_rows, cmap

def dlxcpp_find_mates(P, nr_to_find = None, allow_subtrade = False):
    """
    WARNING: if allow_subtrade is True then we may return a partial
    latin square that is *not* disjoint to P. In that case, use
    bitrade(P, Q) to get an actual bitrade.

    EXAMPLES:
        sage: from sage.combinat.matrices.latin import *
        sage: B = back_circulant(4)
        sage: g = dlxcpp_find_mates(B, allow_subtrade = True)
        sage: B1 = g.next()
        sage: B0, B1 = bitrade(B, B1)
        sage: assert is_bitrade(B0, B1)
        sage: print B0, "\n,\n", B1
        [-1  1  2 -1]
        [-1  2 -1  0]
        [-1 -1 -1 -1]
        [-1  0  1  2] 
        ,
        [-1  2  1 -1]
        [-1  0 -1  2]
        [-1 -1 -1 -1]
        [-1  1  2  0]
    """

    assert P.nrows() == P.ncols()

    n = P.nrows()

    dlx_rows, cmap = disjoint_mate_dlxcpp_rows_and_map(P, allow_subtrade)

    nr_found = 0

    for x in DLXCPP(dlx_rows):
        nr_found += 1

        Q = copy.deepcopy(P)

        for y in x:
            if len(dlx_rows[y]) == 1: continue # dummy row
            (r, c, e) = cmap[tuple(dlx_rows[y])]
            Q[r, c] = e

        yield Q

        if nr_to_find is not None and nr_found >= nr_to_find: return


def line_type(pt1, pt2):
    """
    A line passing through points pt1 and pt2 is either horizontal,
    vertical, or diagonal.

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: line_type((0,0), (0,1))
        'vertical'
        sage: line_type((0,0), (1,1))
        'diagonal'
        sage: line_type((0,0), (1,0))
        'horizontal'
    """

    if pt1[0] == pt2[0]:    return "vertical"
    if pt1[1] == pt2[1]:    return "horizontal"

    return "diagonal"

def colinear(u, v, w):
    """
    Are the distinct points u, v, w on a straight line?

    EXAMPLES:
        sage: print colinear( (0,0), (0,1), (0,2) )
        True
        sage: print colinear( (0,0), (0,2), (0,1) )
        True
        sage: print colinear( (0,0), (0,1), (1,2) )
        False
        sage: print colinear( (0,0), (1,1), (3,3) )
        True
        sage: print colinear( (0,1/2), (1,1), (3,3) )
        False
        sage: print colinear( (-1/2,-1/2), (1,1), (3,3) )
        True
    """

    # Sort the points so that they look like this:
    #
    #   w
    #  v
    # u
    pts = [u, v, w]
    pts.sort(key = (lambda x: x[0]))
    pts.sort(key = (lambda x: x[1]))

    u, v, w = pts[0], pts[1], pts[2]

    # We only look at distinct points:
    assert u != v and u != w and v != w

    # One but not both of u-v or v-w is vertical:
    if v[0] - u[0] == 0 and w[0] - v[0] != 0: return False
    if v[0] - u[0] != 0 and w[0] - v[0] == 0: return False

    # Vertical line:
    if v[0] - u[0] == 0 and w[0] - v[0] == 0: return True

    # Horizontal line:
    if v[1] - u[1] == 0 and w[1] - v[1] == 0: return True

    # 0 < slope < infty
    return (v[1] - u[1])/(v[0] - u[0]) == (w[1] - v[1])/(w[0] - v[0])

def colinear_and_ordered(u, v, w):
    """
    Are the distinct points u, v, w on a straight line, in that
    actual order?

    EXAMPLES:
        sage: print colinear_and_ordered( (0,0), (0,1), (0,2) )
        True
        sage: print colinear_and_ordered( (0,0), (0,2), (0,1) )
        False
        sage: print colinear_and_ordered( (0,0), (1,1), (2,2) )
        True
    """

    if not colinear(u, v, w): return False

    # w        u
    # v   or   v
    # u        w
    if u[0] == v[0] == w[0]:
        return u[1] < v[1] < w[1] or u[1] > v[1] > w[1]

    # u v w
    # or
    # w v u
    if u[1] == v[1] == w[1]:
        return u[0] < v[0] < w[0] or u[0] > v[0] > w[0]

    #   w
    #  v
    # u
    if u[0] < v[0] and v[0] < w[0] and \
       u[1] < v[1] and v[1] < w[1]:
        return True

    #   u
    #  v
    # w
    if u[0] > v[0] and v[0] > w[0] and \
       u[1] > v[1] and v[1] > w[1]:
        return True

    # u
    #  v
    #   w
    if u[0] < v[0] and v[0] < w[0] and \
       u[1] > v[1] and v[1] > w[1]:
        return True
      
    # w
    #  v
    #   u
    if u[0] > v[0] and v[0] > w[0] and \
       u[1] < v[1] and v[1] < w[1]:
        return True
   
    return False 

def triangle_size(pt1, pt2, pt3):
    """
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
    """

    if pt1[0] == pt2[0]: return abs(pt1[1] - pt2[1])
    if pt1[1] == pt2[1]: return abs(pt1[0] - pt2[0])

    return triangle_size(pt2, pt3, pt1)

class TriangleDissection:
    def __init__(self, T1, T2, id_row = None, id_col = None, only_separated_solutions = False):
        """
        EXAMPLES:

        A separated spherical bitrade T = (T1, T2):
            sage: from triangle_dissections import *
            sage: T1 = LatinSquare(matrix(ZZ, [[0, 1, 2, -1, -1], [3, -1, 0, 4, -1], [1, 2, 4, 3, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]))
            sage: T2 = LatinSquare(matrix(ZZ, [[1, 2, 0, -1, -1], [0, -1, 4, 3, -1], [3, 1, 2, 4, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]))
            sage: assert is_bitrade(T1, T2)

        In (fixme) T1 is usually denoted T^* and T2 is T^triangle. Let 
        a = (a1, a2, a3) be some triple in T1. Then we form a system of
        equations Eq(T, a) with b1 + b2 = b3 for all (b1, b2, b3) in 
        T1 \ {a} and additionally a1 = 0, a2 = 0, a3 = 1. By (fixme)
        we know that the system has a unique solution in the rationals.

        Draw the triangle Sigma bounded by the lines y = 0, x = 0, x + y = 1.
        Draw the triangles bounded by the lines
        y = bar c_1, x = bar c_2, x + y = bar c_3. By (fixme) we
        know that these triangles will all be inside the triangle Sigma.

        This class takes a separated spherical latin bitrade, a triple
        (a1,a2,a3), and finds solutions to Eq(T, a). We are able to see the
        dissecting triangles

        Form the triangle dissection with (a1, a2) = (0, 0) and allow nonseparated solutions:
            sage: d = TriangleDissection(T1, T2, id_row = 0, id_col = 0, only_separated_solutions = False)

        The bitrade has row_max rows, col_max columns, and uses sym_max symbols:
            sage: d.row_max
            3
            sage: d.col_max
            4
            sage: d.sym_max
            5

        We have a dictionary for the triangles of the dissection:
            sage: sorted(d.triangles.keys())
            [((0, 0), (0, 1/4), (1/4, 0)),
             ((0, 1/4), (0, 1/2), (1/4, 1/4)),
             ((0, 1/4), (1/4, 0), (1/4, 1/4)),
             ((0, 1/2), (0, 1), (1/2, 1/2)),
             ((0, 1/2), (1/4, 1/4), (1/4, 1/2)),
             ((1/4, 0), (1/4, 1/4), (1/2, 0)),
             ((1/4, 1/4), (1/4, 1/2), (1/2, 1/4)),
             ((1/4, 1/4), (1/2, 0), (1/2, 1/4)),
             ((1/4, 1/2), (1/2, 1/4), (1/2, 1/2)),
             ((1/2, 0), (1/2, 1/2), (1, 0))]

        The corners of the dissecting triangles are stored in a dictionary
        that associates a point pt to all of the triangles with one vertex
        equal to pt.
            sage: sorted(d.points)
            [(0, 0),
             (0, 1/4),
             (0, 1/2),
             (0, 1),
             (1/4, 0),
             (1/4, 1/4),
             (1/4, 1/2),
             (1/2, 0),
             (1/2, 1/4),
             (1/2, 1/2),
             (1, 0)]

        For example, there is one triangle with a vertex equal to (0,0):
            sage: d.points[(0,0)]
            [((0, 0), (0, 1/4), (1/4, 0))]

        While three triangles share the vertex (1/2,1/2):
            sage: d.points[(1/2,1/2)]
            [((0, 1/2), (0, 1), (1/2, 1/2)),
             ((1/2, 0), (1/2, 1/2), (1, 0)),
             ((1/4, 1/2), (1/2, 1/4), (1/2, 1/2))]

        The 'outer' triple:
            sage: (d.a1, d.a2, d.a3)
            (0, 0, 0)
            sage: assert T1[d.a1, d.a2] == d.a3

        The original bitrade is (T1, T2):
            sage: d.T1
            [ 0  1  2 -1 -1]
            [ 3 -1  0  4 -1]
            [ 1  2  4  3 -1]
            [-1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1]
            sage: d.T2
            [ 1  2  0 -1 -1]
            [ 0 -1  4  3 -1]
            [ 3  1  2  4 -1]
            [-1 -1 -1 -1 -1]
            [-1 -1 -1 -1 -1]

        The solution Eq(T, a) is stored in original_solution_r,
        original_solution_c, and original_solution_s.
            sage: RC = [(r, c) for (r, c) in cross(range(d.row_max), range(d.col_max)) if T1[r, c] >= 0]
            sage: RC.remove((d.a1, d.a2))
            sage: for (r, c) in RC: assert d.original_solution_r[r] + d.original_solution_c[c] == d.original_solution_s[T1[r,c]]

            sage: assert d.original_solution_r[d.a1] == 0
            sage: assert d.original_solution_c[d.a2] == 0
            sage: assert d.original_solution_s[d.a3] == 1

        If the solution to Eq(T, a) is not separated (fixme) then we can get
        the reduced bitrade via the geometric data (the actual dissection):

            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.T1
            [ 0  1  2]
            [ 1 -1  0]
            [-1  2  1]
            sage: u.T2
            [ 1  2  0]
            [ 0 -1  1]
            [-1  1  2]
            sage: u.generate_bitrade_via_geometric_data()
            sage: u.X1
            [1 0]
            [0 1]
            sage: u.X2
            [0 1]
            [1 0]
        
        and we can see which entries in the original bitrade (U1, U2)
        degenerated:

            sage: u.T2_degenerate_entries
            {(0, 1, 2): True, (2, 2, 2): True, (2, 1, 1): True}
            sage: for (r, c, s) in u.T2_degenerate_entries.keys(): assert u.T2[r, c] == s
        """

        self.row_max, self.col_max, self.sym_max, id_row, \
        id_col, self.M = find_solution(T1, id_row, id_col, only_separated_solutions)

        self.T1 = T1
        self.T2 = T2

        self.a1 = id_row
        self.a2 = id_col
        self.a3 = T1[id_row, id_col]

        # we have an embedding into a triangle of side n.
        self.n = int(lcm([self.M[i].denom() for i in range(len(self.M))]))

        self.triangles = {}
        self.triangle_sizes = {}

        # Here we store the solution to Eq(T, a).
        self.original_solution_r = [-1] * self.row_max
        self.original_solution_c = [-1] * self.col_max
        self.original_solution_s = [-1] * self.sym_max

        # If only_separated_solutions = False then we may get a solution
        # where some of the variables degenerate, ie. r_i = r_j for
        # distinct rows r_i, r_j. In this case we remove redundant
        # variables and store the solution in reduced_solution_[r,c,s]
        self.reduced_solution_r = []
        self.reduced_solution_c = []
        self.reduced_solution_s = []
        #self.T1_reduced = LatinSquare(max(self.row_max, self.col_max, self.sym_max))
        #self.T2_reduced = LatinSquare(max(self.row_max, self.col_max, self.sym_max))

        self.T2_degenerate_entries = {}

        for r in range(self.row_max):
            for c in range(self.col_max):
                s = T2[r, c]
                if s < 0: continue

                w1 = self.M[r]
                w2 = self.M[c + self.row_max]
                w3 = self.M[s + self.row_max + self.col_max]

                self.original_solution_r[r] = w1
                self.original_solution_c[c] = w2
                self.original_solution_s[s] = w3

                # The triangle corresponding to (r,c,s) in T2 has
                # vertices pt1, pt2, pt3:
                pt1 = (w2, w1)
                pt2 = (w2, w3 - w2)
                pt3 = (w3 - w1, w1)

                if triangle_size(pt1, pt2, pt3) > 0:
                    self.reduced_solution_r.append(w1)
                    self.reduced_solution_c.append(w2)
                    self.reduced_solution_s.append(w3)

                    assert not self.triangles.has_key(tuple(sorted([pt1, pt2, pt3])))

                    self.triangles[tuple(sorted([pt1, pt2, pt3]))] = True

                    self.triangles[tuple(sorted([pt1, pt2, pt3]))] = True
                    self.triangle_sizes[self.n*triangle_size(pt1, pt2, pt3)] = True
                else:
                    self.T2_degenerate_entries[(r, c, s)] = True

        assert not self.triangle_sizes.has_key(0)

        self.corners = [(0,0), (0,1), (1,0)]

        self.points = {}
        for t in self.triangles.keys():
            for i in range(3):
                try:
                    self.points[t[i]].append(t)
                except KeyError:
                    self.points[t[i]] = [t]

        # Vertices with degree 6 require special treatement to recover
        # the underlying bitrade (namely, separation) so we make a note
        # of these for later.
        self.six_way_points = {}
        for p in self.points.keys():
            if len(self.points[p]) == 6:
                self.six_way_points[p] = True

    def lines_of_trade(self):
        """
        Return a 3-tuple consisting of dictionaries mapping a line to an
        integer.

        EXAMPLES:

            sage: from triangle_dissections import *
            sage: T1 = LatinSquare(matrix(ZZ, [[0, 1, 2, -1, -1], [3, -1, 0, 4, -1], [1, 2, 4, 3, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]))
            sage: T2 = LatinSquare(matrix(ZZ, [[1, 2, 0, -1, -1], [0, -1, 4, 3, -1], [3, 1, 2, 4, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]))
            sage: assert is_bitrade(T1, T2)
            sage: d = TriangleDissection(T1, T2, id_row = 0, id_col = 0, only_separated_solutions = False)

        Lines of this dissection:        
            sage: d.lines_of_trade()
            ({0: 0, 1/2: 2, 1/4: 1}, {0: 0, 1/2: 2, 1/4: 1}, {1: 3, 1/2: 1, 1/4: 0, 3/4: 2})

        This gives the lines:
        horizontal: {y = 0, y = 1/4, y = 1/2}
        vertical:   {x = 0, x = 1/4, x = 1/2}
        diagonal:   {x + y = 1/4, x + y = 1/2, x + y = 3/4, x + y = 1}

        The dictionary values are sorted in ascending order with regards
        to the increasing order of the keys. This makes it easy for us
        to later construct the bitrade labeled by these lines, e.g. the
        horizontal line y = 1/4 will correspond to r_1.
        """

        horizontal_lines = []
        vertical_lines = []
        diagonal_lines = []

        for t in self.triangles.keys():
            pt1 = t[0]
            pt2 = t[1]
            pt3 = t[2]

            for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
                ltype = line_type(r, s)

                if ltype == "vertical":
                    k = r[0]

                    vertical_lines.append(k)

                if ltype == "horizontal":
                    k = r[1]

                    horizontal_lines.append(k)

                if ltype == "diagonal":
                    m = (s[1] - r[1])/(s[0] - r[0])
                    if m > 0: m *= -1
                    c = r[1] - m*r[0]
                    intercept = -c/m

                    diagonal_lines.append(intercept)

        vertical_lines = uniq(vertical_lines)
        horizontal_lines = uniq(horizontal_lines)
        diagonal_lines = uniq(diagonal_lines)

        return dict(zip(horizontal_lines, range(len(horizontal_lines)))), \
               dict(zip(vertical_lines, range(len(vertical_lines)))), \
               dict(zip(diagonal_lines, range(len(diagonal_lines))))

    def walk_down(self, pt):
        """
        Try to walk downwards (in the Euclidean plane) to the next vertex in the
        dissection.

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.walk_down((0, 1))
            (0, 1/2)
        """

        # distances are within a unit triangle so this is guaranteed
        # to be larger than any inter-vertex distance.
        min_distance = 10
        min_q = None

        for (pt1, pt2, pt3) in self.points[pt]:
            for q in [pt1, pt2, pt3]:
                if q == pt: continue

                if q[0] != pt[0]: continue

                if q[1] >= pt[1]: continue

                if distance(pt, q) < min_distance:
                    min_distance = distance(pt, q)
                    min_q = q

        return min_q

    def walk_down_right(self, pt):
        """
        Try to walk down-right (in the Euclidean plane) to the next vertex in the
        dissection.

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.walk_down_right((0, 1))
            (1/2, 1/2)
        """

        # distances are within a unit triangle so this is guaranteed
        # to be larger than any inter-vertex distance.
        min_distance = 10
        min_q = None

        for (pt1, pt2, pt3) in self.points[pt]:
            for q in [pt1, pt2, pt3]:
                if q == pt: continue

                if q[0] <= pt[0]: continue

                if q[1] >= pt[1]: continue

                if distance(pt, q) < min_distance:
                    min_distance = distance(pt, q)
                    min_q = q

        return min_q

    def relabel_triangle_column(self, pt1, pt2, pt3, new_label):
        """
        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: pt1, pt2, pt3 = u.triangles.keys()[0]

        These may not be the actual row/column/symbol lines of the trade; just used
        for showing how the relabel_triangle_column function changes a label.
            sage: u.triangles[(pt1,pt2,pt3)] = [(0, "r"), (0, "c"), (0, "s")] 
            sage: u.relabel_triangle_column(pt1, pt2, pt3, 1)
            sage: u.triangles[(pt1,pt2,pt3)]
            [(0, 'r'), (1, 'c'), (0, 's')]
        """

        for i in range(3):
            if self.triangles[(pt1, pt2, pt3)][i][1] == "c":
                self.triangles[(pt1, pt2, pt3)][i] = (new_label, 'c')

    def relabel_triangle_symbol(self, pt1, pt2, pt3, new_label):
        """
        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: pt1, pt2, pt3 = u.triangles.keys()[0]

        These may not be the actual row/column/symbol lines of the trade; just used
        for showing how the relabel_triangle_column function changes a label.
            sage: u.triangles[(pt1,pt2,pt3)] = [(0, "r"), (0, "c"), (0, "s")] 
            sage: u.relabel_triangle_symbol(pt1, pt2, pt3, 1)
            sage: u.triangles[(pt1,pt2,pt3)]
            [(0, 'r'), (0, 'c'), (1, 's')]
        """
        for i in range(3):
            if self.triangles[(pt1, pt2, pt3)][i][1] == "s":
                self.triangles[(pt1, pt2, pt3)][i] = (new_label, 's')

    def label_of_triangle(self, pt1, pt2, pt3, rcs):
        """
        After generate_bitrade_via_geometric_data() has executed, the
        self.triangles dictionary has information about the row, column,
        and symbol labels of the lines bounding each triangle.

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.generate_bitrade_via_geometric_data()
            sage: pt1, pt2, pt3 = u.triangles.keys()[1]
            sage: u.label_of_triangle(pt1, pt2, pt3, 'r')
            1
            sage: u.label_of_triangle(pt1, pt2, pt3, 'c')
            0
            sage: u.label_of_triangle(pt1, pt2, pt3, 's')
            1
        """
        assert rcs in ['r', 'c', 's']

        for i in range(3):
            if self.triangles[(pt1, pt2, pt3)][i][1] == rcs:
                return self.triangles[(pt1, pt2, pt3)][i][0]

    def generate_bitrade_via_geometric_data(self):
        """
        Given just the geometric data of a triangle dissection (points,
        lines, triangles) form the bitrade (X1, X2) by labelling lines
        and separating any vertices of degree 6. The resulting bitrade
        is stored in self.X1, self.X2.

        EXAMPLES:

            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.T1
            [ 0  1  2]
            [ 1 -1  0]
            [-1  2  1]
            sage: u.T2
            [ 1  2  0]
            [ 0 -1  1]
            [-1  1  2]
            sage: u.generate_bitrade_via_geometric_data()
            sage: u.X1
            [1 0]
            [0 1]
            sage: u.X2
            [0 1]
            [1 0]
            sage: u.T2_degenerate_entries
            {(0, 1, 2): True, (2, 2, 2): True, (2, 1, 1): True}
            sage: for (r, c, s) in u.T2_degenerate_entries.keys(): assert u.T2[r, c] == s

        """

        horizontal_lines, vertical_lines, diagonal_lines = self.lines_of_trade()

        self.sym_max = len(diagonal_lines)

        for (pt1,pt2,pt3) in self.triangles.keys():

            self.triangles[(pt1,pt2,pt3)] = []

            for (r, s) in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
                ltype = line_type(r, s)

                if ltype == "vertical":
                    k = r[0]

                    y = vertical_lines[k]

                    self.triangles[(pt1,pt2,pt3)].append((y, "c"))
                if ltype == "horizontal":
                    k = r[1]

                    x = horizontal_lines[k]

                    self.triangles[(pt1,pt2,pt3)].append((x, "r"))
                if ltype == "diagonal":
                    m = (s[1] - r[1])/(s[0] - r[0])
                    if m > 0: m *= -1
                    c = r[1] - m*r[0]
                    k = -c/m

                    z = diagonal_lines[k]

                    self.triangles[(pt1,pt2,pt3)].append((z, "s"))

        self.max_triangle_row_label = len(horizontal_lines)
        self.max_triangle_col_label = len(vertical_lines)
        self.max_triangle_sym_label = len(diagonal_lines)

        six_points = self.six_way_points.keys()
        six_points.sort()

        self.separated_columns = {}
        self.separated_symbols = {}

        self.original_max_triangle_col_label = len(vertical_lines)
        self.original_max_triangle_sym_label = len(diagonal_lines)

        for six in six_points:
            pt = six
            while True:
                # For each triangle around this point:
                for (pt1, pt2, pt3) in self.points[pt]:
                    if has_side_below(pt1, pt2, pt3, six):
                        lab = self.label_of_triangle(pt1, pt2, pt3, 'c')

                        if lab != self.max_triangle_col_label:
                            self.separated_columns[lab] = self.max_triangle_col_label

                        self.relabel_triangle_column(pt1, pt2, pt3, self.max_triangle_col_label)
                pt = self.walk_down(pt)
                if pt is None: break
                if self.six_way_points.has_key(pt): break

            pt = six
            while True:
                # For each triangle around this point:
                for (pt1, pt2, pt3) in self.points[pt]:
                    if has_side_below_right(pt1, pt2, pt3, six):
                        lab = self.label_of_triangle(pt1, pt2, pt3, 's')

                        if lab != self.max_triangle_sym_label:
                            self.separated_symbols[lab] = self.max_triangle_sym_label

                        self.relabel_triangle_symbol(pt1, pt2, pt3, self.max_triangle_sym_label)

                pt = self.walk_down_right(pt)
                if pt is None: break
                if self.six_way_points.has_key(pt): break

            self.max_triangle_col_label += 1
            self.max_triangle_sym_label += 1

        self.X2 = LatinSquare(max(self.max_triangle_row_label, self.max_triangle_col_label, self.max_triangle_sym_label))

        for (g1, g2, g3) in self.triangles.values():
            r = -1
            c = -1
            s = -1

            for (v, w) in [g1, g2, g3]:
                if w == "r": r = v
                if w == "c": c = v
                if w == "s": s = v

            self.X2[r, c] = s

        assert self.X2.is_partial_latin_square()
        g = dlxcpp_find_mates(self.X2, allow_subtrade = False)
        self.X1 = g.next()

        assert is_bitrade(self.X1, self.X2)
        assert genus(self.X1, self.X2) == 0


    def previous_vertex(self, v):
        """
        This function finds the triangle [self.corners[v], x, y]
        and returns the vertex x or y which is found in the anticlockwise
        order around the border of the dissection.

        EXAMPLES:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.previous_vertex(0)
            (1/2, 0)
        """

        assert len(self.points[self.corners[v]]) == 1
        vertices = list(self.points[self.corners[v]][0])
        vertices.remove(self.corners[v])

        # Perhaps this triangle is right next to the previous
        # corner point:
        if vertices[0] == self.corners[v-1]:
            return self.corners[v-1]
        if vertices[1] == self.corners[v-1]:
            return self.corners[v-1]

        # Otherwise we must find the vertices[i] that is colinear
        # with the previous corner point.
        for i in [0, 1]:
            if colinear(self.corners[v-1], vertices[i], self.corners[v]):
                return vertices[i]
        
        raise ValueError, "unable to find previous vertex"

    def next_vertex(self, v):
        """
        This function finds the triangle [self.corners[v], x, y]
        and returns the vertex x or y which is found in the clockwise
        order around the border of the dissection.

        EXAMPLES:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.next_vertex(0)
            (0, 1/2)
        """

        assert len(self.points[self.corners[v]]) == 1
        vertices = list(self.points[self.corners[v]][0])
        vertices.remove(self.corners[v])
        vertices.remove(self.previous_vertex(v))
        assert len(vertices) == 1

        return vertices[0]

    def adjacent_triangle(self, pt1, pt2, pt3, r, s):
        """
        (pt1, pt2, pt3) is a triangle in the dissection t
        r, s are in [pt1, pt2, pt3]

        We find the triangle (q1, q2, q3) such that the common
        vertices with (pt1, pt2, pt3) are r and s.

        EXAMPLE:

            sage: from triangle_dissections import *
            sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
            sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
            sage: assert is_bitrade(T1, T2)
            sage: t53 = TriangleDissection(T1, T2, 5, 3, only_separated_solutions = False)

        Find the triangle with a corner at (11/39, 19/39):

            sage: pt1, pt2, pt3 = t53.points[(11/39, 19/39)][0]

        The adjacent triangle is:

            sage: t53.adjacent_triangle(pt1, pt2, pt3, r = pt2, s = pt3)
            ((11/39, 19/39), (1/3, 17/39), (1/3, 19/39), (1/3, 19/39))
        """

        assert self.triangles.has_key((pt1, pt2, pt3))

        assert r != s

        assert r in [pt1, pt2, pt3]
        assert s in [pt1, pt2, pt3]

        for (q1, q2, q3) in self.points[r]:
            if (q1, q2, q3) == (pt1, pt2, pt3): continue

            assert r in [q1, q2, q3]
            if s not in [q1, q2, q3]: continue

            points = [q1, q2, q3]
            points.remove(r)
            points.remove(s)

            return q1, q2, q3, points[0]

        raise ValueError, "no adjacent triangle with same size"


    def neighbours(self, v):
        """
        Find the (unsorted) neighbours of the point v.

        EXAMPLE:

            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.neighbours(u.points.keys()[0])
            [(0, 1/2), (1/2, 1/2)]
        """

        assert self.points.has_key(v)

        adjacent_points = []

        for t in self.points[v]:
            t = list(t)
            t.remove(v)

            assert len(t) == 2

            if len(adjacent_points) == 0:
                adjacent_points = t
            else:
                # Make sure that we don't add a colinear point

                to_remove = []

                # These two blocks of code are the same except
                # for t[0] and t[1].
                for u in adjacent_points:
                    if t[0] == u: continue

                    if colinear_and_ordered(v, t[0], u):
                        to_remove.append(u)
                    if colinear_and_ordered(v, u, t[0]):
                        to_remove.append(t[0])
                for u in adjacent_points:
                    if t[1] == u: continue

                    if colinear_and_ordered(v, t[1], u):
                        to_remove.append(u)
                    if colinear_and_ordered(v, u, t[1]):
                        to_remove.append(t[1])
                        #print v, t[1], "removing", t[0]

                adjacent_points += [t[0], t[1]]

                #print adjacent_points, to_remove

                for x in to_remove:
                    adjacent_points.remove(x)

        adjacent_points = uniq(adjacent_points)

        return adjacent_points

    def has_dividing_line(self):
        """
        See if the triangle dissection, in core form, has a dividing line.

        EXAMPLES:
            sage: from triangle_dissections import *
            sage: W1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
            sage: W2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
            sage: w = TriangleDissection(W1, W2, id_row = 2, id_col = 3, only_separated_solutions = False)
            sage: w.core()
            sage: w.has_dividing_line()
            True
        """

        assert len(self.corners) == 6

        for z in range(6): # fixme slightly redundant due to symmetry?
            pt1 = self.corners[z]
            pt2 = self.corners[(z+3) % 6]

            line = [pt1]

            current_point = pt1

            # Try to build a line from pt1 to pt2 
            while line[-1] != pt2:
                made_extension = False

                for new_pt in self.neighbours(line[-1]):
                    assert new_pt != line[-1]

                    # Reached the end?
                    if new_pt == pt2 and colinear_and_ordered(pt1, line[-1], pt2):
                        line.append(new_pt)
                        break

                    # Don't go backwards
                    if len(line) > 1 and line[-2] == new_pt: continue

                    # This point has to be colinear with the endpoints
                    if not colinear_and_ordered(pt1, new_pt, pt2): continue

                    # So here we know that the new point is a new interior point,
                    # is colinear, and in the right direction.
                    made_extension = True
                    line.append(new_pt)
                    break

                if not made_extension: break

            if line[-1] == pt2: return True

        return False


    def degree(self, v):
        """
        Degree of a vertex v.

        EXAMPLE:

            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.degree(u.points.keys()[0])
            2
        """

        return len(self.neighbours(v))

    def can_remove_triangle(self, v):
        """
        We can remove the triangle with vertices [self.corners[v], x, y]
        only if there is precisely one triangle at the 
        point self.corners[v]. (We do this to ensure that deletion of a 
        triangle leaves a convex shape.)

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.can_remove_triangle(0)
            True
        """

        return len(self.points[self.corners[v]]) == 1

    def remove_triangle(self, v):
        """
        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.triangles
            {((0, 0), (0, 1/2), (1/2, 0)): True, ((0, 1/2), (0, 1), (1/2, 1/2)): True, ((1/2, 0), (1/2, 1/2), (1, 0)): True, ((0, 1/2), (1/2, 0), (1/2, 1/2)): True}
            sage: u.remove_triangle(0)
            sage: u.triangles
            {((0, 1/2), (0, 1), (1/2, 1/2)): True, ((1/2, 0), (1/2, 1/2), (1, 0)): True, ((0, 1/2), (1/2, 0), (1/2, 1/2)): True}
        """

        assert self.can_remove_triangle(v)
        assert 0 <= v < len(self.corners)

        triangle_to_remove = tuple(sorted(self.points[self.corners[v]][0]))

        prev_vertex = self.previous_vertex(v)
        next_vertex = self.next_vertex(v)
        self.corners.insert(v, prev_vertex)
        self.corners[v+1] = next_vertex

        i = 0
        while i < len(self.corners) - 1:
            if self.corners[i] == self.corners[i+1]:
                del self.corners[i+1]
                continue
            else:
                i += 1
        while self.corners[0] == self.corners[-1]:
            del self.corners[-1]

        # Remove the triangle from the dictionary of points and if there are
        # no triangles left at a point, remove that entry from the
        # dictionary.
        for i in range(3):
            p = triangle_to_remove[i]
            self.points[p].remove(triangle_to_remove)
            if len(self.points[p]) == 0: del self.points[p]

        del self.triangles[triangle_to_remove]

    def core(self):
        """
        Try to remove all outer triangles of the dissection.

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2), (1, -1, 0), (-1, 2, 1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 0), (0, -1, 1), (-1, 1, 2)]))
            sage: u = TriangleDissection(U1, U2, id_row = 0, id_col = 0, only_separated_solutions = False)
            sage: u.points
            {(0, 1): [((0, 1/2), (0, 1), (1/2, 1/2))], (0, 0): [((0, 0), (0, 1/2), (1/2, 0))], (1/2, 1/2): [((0, 1/2), (0, 1), (1/2, 1/2)), ((1/2, 0), (1/2, 1/2), (1, 0)), ((0, 1/2), (1/2, 0), (1/2, 1/2))], (1/2, 0): [((0, 0), (0, 1/2), (1/2, 0)), ((1/2, 0), (1/2, 1/2), (1, 0)), ((0, 1/2), (1/2, 0), (1/2, 1/2))], (0, 1/2): [((0, 0), (0, 1/2), (1/2, 0)), ((0, 1/2), (0, 1), (1/2, 1/2)), ((0, 1/2), (1/2, 0), (1/2, 1/2))], (1, 0): [((1/2, 0), (1/2, 1/2), (1, 0))]}
            sage: u.core()
            sage: u.points
            {(1/2, 1/2): [((1/2, 0), (1/2, 1/2), (1, 0))], (1/2, 0): [((1/2, 0), (1/2, 1/2), (1, 0))], (1, 0): [((1/2, 0), (1/2, 1/2), (1, 0))]}
        """

        while True:
            if len(self.triangles) == 1: return

            i = 0
            while i < len(self.corners):
                if self.can_remove_triangle(i): break
                i += 1

            if i == len(self.corners): return

            self.remove_triangle(i)

    def write_PDF(self, filename, draw_border = False, draw_labels = False, mark_unit_length = False, mark_points = [], draw_sizes = False):
        """
        EXAMPLE:
            sage: from triangle_dissections import *
            sage: U1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
            sage: U2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
            sage: u = TriangleDissection(U1, U2, id_row = 2, id_col = 3, only_separated_solutions = False)
            sage: file1 = tmp_filename()
            sage: file2 = tmp_filename()
            sage: u.write_PDF(file1)
            sage: u.write_PDF(file2, draw_labels = True)
            sage: os.remove(file1 + ".pdf") # .pdf extension is automatically added
            sage: os.remove(file2 + ".pdf")
        """

        canv = pyx.canvas.canvas()

        if False:
            canv.stroke(pyx.path.line(0, 0, 0, 1), [pyx.style.linewidth.THin])
            canv.stroke(pyx.path.line(0, 0, 1, 0), [pyx.style.linewidth.THin])
            canv.stroke(pyx.path.line(0, 1, 1, 0), [pyx.style.linewidth.THin])

        if False:
            for i in range(len(self.corners)):
                canv.stroke(pyx.path.line(self.corners[-i][0], 
                    self.corners[-i][1],
                    self.corners[-i-1][0], 
                    self.corners[-i-1][1]), 
                    [pyx.color.rgb.black])

        for t in self.triangles.keys():
            canv.stroke(pyx.path.line(t[0][0], t[0][1], t[1][0], t[1][1]), 
                [pyx.style.linewidth.THin])
            canv.stroke(pyx.path.line(t[1][0], t[1][1], t[2][0], t[2][1]), 
                [pyx.style.linewidth.THin])
            canv.stroke(pyx.path.line(t[2][0], t[2][1], t[0][0], t[0][1]), 
                [pyx.style.linewidth.THin])

        if draw_labels:
            horizontal_lines, vertical_lines, diagonal_lines = self.lines_of_trade()

        horizontal_lines, vertical_lines, diagonal_lines = self.lines_of_trade()

        delta1 = 0.1
        delta2 = 0.2

        label_points_r = {}
        label_points_c = {}
        label_points_s = {}

        if draw_labels:
            for (y, y_label) in horizontal_lines.items():
                canv.stroke(pyx.path.line(-delta1, y, -delta2, y), [pyx.style.linewidth.THin])
                label_points_r[(-0.3, y)] = r"r_" + str(y_label)

            for (x, x_label) in vertical_lines.items():
                canv.stroke(pyx.path.line(x, 1 + delta1 - x, x, 1 + delta2 - x), [pyx.style.linewidth.THin])
                label_points_c[(x, 1 + delta2 + 0.05 - x)] = r"c_" + str(x_label)

            blah = 0.1
            bloop = 0.1

            for (x, x_label) in diagonal_lines.items():
                canv.stroke(pyx.path.line(x+bloop, -bloop, x + bloop + blah, -bloop -blah), [pyx.style.linewidth.THin])
                label_points_s[(x + 1.5*bloop + blah, -1.5*bloop -blah)] = r"s_" + str(x_label)

        #for x in range(int(self.n)+1):
            #canv.fill(mark(x/self.n, 0))
            #canv.fill(mark(0, x/self.n))
            #canv.fill(mark(1.0 - x/self.n, x/self.n))

        large_canvas = pyx.canvas.canvas()

        # Uncomment one of these:

        # (1) Triangle with right angle at bottom-left:
        #to_equilateral = pyx.trafo.trafo(((1, 0), (0, 1)))

        # (2) Equilateral triangle:
        to_equilateral = pyx.trafo.trafo(((1, 0.5), (0, math.sqrt(3)/2.0)))

        scale_factor = 5

        large_canvas.insert(canv, 
            [pyx.trafo.scale(sx=scale_factor, sy=scale_factor),
             to_equilateral])

        try:
            if len(self.six_way_points) > 0:
                for z in label_points_c.keys():
                    if self.separated_columns.has_key(int(label_points_c[z][2:])):
                        label_points_c[z] += "/c_" + str(self.separated_columns[int(label_points_c[z][2:])])
                for z in label_points_s.keys():
                    if self.separated_symbols.has_key(int(label_points_s[z][2:])):
                        label_points_s[z] += "/s_" + str(self.separated_symbols[int(label_points_s[z][2:])])

        except AttributeError:
            pass # no separated column or symbol...


        if draw_labels:
            for (pt, lab) in label_points_r.items():
                new0, new1 = to_equilateral.scaled(sx=scale_factor, sy=scale_factor).apply_pt(pt[0], pt[1])
                large_canvas.text(new0, new1, lab, [pyx.text.mathmode,pyx.text.valign.middle])

            for (pt, lab) in label_points_c.items():
                new0, new1 = to_equilateral.scaled(sx=scale_factor, sy=scale_factor).apply_pt(pt[0], pt[1])
                large_canvas.text(new0, new1, lab, [pyx.text.mathmode,pyx.text.halign.center])

            for (pt, lab) in label_points_s.items():
                new0, new1 = to_equilateral.scaled(sx=scale_factor, sy=scale_factor).apply_pt(pt[0], pt[1])
                large_canvas.text(new0, new1, lab, [pyx.text.mathmode,pyx.text.halign.right])

        if mark_unit_length:
            for m in range(self.n + 1):
                x, y = to_equilateral.apply_pt(scale_factor*m/float(self.n), 0)
                large_canvas.fill(mark(x, y))

                x, y = to_equilateral.apply_pt(0, scale_factor*m/float(self.n))
                large_canvas.fill(mark(x, y))

                x, y = to_equilateral.apply_pt(scale_factor*(1.0-m/float(self.n)),
                                               scale_factor*m/float(self.n))
                large_canvas.fill(mark(x, y))

        for (u, v) in mark_points:
            x, y = to_equilateral.apply_pt(scale_factor*u, scale_factor*v)
            large_canvas.fill(mark(x, y))

        if draw_sizes:
            for t in self.triangles.iterkeys():
                # fixme writing triangle size in interior.
                cent = centroid_of_triangle(t[0], t[1], t[2])
                x, y = to_equilateral.apply_pt(scale_factor*cent[0], scale_factor*cent[1])

                tsize = self.n * horizontal_length(t[0], t[1], t[2])

                large_canvas.text(x, y, str(tsize), [pyx.text.vshift.middlezero, pyx.text.halign.center, pyx.text.size.tiny])


        large_canvas.writePDFfile(filename)
        #large_canvas.writeEPSfile(filename + r".eps")

    def canonical_signature(self):
        """
        To determine the canonical signature of a triangle dissection
        we take the set of points (as an equilateral triangle) and then find
        the image under the symmetry group (three reflections and two
        rotations). We then sort the images and select the lexicographically
        least as the canonical signature.

        EXAMPLE:
            sage: from triangle_dissections import *
            sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
            sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
            sage: assert is_bitrade(T1, T2)
            sage: t53 = TriangleDissection(T1, T2, 5, 3, only_separated_solutions = False)
            sage: t53.canonical_signature()
            ((0, 0),
             (11/78, 11*3**(1/2)/78),
             (19/78, 19*3**(1/2)/78),
             (11/39, 0),
             (9/26, 11*3**(1/2)/78),
             (5/13, 7*3**(1/2)/39),
             (31/78, 3*3**(1/2)/26),
             (11/26, 7*3**(1/2)/78),
             (11/26, 11*3**(1/2)/78),
             (35/78, 3*3**(1/2)/26),
             (35/78, 19*3**(1/2)/78),
             (1/2, 3**(1/2)/2),
             (20/39, 0),
             (20/39, 7*3**(1/2)/39),
             (47/78, 7*3**(1/2)/78),
             (59/78, 19*3**(1/2)/78),
             (1, 0))
        """

        def has_sqrt3_term(x):
            """
            Does x contain a factor of sqrt(3)?
            """

            return '**' in str(x)
            return not x.is_Rational and (x/sympy.sqrt(3)).is_Rational

        def vertex_to_list(v):
            assert len(v) == 2
            x, y = v

            if has_sqrt3_term(x):
                x = [0, x/(sympy.sqrt(3))]
            else:
                x = [x, 0]

            if has_sqrt3_term(y):
                y = [0, y/(sympy.sqrt(3))]
            else:
                y = [y, 0]

            return x + y

        def image_to_sorted_lists(image):
            new_image = []

            for (pt1, pt2, pt3) in image:
                this_triangle = [vertex_to_list(pt1), vertex_to_list(pt2), vertex_to_list(pt3),]
                #print 'this_triangle:             ', this_triangle
                this_triangle.sort()
                #print 'this_triangle (after sort):', this_triangle
                new_image.append(sum(this_triangle, []))

            new_image.sort()

            return sum(new_image, [])

        images = []

        # Equilateral triangle:
        # images.append([(y/2 + x, sympy.sqrt(3)*y/2) for (x, y) in [(sympy.Rational(str(x)), sympy.Rational(str(y))) for (x,y) in self.points.iterkeys()]])

        images.append([])

        for t in self.triangles.iterkeys():
            new_triangle = []

            for (x, y) in t: # 3 points
                x = sympy.Rational(str(x))
                y = sympy.Rational(str(y))
                x, y = (y/2 + x, sympy.sqrt(3)*y/2)
                new_triangle.append((x, y))

            images[0].append(new_triangle)

        assert len(images[0]) == len(self.triangles)

        for fn in [reflect1, reflect2, reflect3, rotate_equilateral, rotate_equilateral_inverse]:
            images.append([])

            for t in images[0]:
                images[-1].append([fn(x, y) for (x, y) in t])

        assert len(images) == 6
        for im in images: assert len(im) == len(images[0])

        images = [image_to_sorted_lists(im) for im in images]
        images.sort()

        return tuple(images[0])


    def is_perfect_dissection(self):
        """
        From http://www.squaring.net/tri/twt.html

            The authors of "The Dissection of Rectangles into Squares" proved
            that an equilateral triangle cannot be dissected into equilateral
            triangles all of different sizes (orientation ignored). At least two
            triangles will be of the same size. See David Radcliffe's post for
            a proof. However equilateral triangles can tile in an up direction
            or a down direction, if these are considered different as they are
            not congruent, even if at the same size, then a kind of 'perfect'
            tiling is possible.

        EXAMPLE:

        This is the first bitrade that gives a perfect dissection:

            sage: from triangle_dissections import *
            sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
            sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
            sage: assert is_bitrade(T1, T2)
            sage: t53 = TriangleDissection(T1, T2, 5, 3, only_separated_solutions = False)
            sage: sorted(t53.triangles.keys())
            [((0, 0), (0, 20/39), (20/39, 0)),
             ((0, 20/39), (0, 28/39), (8/39, 20/39)),
             ((0, 20/39), (8/39, 4/13), (8/39, 20/39)),
             ((0, 28/39), (0, 1), (11/39, 28/39)),
             ((0, 28/39), (11/39, 17/39), (11/39, 28/39)),
             ((8/39, 4/13), (8/39, 17/39), (1/3, 4/13)),
             ((8/39, 4/13), (20/39, 0), (20/39, 4/13)),
             ((8/39, 17/39), (8/39, 20/39), (11/39, 17/39)),
             ((8/39, 17/39), (1/3, 4/13), (1/3, 17/39)),
             ((11/39, 17/39), (11/39, 19/39), (1/3, 17/39)),
             ((11/39, 19/39), (11/39, 28/39), (20/39, 19/39)),
             ((11/39, 19/39), (1/3, 17/39), (1/3, 19/39)),
             ((1/3, 4/13), (1/3, 19/39), (20/39, 4/13)),
             ((1/3, 19/39), (20/39, 4/13), (20/39, 19/39)),
             ((20/39, 0), (20/39, 19/39), (1, 0))]
            sage: assert t53.is_perfect_dissection()
        """

        triangle_sizes = {}

        for (pt1, pt2, pt3) in self.triangles.iterkeys():
            this_size = self.n*horizontal_length(pt1, pt2, pt3)

            if not up_triangle(pt1, pt2, pt3):
                this_size = -this_size

            if triangle_sizes.has_key(this_size): return False
            triangle_sizes[this_size] = True

        return True

def is_separated_solution(row_max, col_max, sym_max, M):
    """
    EXAMPLES:

        sage: from triangle_dissections import *
        sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
        sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
        sage: assert is_bitrade(T1, T2)

        sage: row_max, col_max, sym_max, M = trade_dissection_matrix(T1, 5, 3)
        sage: M = M.echelon_form().column(-1)
        sage: is_separated_solution(row_max, col_max, sym_max, M)
        True
    """

    if len(uniq(M[0:row_max])) != row_max: return False
    if len(uniq(M[row_max:row_max+col_max])) != col_max: return False
    if len(uniq(M[row_max+col_max:])) != sym_max: return False

    return True

def find_solution(T1, id_row, id_col, only_separated_solutions):
    """
    EXAMPLES:

        sage: from triangle_dissections import *
        sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
        sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
        sage: assert is_bitrade(T1, T2)

        sage: find_solution(T1, 5, 3, only_separated_solutions = True)
        (6, 5, 6, 5, 3, (17/39, 4/13, 20/39, 28/39, 19/39, 0, 8/39, 11/39, 1/3, 0, 20/39, 25/39, 28/39, 10/13, 20/39, 1, 32/39))
    """

    assert id_row is not None
    assert id_col is not None

    assert T1[id_row, id_col] >= 0

    row_max, col_max, sym_max, M = trade_dissection_matrix(T1, id_row, id_col)
    M = M.echelon_form().column(-1)

    if only_separated_solutions and (not is_separated_solution(row_max, col_max, sym_max, M)):
        raise ValueError, "no separated solution at " + str(id_row) + ", " + str(id_col)
    else:
        return row_max, col_max, sym_max, id_row, id_col, M

def trade_dissection_matrix(T, id_row, id_col):
    """
    EXAMPLES:

        sage: from triangle_dissections import *
        sage: T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
        sage: T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))
        sage: assert is_bitrade(T1, T2)
        sage: trade_dissection_matrix(T1, 5, 3)
        (6, 5, 6, [ 1  0  0  0  0  0  1  0  0  0  0 -1  0  0  0  0  0  0]
        [ 1  0  0  0  0  0  0  1  0  0  0  0 -1  0  0  0  0  0]
        [ 1  0  0  0  0  0  0  0  1  0  0  0  0 -1  0  0  0  0]
        [ 0  1  0  0  0  0  1  0  0  0  0  0  0  0 -1  0  0  0]
        [ 0  1  0  0  0  0  0  0  1  0  0 -1  0  0  0  0  0  0]
        [ 0  1  0  0  0  0  0  0  0  0  1  0  0  0  0  0 -1  0]
        [ 0  0  1  0  0  0  1  0  0  0  0  0 -1  0  0  0  0  0]
        [ 0  0  1  0  0  0  0  0  0  1  0  0  0  0 -1  0  0  0]
        [ 0  0  0  1  0  0  0  1  0  0  0  0  0  0  0 -1  0  0]
        [ 0  0  0  1  0  0  0  0  0  1  0  0 -1  0  0  0  0  0]
        [ 0  0  0  0  1  0  0  1  0  0  0  0  0 -1  0  0  0  0]
        [ 0  0  0  0  1  0  0  0  1  0  0  0  0  0  0  0 -1  0]
        [ 0  0  0  0  1  0  0  0  0  0  1  0  0  0  0 -1  0  0]
        [ 0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  1]
        [ 0  0  0  0  0  1  0  0  0  0  1  0  0  0 -1  0  0  0])
    """


    assert T[id_row, id_col] >= 0

    row_max, col_max, sym_max = T.actual_row_col_sym_sizes()

    rows = []

    id_sym = T[id_row, id_col]

    # A column is all zeros by default, and we cut out
    # the identity row and identity column, but then we add
    # a column for the rhs.
    nr_columns = row_max+col_max+sym_max+1

    for r in range(row_max):
        for c in range(col_max):
            s = T[r, c]
            if s < 0: continue

            if r == id_row and c == id_col and s == id_sym:
                # here we have the equations
                # id_row = id_col = 0, id_sym = 1.
                new_row = nr_columns*[0]
                new_row[id_row] = 1                
                rows.append(new_row)

                new_row = nr_columns*[0]
                new_row[id_col + row_max] = 1                
                rows.append(new_row)

                new_row = nr_columns*[0]
                new_row[id_sym + row_max + col_max] = 1                
                new_row[-1] = 1                
                rows.append(new_row)

                continue

            new_row = nr_columns*[0]

            new_row[r] = 1
            new_row[c + row_max] = 1
            new_row[s + row_max+col_max] = -1

            rows.append(new_row)

    return row_max, col_max, sym_max, matrix(QQ, rows)

def mark(x, y):
    """

    EXAMPLES:
        sage: from triangle_dissections import *
        sage: str(mark(0, 0))
        'path(moveto_pt(2.83465, 0), arc_pt(0, 0, 2.83465, 0.1, 359.9), closepath())'
    """

    return pyx.path.circle(x, y, 0.1)

if False and __name__ == "__main__":
    T1 = LatinSquare(Matrix(ZZ, [(0, 1, 2, -1, -1, -1), (3, -1, 0, -1, 5, -1), (1, -1, -1, 3, -1, -1), (-1, 4, -1, 1, -1, -1), (-1, 2, 5, -1, 4, -1), (-1, -1, -1, 4, 3, -1)]))
    T2 = LatinSquare(Matrix(ZZ, [(1, 2, 0, -1, -1, -1), (0, -1, 5, -1, 3, -1), (3, -1, -1, 1, -1, -1), (-1, 1, -1, 4, -1, -1), (-1, 4, 2, -1, 5, -1), (-1, -1, -1, 3, 4, -1)]))

    assert is_bitrade(T1, T2)

    # One of these is Tutte's example?
    t53 = TriangleDissection(T1, T2, 5, 3, only_separated_solutions = False)
    t54 = TriangleDissection(T1, T2, 5, 4, only_separated_solutions = False)

    t53.write_PDF("t53.pdf", draw_sizes = True)
    t54.write_PDF("t54.pdf", draw_sizes = True)

if __name__ == "__main__":
    b = some_spherical_bitrades()

    for i in range(10):
        T1, T2 = b[i]

        for r, c in cross(range(T1.nrows()), range(T1.ncols())):
            if T1[r, c] < 0: continue

            try:
                t = TriangleDissection(T1, T2, r, c, only_separated_solutions = False)
            except ValueError:
                continue # there was no (separated?) solution

            if len(t.six_way_points) > 0:
                print T1.square.rows()
                print
                print T2.square.rows()
                print r, c
                sys.exit(0)
            continue

            t.generate_bitrade_via_geometric_data()

            print "Saving dissection" + str(i) + "_r" + str(r) + "_c" + str(c) + ".pdf"
    
            t.write_PDF("dissection" + str(i) + "_r" + str(r) + "_c" + str(c) + ".pdf", draw_labels = True)

