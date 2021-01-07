from geo.comp.polygon import Polygon


class Quadrilateral(Polygon):
    def __repr__(self):
        return "▱" + str(self)

    @classmethod
    def fromPolygon(cls, poly):
        return Quadrilateral(
            poly.points, poly.sides, poly.aangs, poly.aconv, poly.sconv
        )
