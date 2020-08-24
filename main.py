from segment import Segment
from angle import Angle
from point import Point
from geohandler import GeoHandler

print("start\n")

A,B,C,D = Point.createPoints(4,'A','B','C','D')
AB = Segment(A,B,True)
AB.add_midpoints(C)
CD = Segment(C,D,True)

geo = GeoHandler([A,B,C,D])
x = geo.get_angles()
for i in x:
    print(i)

ACD = Angle(AB.get_subsegment_to(C),C,CD)
ACB = Angle(AB.get_subsegment_to(C),C,AB.get_subsegment_from(C))
BCA = x[2]
CBA = Angle(AB.get_subsegment_from(C),B,AB)
print("ACD",geo.is_180_angle(ACD),False)
print("ACB",geo.is_180_angle(ACB),True)
print("BCA",geo.is_180_angle(BCA),True)
print("CBA",geo.is_180_angle(CBA),False,0)

print("\nend")