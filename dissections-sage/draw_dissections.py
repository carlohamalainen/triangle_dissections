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

import sage.all
from sage.all import Rational

import sympy

from triangle_dissections import *
from bbitrade import *

def to_latex(P, op_sym, t):
    """
    Provide a nice LaTeX rendering of a trade P, with operation
    symbol op_sym, and associated triangle dissection t. Note that
    we must run generate_bitrade_via_geometric_data() before using
    this method as we need the attribute max_triangle_row_label, etc.

    EXAMPLE::

        sage: from triangle_dissections import *
        sage: T1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
        sage: T2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
        sage: t = TriangleDissection(T1, T2, id_row = 2, id_col = 3, only_separated_solutions = False)
        sage: t.generate_bitrade_via_geometric_data()
        sage: print to_latex(T1, "\\ast", t)
        \begin{array}{|c||c|c|c|c|}
        \hline \ast & c_0 & c_1 & c_2 & c_3\\
        \hline \hline r_0 & s_0 & s_1 & s_2 & s_3\\\hline r_1 & s_1 & ~ & ~ & s_0\\\hline r_2 & ~ & s_2 & s_3 & s_1\\\hline\end{array}
    """

    a = ""
    a += r"\begin{array}{" + r"|c|" + P.ncols()*"|c" + "|}" + '\n'

    a += r"\hline "
    a += op_sym + r" & "

    nr_rows = t.max_triangle_row_label
    nr_cols = t.max_triangle_col_label

    for c in range(nr_cols):
        a += r"c_" + str(c)
        if c < nr_cols-1: a += " & "
        else: a += r"\\" + '\n'

    a += r"\hline "
    
    for r in range(nr_rows):
        a += r"\hline " + r"r_" + str(r) + r" & "
        for c in range(nr_cols):
            s = P[r, c]

            if s < 0: a += "~"
            else: a += r"s_" + str(s)

            if c < nr_cols-1: a += " & "
            else: a += "\\\\"
    a += r"\hline"
    a += r"\end{array}"
    return a

def print_bitrade(T1, T2, t):
    """
    Provide a nice LaTeX rendering of a bitrade (T1, T2), with
    associated triangle dissection t. Note that we must run
    generate_bitrade_via_geometric_data() before using this method
    as we need the attribute max_triangle_row_label, etc.

    EXAMPLE::

        sage: from triangle_dissections import *
        sage: T1 = LatinSquare(matrix(ZZ, [(0, 1, 2, 3), (1, -1, -1, 0), (-1, 2, 3, 1), (-1, -1, -1, -1)]))
        sage: T2 = LatinSquare(matrix(ZZ, [(1, 2, 3, 0), (0, -1, -1, 1), (-1, 1, 2, 3), (-1, -1, -1, -1)]))
        sage: t = TriangleDissection(T1, T2, id_row = 2, id_col = 3, only_separated_solutions = False)
        sage: t.generate_bitrade_via_geometric_data()
        sage: print_bitrade(T1, T2, t)
        '\\[ T^{\\ast},\\, T^{\\triangle} =\\begin{array}{|c||c|c|c|c|}\n\\hline \\ast & c_0 & c_1 & c_2 & c_3\\\\\n\\hline \\hline r_0 & s_0 & s_1 & s_2 & s_3\\\\\\hline r_1 & s_1 & ~ & ~ & s_0\\\\\\hline r_2 & ~ & s_2 & s_3 & s_1\\\\\\hline\\end{array}\\phantom{x}\\begin{array}{|c||c|c|c|c|}\n\\hline \\triangle & c_0 & c_1 & c_2 & c_3\\\\\n\\hline \\hline r_0 & s_1 & s_2 & s_3 & s_0\\\\\\hline r_1 & s_0 & ~ & ~ & s_1\\\\\\hline r_2 & ~ & s_1 & s_2 & s_3\\\\\\hline\\end{array}\\]'
    """

    a = ""
    a += r"\[ T^{\ast},\, T^{\triangle} ="
    a += to_latex(T1, r"\ast", t)
    a += "\\phantom{x}"
    a += to_latex(T2, r"\triangle", t)
    a += "\\]"
    return a

def reflect1(x, y):
    """
    One of the symmetries of an equilateral triangle. This is
    reflection along the line x = 1/2 (fixing the top vertex
    (1/2, 1/2*sqrt(3))).

    EXAMPLE::

        sage: reflect1(1, 0)
        (0, 0)
        sage: reflect1(sympy.Rational(1, 2), 0)
        (1/2, 0)
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
    The reflection of the equilateral triangle with vertices (0, 0),
    (1, 0), (1/2, 1/2*sqrt(3)) that fixes (0, 0).

    EXAMPLES:
        sage: from draw_dissections import *
        sage: reflect2(0, 0)
        (0, 0)
    """

    x, y = rotate_equilateral_inverse(x, y)
    x, y = reflect1(x, y)
    return rotate_equilateral(x, y)

def reflect3(x, y):
    """
    The reflection of the equilateral triangle with vertices (0, 0),
    (1, 0), (1/2, 1/2*sqrt(3)) that fixes (1, 0).

    EXAMPLES:
        sage: from draw_dissections import *
        sage: reflect3(1, 0)
        (1, 0)
    """

    x, y = rotate_equilateral(x, y)
    x, y = reflect1(x, y)
    return rotate_equilateral_inverse(x, y)

def rotate_equilateral(x, y, theta = 2*sympy.pi/3):
    """
    Rotate the equilateral triangle anticlockwise around point
    (x, y) by angle theta.

    EXAMPLES:
        sage: from draw_dissections import *
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
        sage: from draw_dissections import *
        sage: rotate_equilateral_inverse(0, 0)
        (1/2, 1/2*sqrt(3))
    """
    return rotate_equilateral(x, y, theta = -2*sympy.pi/3)

def canonical_signature(_points):
    assert False
