# TODO: make a proves.py page with function that are exampke of proves from axyoms
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
