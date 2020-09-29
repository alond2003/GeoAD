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


def p350_e9():
    h = Helper()
    h.tri("BAC")
    h.conts("BC", "BCD")
    h.seta("ACD", 144)
    h.seta("CAB", 88)
    return h.geta("ABC")


def p350_e10():
    h = Helper()
    h.tri("BAC")
    h.conts("BC", "BCD")
    h.seta("ACD", 105)
    x = Degree.given("x")
    h.seta("CAB", 2 * x)
    h.seta("ABC", x)
    return h.geta("CAB"), h.geta("ABC")


def p350_e11():
    h = Helper()
    h.tri("BAC")
    h.conts("AC", "AEC")
    h.tri_angbi("BAC", "BE")
    h.conts("BC", "BDC")
    h.tri_med("BAC", "AD")
    h.sets("BC", 12)
    h.seta("ABE", 36)
    return h.gets("DC"), h.geta("ABC")


def p350_e12():
    h = Helper()
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.tri_angbi("ABC", "AD")
    h.seta("ACB", 44)
    h.seta("CBA", 80)
    return h.geta("ADB"), h.geta("CDA")


def p350_e13():
    h = Helper()
    h.tri("BAC")
    h.conts("BC", "BDCE")
    h.tri_angbi("BAC", "AD")
    x, y, z = Degree.given("x", "y", "z")
    h.seta("ABC", x)
    h.seta("ADC", y)
    h.seta("ACE", z)
    h.calc()
    return 2 * y, x + z, 2 * y == x + z, (x, y, z)


def p351_e14():
    h = Helper()
    h.tri("ABC")
    h.conts("BC", "BDC")
    h.tri_angbi("ABC", "AD")
    h.equala("BAD", "ACB")
    h.seta("CBA", 81)
    return h.geta("ACB")


def p351_e15():
    h = Helper()
    h.tri("CAB")
    h.conts("AB", "ADEB")
    h.tri_alt("CAB", "CD")
    h.tri_angbi("CAB", "CE")
    h.seta("ACB", 90)
    h.seta("CBA", 26)
    return h.geta("DCE")


def p351_e16():
    # CH proof
    h = Helper()
    h.tri("BAC")
    h.conts("AC", "AEC")
    h.tri_alt("BAC", "BE")
    h.conts("BC", "BDC")
    h.tri_angbi("BAC", "AD")
    h.conts("BE", "BFE")
    h.conts("AD", "AFD")
    h.seta("ABC", 90)
    return h.geta("BDF"), h.geta("DFB"), h.geta("BDF") == h.geta("DFB")


def p251_e17():
    # CH proof
    h = Helper()
    h.tri("CAB")
    h.conts("AB", "AEB")
    h.tri_alt("CAB", "CE")
    h.conts("CB", "CDB")
    h.tri_angbi("CAB", "AD")
    h.conts("CE", "CNE")
    h.conts("AD", "AND")
    h.seta("ACB", 90)
    h.seta("BAC", 34)
    return h.geta("DNC")


def p351_e18():
    # CH proof
    h = Helper()
    h.tri("CAB")
    h.conts("CB", "CDB")
    h.tri_alt("CAB", "AD")
    h.conts("AC", "AEC")
    h.tri_alt("CAB", "BE")
    h.seta("BAD", 38)
    h.seta("ACB", 48)
    return h.geta("EBA")


def p352_e19():
    # CH Proof
    h = Helper()
    h.tri("BAC")
    h.conts("AC", "AEC")
    h.tri_segbi("BAC", "EO", "AC")
    # h.tri_innerline("BAC", "CO")
    h.conts("BC", "BDC")
    h.tri_segbi("BAC", "DO", "BC")
    # other data
    h.sets("BD", 6)
    h.sets("AC", 8)

    return (
        h.gets("CE"),
        h.gets("BC"),
        h.geta("BCA"),
        h.geta("EOD"),
    )


def p352_e22():
    # CH Proof
    h = Helper()
    h.tri("BAC")
    h.conts("AB", "AEB")
    h.conts("BC", "BDC")
    h.tri_angbi("BAC", "AD")
    h.conts("AD", "AFD")
    h.tri_angbi("BAC", "CE")
    h.conts("CE", "CFE")
    h.seta("ABC", 64)
    return h.geta("AFC")


def p352_e24():
    # CH Proof
    h = Helper()
    h.tri("BAC")
    h.conts("AB", "ADB")
    h.conts("AC", "AEC")
    h.s("DE")
    h.paras("DE", "BC")
    h.seta("ABC", 50)
    h.seta("BCA", 60)
    return h.geta("ADE"), h.geta("CED")


def p353_e25():
    # CH Proof
    h = Helper()
    h.tri("BAC")
    h.conts("AB", "ADB")
    h.conts("AC", "AEC")
    h.s("DE")
    h.seta("CAB", 72)
    h.seta("ABC", 48)
    h.seta("CED", 120)
    h.calc()
    return h.geta("DEA"), h.geta("BCA")
    # return h.g().angles


def p_e():
    # CH Proof
    h = Helper()


print(p353_e25())

