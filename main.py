# TODO: implement th1-3 in handler
# TODO: make degree str better looking (180 - alpha, 180 + alpha - beta)

from point import Point
from segment import Segment
from realangle import RealAngle
from absangle import AbsAngle
from geohandler import GeoHandler
from degree import Degree

print("start\n")

"""
A, B, C, D = Point.createPoints("A", "B", "C", "D")
AB = Segment(A, B, True)
AB.add_midpoints(C)
CD = Segment(C, D, True)
"""

A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
AB = Segment(A, B, True)
AB.add_midpoints(C)
CD = Segment(C, D, True)
CE = Segment(C, E, True)
ECB = AbsAngle(CE, C, AB.get_subsegment_from(C))
geo = GeoHandler(A, B, C, D, E)
geo.angles_calc()
print(geo.angles)


print("\nend")
