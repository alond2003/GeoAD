import math
from geo.abs.point import Point
from geo.abs.abssegment import AbsSegment
from geo.handler import Handler
from geo.real.expression import Degree
from geo.abs.absangle import AbsAngle
from geo.helper import Helper
from geo.filehandler import print_points_from_file


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

    AI = AbsSegment(A, I, True)
    CG = AbsSegment(C, G, True)
    DF = AbsSegment(D, F, True)
    BH = AbsSegment(B, H, True)

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


def try_solve_problem_using_coor_system():
    """with Helper object"""

    # with helper
    h = Helper()
    x = Degree.given("x")
    h.p("A", -4, 0)
    h.p("B", 6, 0)
    h.p("C", 4, 4)
    h.p("D", -4, -2)
    h.p("E", -1.33, 0)
    h.s("AEB", "CED")
    h.seta("AEC", 2 * x + 40)
    h.seta("BED", x + 90)
    h.calc()
    print(x)

    """ without helper
        A = Point("A", -4, 0)
        B = Point("B", 6, 0)
        C = Point("C", 4, 4)
        D = Point("D", -4, -2)
        E = Point("E", -1.33, 0)
        AB = AbsSegment(A, B, True)
        AB.set_midpoints(E)
        CD = AbsSegment(C, D, True)
        CD.set_midpoints(E)
        geo = Handler(A, B, C, D, E)
        geo.init_angles()
        AE = AB.get_subsegment("AE")
        CE = CD.get_subsegment("CE")
        AEC = AbsAngle(AE, E, CE)
        geo.abs_equal_exp(AEC, 2 * x + 40, "known")
        BED = AbsAngle(AB.get_subsegment("BE"), E, CD.get_subsegment("DE"))
        geo.abs_equal_exp(BED, x + 90, "known")
        geo.calc(inita=False)
        print(x)
    """


def ggb_test():

    path = r"ggb_test\geogebra-export.ggb"
    from time import perf_counter

    start = perf_counter()
    print_points_from_file(path)
    end = perf_counter()
    print(end - start)


# test_segment_ordering_inside_point_lines_arr()
# try_solve_problem_using_coor_system()
ggb_test()
