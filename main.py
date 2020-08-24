from segment import Segment
from angle import Angle
from point import Point
from geohandler import GeoHandler

print("start\n")

A,B,C,D = Point.createPoints('A','B','C','D')
AB = Segment(A,B,True)
AB.add_midpoints(C)
CD = Segment(C,D,True)

geo = GeoHandler([A,B,C,D])
print([str(i) for i in geo.get_angles()])
ACB = Angle(AB.get_subsegment_to(C),C,AB.get_subsegment_from(C))
print([str(i) for i in geo.disassemble_angle(ACB)])

print("\nend")