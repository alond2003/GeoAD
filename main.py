from segment import Segment
from angle import Angle
from evaluator import Evaluator
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
# ACD = Angle(AB.get_subsegment_to(C),C,CD)
print("\nend")