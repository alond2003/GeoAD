import math
from geo.abs.point import Point
from geo.abs.segment import Segment
from geo.handler import Handler
from geo.real.expression import Degree
from geo.abs.absangle import AbsAngle
from geo.helper import Helper
from geo.problem import Problem
from geo.filehandler import get_points_from_file


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


def try_solve_problem_using_coor_system():
    """with Problem object"""

    p = Problem(349, 1)

    def create():
        h = Helper()
        x = h.given(Degree, "x")
        h.p("A", -4, 0)
        h.p("B", 6, 0)
        h.p("C", 4, 4)
        h.p("D", -4, -2)
        h.p("E", -1.33, 0)
        h.s("AEB", "CED")
        h.seta("AEC", 2 * x + 40)
        h.seta("BED", x + 90)
        h.calc()
        return h

    answer = lambda h, _: str(h.given(Degree, "x"))
    cur_ans = lambda _: "50"

    p.set_functions(create, answer, cur_ans)

    print(p.answer(), p.currect_answer(), p.answer() == p.currect_answer())

    """ with helper
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
    """
    """ without helper
        A = Point("A", -4, 0)
        B = Point("B", 6, 0)
        C = Point("C", 4, 4)
        D = Point("D", -4, -2)
        E = Point("E", -1.33, 0)
        AB = Segment(A, B, True)
        AB.set_midpoints(E)
        CD = Segment(C, D, True)
        CD.set_midpoints(E)
        geo = Handler(A, B, C, D, E)
        geo.init_angles()
        AE = AB.get_subsegment("AE")
        CE = CD.get_subsegment("CE")
        AEC = AbsAngle(AE, E, CE)
        geo.aang_equal_deg(AEC, 2 * x + 40, "known")
        BED = AbsAngle(AB.get_subsegment("BE"), E, CD.get_subsegment("DE"))
        geo.aang_equal_deg(BED, x + 90, "known")
        geo.calc(inita=False)
        print(x)
    """


def ggb_test():

    path = r"C:\Users\alond\Documents\School\AvodatGemer\AvodatGemerCode\ggb_test\geogebra-export.ggb"
    from time import perf_counter

    start = perf_counter()
    print(get_points_from_file(path))
    end = perf_counter()
    print(end - start)


# test_segment_ordering_inside_point_lines_arr()
# try_solve_problem_using_coor_system()
ggb_test()
