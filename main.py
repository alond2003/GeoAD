# TODO: make degree str better looking (180 - alpha, 180 + alpha - beta)
# TODO: if angle is 180 -> it is a segment
# TODO: use tri_innerline in angle bisector and such
# TODO: value class that merges degree and length
# TODO: MAYBE merge rang=deg and such (same code twice for seg and ang)
from geo.abs.point import Point
from geo.abs.segment import Segment
from geo.real.realangle import RealAngle
from geo.abs.absangle import AbsAngle
from geo.handler import Handler
from geo.real.expression import Degree
from geo.helper import Helper

print("start\n")

"""
A, B, C, D = Point.createPoints("A", "B", "C", "D")
AB = Segment(A, B, True)
AB.set_midpoints(C)
CD = Segment(C, D, True)
"""

# h = Helper()
# h.s("AEB")
# h.s("CFD")
# h.s("GFEH")
# h.s("AB").set_parallel(h.s("CD"))
# h.g().angles_calc()
# print(h.g().angles)
# A, B, C, D, E, F, G, H = Point.createPoints(8)
# AB = Segment(A, B, True)
# AB.set_midpoints(E)
# CD = Segment(C, D, True)
# CD.set_midpoints(F)
# GH = Segment(G, H, True)
# GH.set_midpoints(F, E)
# AB.set_parallel(CD)
# geo = Handler(A, B, C, D, E, F, G, H)
# geo.angles_calc()
# print(geo.angles)

# """
h = Helper()
h.s("HGFE", "CGD", "AFB")
h.paras("AB", "CD")
# h.calca()
# print(h.g().angles)
h.g().init_segments()
print(h.g().rsegments)
# """

print("\nend")
