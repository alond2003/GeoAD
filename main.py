from segment import Segment
from angle import Angle
from point import Point
from geohandler import GeoHandler

print("start\n")
"""
A,B,C,D = Point.createPoints('A','B','C','D')
AB = Segment(A,B,True)
AB.add_midpoints(C)
CD = Segment(C,D,True)

geo = GeoHandler([A,B,C,D])
"""

A,B,C,D,E = Point.createPoints('A','B','C','D','E')
AC = Segment(A,C,True)
AC.add_midpoints(B)
CE = Segment(C,E,True)
CE.add_midpoints(D)
geo = GeoHandler([A,B,C,D,E])
print([str(i) for i in geo.segments])
print([str(i) for i in geo.get_angles()])
BCD = Angle(AC.get_subsegment_from(B),C,CE.get_subsegment_to(D))
ACD = Angle(AC,C,CE.get_subsegment_to(D))
print(str(geo.get_better_name_angle(BCD)))
print(str(geo.get_better_name_angle(ACD)))



print("\nend")