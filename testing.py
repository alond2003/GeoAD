import math
from geo.abs.point import Point
from geo.abs.segment import Segment


def test_segment_ordering_inside_point_lines_arr():

    A = Point("A", -1, 1)
    B = Point("B", 0, 1)
    C = Point("C", 1, 1)
    D = Point("D", -1, 0)
    E = Point("E", 0, 0)
    F = Point("F", 1, 0)
    G = Point("G", -1, -1)
    H = Point("H", 0, -1)
    I = Point("I", 1, -1)

    AI = Segment(A, I, True)
    CG = Segment(C, G, True)
    DF = Segment(D, F, True)
    BH = Segment(B, H, True)

    arr = [AI, CG, DF, BH]

    for i in arr:
        i.set_midpoints(E)

    print(E.lines)
    print(len(E.lines))
    for line, _ in E.lines:
        print(f"{line} {(line.get_slope_angle(E))}")

    """
    A B C
    D E F
    G H I
    """


test_segment_ordering_inside_point_lines_arr()
