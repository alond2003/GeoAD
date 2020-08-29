# TODO: fix -alpha in th1,th2
# TODO: add 360 th3
# TODO: implement th1-3 in handler

from point import Point
from segment import Segment
from realangle import RealAngle
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
AB.add_midpoints(E)
CD = Segment(C, D, True)
CD.add_midpoints(E)
geo = GeoHandler([A, B, C, D, E])
geo.angles_calc()
print(geo.angles)


print("\nend")
