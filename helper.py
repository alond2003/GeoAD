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
        self.did_inita = False
        self.did_calca = False

    def p(self, name):
        """Create new Point (if needed) and return it"""
        # print(name, [i.name for i in self.points])
        if name not in [i.name for i in self.points]:
            self.points.append(Point(name))
        for p in self.points:
            if p.name == name:
                return p

    def s(self, *names):
        """Create new Segment(s) (if needed) and return it(them)"""
        res = []
        for name in names:
            for pname in name:
                self.p(pname)
            maybe = Segment(self.p(name[0]), self.p(name[-1]))
            for seg in self.segments:
                if seg.is_subsegment(maybe):
                    return seg.get_subsegment(name)
            self.segments.append(Segment(self.p(name[0]), self.p(name[-1]), True))
            self.segments[-1].set_midpoints(*[self.p(i) for i in name[1:-1]])
            res.append(self.segments[-1])
        if len(names) == 1:
            return res[0]
        return tuple(res)

    def paras(self, *names):
        """Set segments to be parallel by their names"""
        if len(names) < 2:
            return
        first = self.s(names[0])
        for name in names[1:]:
            first.set_parallel(self.s(name))

    def a(self, name):
        """Create new AbsAngle and return it"""
        return self.g().get_better_name_angle(
            AbsAngle(self.s(name[:-1]), self.p(name[1]), self.s(name[1:]))
        )

    def inita(self):
        """Call self.geo.init_angles"""
        self.g().init_angles()
        self.did_inita = True

    def seta(self, name, deg):
        """Set value of angle in geo to deg"""
        if not self.did_inita:
            self.inita()
        if self.a(name) not in self.g().angles:
            self.g().aang_equal_deg(self.a(name), deg, "given")
        else:
            self.g().angles[self.a(name)].set_value(deg)
            print(self.a(name), "=", deg, "(given)")

    def calca(self):
        """Call self.geo.calc_angles"""
        self.g().angles_calc(not self.did_inita)
        self.did_calca = True

    def geta(self, name):
        """Get angle value from geo by name"""
        if not self.did_calca:
            self.calca()
        try:
            return self.g().angles[self.a(name)]
        except KeyError:
            return sum(
                [self.g().angles[x] for x in self.g().disassemble_angle(self.a(name))]
            )

    def equala(self, name1, name2):
        """Set angle name1 to be equal to name2"""
        if not self.did_inita:
            self.inita()
        self.g().aang_equal_aang(self.a(name1), self.a(name2), "given")

    def g(self):
        """Create new GeoHandler (if needed) and return it"""
        if self.geo is None or len(self.geo.points) < len(self.points):
            self.geo = GeoHandler(*self.points)
        return self.geo
