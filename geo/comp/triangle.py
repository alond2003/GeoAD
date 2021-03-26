from geo.comp.polygon import Polygon


class Triangle(Polygon):
    def __repr__(self):
        return "△" + str(self)

    @classmethod
    def fromPolygon(cls, poly):
        return Triangle(poly.points, poly.sides, poly.aangs, poly.aconv, poly.sconv)
