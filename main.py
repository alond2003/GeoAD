# TODO: make degree str better looking (180 - alpha, 180 + alpha - beta)
# TODO: maybe seperate th4 to th4&5
# TODO: make subsegment easier with string AB.get("AE")
# TODO: possible angle problem with reverse()
# TODO: add_midpoint -> *args, set_midpoints
# TODO: make @ax3 in proofs
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

A, B, C, D, E, F, G, H = Point.createPoints(8)
AB = Segment(A, B, True)
AB.add_midpoints(E)
CD = Segment(C, D, True)
CD.add_midpoints(F)
GH = Segment(G, H, True)
GH.add_midpoints([F, E])
AB.set_parallel(CD)
geo = GeoHandler(A, B, C, D, E, F, G, H)
geo.angles_calc()
print(geo.angles)

print("\nend")
