# TODO: make @th4 in geo
# TODO: make degree str better looking (180 - alpha, 180 + alpha - beta)
# TODO: if angle is 180 -> it is a segment
# TODO: when given angle (BED = x), make option to give actual name to var (speciel var/switch)
from point import Point
from segment import Segment
from realangle import RealAngle
from absangle import AbsAngle
from geohandler import GeoHandler
from degree import Degree
from helper import Helper

print("start\n")

"""
A, B, C, D = Point.createPoints("A", "B", "C", "D")
AB = Segment(A, B, True)
AB.set_midpoints(C)
CD = Segment(C, D, True)
"""

h = Helper()
h.s("AEB")
h.s("CFD")
h.s("GFEH")
h.s("AB").set_parallel(h.s("CD"))
h.g().angles_calc()
print(h.g().angles)
# A, B, C, D, E, F, G, H = Point.createPoints(8)
# AB = Segment(A, B, True)
# AB.set_midpoints(E)
# CD = Segment(C, D, True)
# CD.set_midpoints(F)
# GH = Segment(G, H, True)
# GH.set_midpoints(F, E)
# AB.set_parallel(CD)
# geo = GeoHandler(A, B, C, D, E, F, G, H)
# geo.angles_calc()
# print(geo.angles)

print("\nend")
