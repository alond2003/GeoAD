from point import Point
from segment import Segment
from angle import Angle
from geohandler import GeoHandler

print("start\n")

"""
A,B,C,D = Point.createPoints('A','B','C','D')
AB = Segment(A,B,True)
AB.add_midpoints(C)
CD = Segment(C,D,True)
"""
# pylint: disable=unbalanced-tuple-unpacking


pl = lambda x: print(list(map(str, x)))
A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
AB = Segment(A, B, True)
AB.add_midpoints(E)
CD = Segment(C, D, True)
CD.add_midpoints(E)
geo = GeoHandler([A, B, C, D, E])
geo.angles_calc()
pl(geo.angles)
# print([[str(i) for i in geo.disassemble_angle(j)] for j in geo.find_all_180_angles()])

print("\nend")
