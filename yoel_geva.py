from point import Point
from segment import Segment
from realangle import RealAngle
from absangle import AbsAngle
from geohandler import GeoHandler
from degree import Degree
from helper import Helper


def p349_e1():
    h = Helper()
    h.s("AEB")
    h.s("CED")
    h.g().init_angles()
    x = Degree()
    x.watch()
    h.g().angles[h.a("BED")].set_value(x + 90)
    h.g().angles[h.a("AEC")].set_value(2 * x + 40)
    h.g().angles_calc(False)
    # print(h.g().angles)
    return x


def p349_e2():
    h = Helper()
    h.s("ACB")
    h.s("CD")
    h.inita()
    x = Degree()
    h.seta("DCB", x)
    h.seta("ACD", 3 * x)
    h.calca()
    # print(h.g().angles)
    return h.geta("DCB"), h.geta("ACD")


def p349_e3():
    h = Helper()
    h.s("ACB")
    h.s("CD")
    h.inita()
    x = Degree()
    h.seta("DCB", x)
    h.seta("ACD", x + 48)
    h.calca()
    # print(h.g().angles)
    return h.geta("DCB"), h.geta("ACD")


def p349_e4():
    h = Helper()
    h.s("BE")
    h.s("ABC")
    h.s("BD")
    h.inita()
    x = Degree()
    h.seta("EBA", x)
    h.seta("DBC", x)
    h.calca()
    # print(h.g().angles)
    return h.geta("EBD")


def p349_e5():
    h = Helper()
    h.s("AEB")
    h.s("FEG")
    h.s("CED")
    h.inita()
    x = Degree()
    h.seta("AEF", x)
    h.seta("FEC", x)
    h.calca()
    # print(h.g().angles)
    return h.geta("BEG") == h.geta("GED")


def p352_e20():
    h = Helper()
    h.s("ACB")
    h.s("CE")
    h.s("DC")
    h.s("FC")
    h.inita()
    h.equala("ACE", "ECD")
    h.equala("DCF", "FCB")
    h.calca()
    # print(h.g().angles)
    return h.geta("ECF")


def p352_e21():
    h = Helper()
    h.s("EB", "AB", "DB", "CB")
    h.seta("ABC", 90)
    h.equala("EBA", "DBC")
    # print(h.g().angles)
    return h.geta("EBD") == Degree(False, 90)


def p352_e23():
    h = Helper()
    h.s("AFB", "CGD", "EFGH")
    x = Degree()
    y = Degree()
    x.watch()
    y.watch()
    h.seta("HFA", x + y)
    h.seta("BFH", 4 * x - 2 * y)
    h.seta("EGD", 60)
    h.paras("AB", "CD")
    h.calca()
    # print(h.g().angles)
    return x, y


print(p349_e1())
