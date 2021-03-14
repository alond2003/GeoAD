from geo.problem import Problem
from geo.helper import Helper
from geo.real.expression import Degree


def p349_e1():
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
    return (x,), (50,)


def p349_e2():
    h = Helper()
    h.ps("ABCD", [-4, 4, 0, 3], [0, 0, 0, 3])
    h.s("ACB", "CD")
    x = h.given(Degree, "x")
    h.seta("ACD", 3 * x)
    h.seta("DCB", x)
    h.calc()
    return (x, h.geta("ACD")), (45, 135)


def p349_e3():
    h = Helper()
    h.ps("ABCD", [-4, 4, 0, 3], [0, 0, 0, 3])
    h.s("ACB", "CD")
    x = h.given(Degree, "x")
    h.seta("ACD", x + 48)
    h.seta("DCB", x)
    h.calc()
    return (h.geta("DCB"), h.geta("ACD")), (66, 114)


def p349_e4():
    h = Helper()
    h.ps("ABCDE", [-4, 0, 4, 3, -3], [0, 0, 0, 3, -3])
    h.s("ABC", "DBE")
    h.equala("EBA", "DBC")
    h.calc()
    return (h.geta("DBE"),), (180,)


def p349_e5():
    h = Helper()
    h.ps("ABCDEFG", [-4, 4, 3, -3, 0, -2, 2], [0, 0, 3, -3, 0, 4, -4])
    h.s("AEB", "CED", "FEG")
    h.equala("AEF", "FEC")
    h.calc()
    return (h.geta("BEG") == h.geta("GED"),), (True,)


def p349_e6():
    h = Helper()
    h.ps("ABC", [4, 0, 8], [6, 0, 0])
    h.tri("ABC")
    x = h.given(Degree, "x")
    h.seta("CAB", 7 * x)
    h.seta("ABC", 5 * x)
    h.seta("BCA", 3 * x)
    h.calc()
    return (h.geta("CAB"), h.geta("ABC"), h.geta("BCA")), (84, 60, 36)


def p349_e7():
    h = Helper()
    h.ps("ABC", [0, 0, 8], [6, 0, 0])
    h.tri("ABC")
    h.seta("ABC", 90)
    x = h.given(Degree, "x")
    h.seta("CAB", x)
    h.seta("BCA", x + 40)
    h.calc()
    return (h.geta("CAB"), h.geta("BCA")), (25, 65)


print(p349_e7())