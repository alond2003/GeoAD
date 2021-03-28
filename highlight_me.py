from geo.helper import Helper
from geo.real.expression import Degree


def p349_e2():
    h = Helper()
    h.s("ACB")
    h.s("CD")
    x = Degree().given("x")
    h.seta("DCB", x)
    h.seta("ACD", 3 * x)
    h.calc()
    return h.geta("DCB"), h.geta("ACD")


#