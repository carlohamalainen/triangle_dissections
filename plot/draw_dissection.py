from fractions import Fraction
from math import sqrt
import sys
import pyx


counter = 0

for line in sys.stdin.readlines():
    sig = line.split()

    assert len(sig) % 12 == 0
    nr_triangles = len(sig)/12

    triangles = [sig[12*i:12*(i+1)] for i in range(nr_triangles)]

    triangle_corners = []

    for triangle in triangles:
        assert len(triangle) == 12

        points = [triangle[4*i:4*(i+1)] for i in range(3)]

        triangle_points_f = []

        for point in points:
            assert len(point) == 4

            x = float(Fraction(point[0])) + sqrt(3)*float(Fraction(point[1]))
            y = float(Fraction(point[2])) + sqrt(3)*float(Fraction(point[3]))

            triangle_points_f.append((x, y))

        triangle_corners.append(triangle_points_f)

    canv = pyx.canvas.canvas()

    for t in triangle_corners:
        canv.stroke(pyx.path.line(t[0][0], t[0][1], t[1][0], t[1][1]), [pyx.style.linewidth.THin])
        canv.stroke(pyx.path.line(t[1][0], t[1][1], t[2][0], t[2][1]), [pyx.style.linewidth.THin])
        canv.stroke(pyx.path.line(t[2][0], t[2][1], t[0][0], t[0][1]), [pyx.style.linewidth.THin])

    # Make the corners look closed.
    canv.stroke(pyx.path.path(pyx.path.moveto(0, 0), pyx.path.lineto(1, 0), pyx.path.lineto(1.0/2, sqrt(3)/2.0), pyx.path.closepath()), [pyx.style.linewidth.THin])

    large_canvas = pyx.canvas.canvas()

    scale_factor = 5

    large_canvas.insert(canv, [pyx.trafo.scale(sx=scale_factor, sy=scale_factor)])

    filename = 'n%d_sig_%d.pdf' % (len(triangles), counter) # 'n%d_sig_%s.pdf' % (len(triangles), '_'.join(sig).replace('/', 'd'))
    large_canvas.writePDFfile(filename)
    print filename

    counter += 1

