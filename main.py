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

A, B, C, D = Point.createPoints(4)
AB = Segment(A, B, True)
BC = Segment(B, C, True)
BD = Segment(B, D, True)
geo = GeoHandler(A, B, C, D)
geo.angles_calc()
print(geo.angles)


print("\nend")
