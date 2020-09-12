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
    x = Degree.given("x")
    h.seta("BED", x + 90)
    h.seta("AEC", 2 * x + 40)
    h.calc()
    # print(h.g().angles)
    return x


def p349_e2():
    h = Helper()
    h.s("ACB")
    h.s("CD")
    x = Degree().given("x")
    h.seta("DCB", x)
    h.seta("ACD", 3 * x)
    h.calc()
    # print(h.g().angles)
    return h.geta("DCB"), h.geta("ACD")


def p349_e3():
    h = Helper()
    h.s("ACB")
    h.s("CD")
    h.inita()
    x = Degree().given("x")
    h.seta("DCB", x)
    h.seta("ACD", x + 48)
    h.calc()
    # print(h.g().angles)
    return h.geta("DCB"), h.geta("ACD")


def p349_e4():
    h = Helper()
    h.s("BE")
    h.s("ABC")
    h.s("BD")
    x = Degree().given("x")
    h.seta("EBA", x)
    h.seta("DBC", x)
    h.calc()
    # print(h.g().angles)
    return h.geta("EBD")


def p349_e5():
    # print("hello\n" * 1882)
    h = Helper()
    h.s("AEB")
    h.s("FEG")
    h.s("CED")
    # print("yo", h.g().angles)
    h.equala("AEF", "FEC")
    # h.calca()
    # h.inita()
    # print("yo", h.g().angles)
    # print(h.geta("BEG") == h.geta("GED"))
    # print("yo", h.g().angles)
    return h.geta("BEG") == h.geta("GED")


def p352_e20():
    h = Helper()
    h.s("ACB")
    h.s("CE")
    h.s("DC")
    h.s("FC")
    h.equala("ACE", "ECD")
    h.equala("DCF", "FCB")
    # print(h.g().angles)
    return h.geta("ECF")


def p352_e21():
    h = Helper()
    h.s("EB", "AB", "DB", "CB")
    h.seta("ABC", 90)
    h.equala("EBA", "DBC")
    # print(h.g().angles)
    return h.geta("EBD") == 90


def p352_e23():
    h = Helper()
    h.s("AFB", "CGD", "EFGH")
    x = Degree().given("x")
    y = Degree().given("y")
    h.seta("HFA", x + y)
    h.seta("BFH", 4 * x - 2 * y)
    h.seta("EGD", 60)
    h.paras("AB", "CD")
    h.calc()
    # print(h.g().angles)
    return x, y


def p349_e6():
    h = Helper()
    h.tri("BAC")
    x = Degree.given("x")
    h.seta("CAB", 7 * x)
    h.seta("ABC", 5 * x)
    h.seta("BCA", 3 * x)
    # print(h.g().angles)
    return h.geta("CAB"), h.geta("ABC"), h.geta("BCA")


def p349_e7():
    h = Helper()
    h.tri("BAC")
    h.seta("ABC", 90)
    x = Degree.given("x")
    h.seta("CAB", x)
    h.seta("BCA", x + 40)
    return h.geta("CAB"), h.geta("BCA")


def p350_e8():
    h = Helper()
    # A
    h.s("DOC", "AC", "DB", "AOB")
    h.seta("DCA", 34)
    h.seta("CAB", 70)
    h.seta("DBA", 47)
    return h.geta("CDB")
    # B
    # h.s("DOC", "AC", "DB", "AOB")
    # h.calc()
    # return h.geta("DCA") + h.geta("CAB") == h.geta("DBA") + h.geta("CDB")
    # return h.geta("DCA"), h.geta("CAB"), h.geta("DBA"), h.geta("CDB")


arr = [
    p349_e1,
    p349_e2,
    p349_e3,
    p349_e4,
    p349_e5,
    p352_e20,
    p352_e21,
    p352_e23,
    p349_e6,
]
# print(len(arr))
f = arr[8]
print(p350_e8())

