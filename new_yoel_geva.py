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


def p350_e11():
    h = Helper()
    h.ps("ABCDEF", [1, 0, 7, 3, 4, 2.4], [4, 0, 0, 0, 2, 1.2])
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.tri_med("ABC", "AFD")
    h.conts("AC", "AEC")
    h.tri_angbi("ABC", "BFE")
    h.sets("BC", 12)
    h.seta("ABE", Degree(False, {0: 36}))
    h.calc()
    return (h.gets("DC"), h.geta("ABC")), (6, 72)


def p350_e12():
    h = Helper()
    h.ps("ABCD", [0, 2, 6, 4], [0, 4, 0, 2])
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.tri_angbi("ABC", "AD")
    h.seta("ACB", 44)
    h.seta("CBA", 80)
    h.calc()
    return (h.geta("ADB"), h.geta("CDA")), (72, 108)


def p351_e15():
    h = Helper()
    h.ps("ABCDE", [0, 8, 0, 2, 4], [4, 0, 0, 3, 2])
    h.tri("ABC")
    h.conts("AB", "ADEB")
    h.tri_alt("ABC", "CD")
    h.tri_angbi("ABC", "CE")
    h.seta("ACB", 90)
    h.seta("CBA", 26)
    h.calc()
    return h.geta("DCE")


def p351_e17():
    h = Helper()
    h.ps("ABCDEN", [0.0, 6.0, 0.0, 3.0, 3.0, 2.1], [4.0, 0.0, 0.0, 0.0, 2.0, 1.4])
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.conts("AB", "AEB")
    h.tri_alt("ABC", "CNE")
    h.tri_angbi("ABC", "AND")
    h.seta("ACB", 90)
    h.seta("BAC", 34)
    h.calc()
    return (h.geta("DNC"),), (73,)


def p352_e19():
    h = Helper()
    h.ps("ABCDEO", [3.0, 0.0, 6.0, 3.0, 4.488, 3.0], [4.0, 0.0, 0.0, 0.0, 2.016, 2.0])
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.conts("AC", "AEC")
    h.tri_segbi("ABC", "DO", "BC")
    h.tri_segbi("ABC", "EO", "AC")
    h.sets("BD", 6)
    h.sets("AC", 8)
    h.calc()
    return (h.gets("CE"), h.gets("BC"), h.geta("BCA") + h.geta("EOD")), (4, 12, 180)


def p352_e23():
    h = Helper()
    h.ps("ABCDEFGH", [0, 9, 0, 9, 6, 0, 4, 2], [4, 4, 2, 2, 6, 0, 4, 2])
    h.paras("AGB", "CHD")
    h.s("EGHF")
    x, y = h.given(Degree, "x"), h.given(Degree, "y")
    h.seta("FGA", x + y)
    h.seta("BGF", 4 * x - 2 * y)
    h.seta("EHD", 60)
    h.calc()
    return (x, y), (40, 20)


def p352_e24():
    from geo.filehandler import print_points_from_file as pggb

    h = Helper()
    h.ps("ABCDE", [4, 0, 8, 2, 6], [6, 0, 0, 3, 3])
    h.tri("ABC")
    h.conts("AB", "ADB")
    h.conts("AC", "AEC")
    h.s("DE")
    h.paras("DE", "BC")
    h.seta("ABC", 50)
    h.seta("BCA", 60)
    h.calc()
    return (h.geta("ADE"), h.geta("CED")), (50, 120)


print(ans := p352_e24())
print(ans[0] == ans[1])
