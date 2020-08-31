from segment import Segment
from absangle import AbsAngle
from geohandler import GeoHandler
from point import Point


class Helper:
    def __init__(self):
        """Init points,segments and geo"""
        self.points = []
        self.segments = []
        self.geo = None

    def p(self, name):
        """Create new Point (if needed) and return it"""
        print(name, [i.name for i in self.points])
        if name not in [i.name for i in self.points]:
            self.points.append(Point(name))
        for p in self.points:
            if p.name == name:
                return p

    def s(self, name):
        """Create new Segment (if needed) and return it"""
        for pname in name:
            self.p(pname)
        start = self.p(name[0])
        end = self.p(name[-1])
        for seg in self.segments:
            if (seg.start == start and seg.end == end) or (
                seg.end == start and seg.start == end
            ):
                return seg
        self.segments.append(Segment(start, end, True))
        self.segments[-1].set_midpoints(*[self.p(i) for i in name[1:-1]])
        return self.segments[-1]

    def a(self, name):
        """Create new AbsAngle and return it"""
        self.geo()
        return self.geo.get_better_name_angle(
            AbsAngle(self.s(name[:-1]), self.p(name[1]), self.s(name[1:]))
        )

    def g(self):
        """Create new GeoHandler (if needed) and return it"""
        if self.geo is None or len(self.geo.points) < len(self.points):
            self.geo = GeoHandler(*self.points)
        return self.geo
