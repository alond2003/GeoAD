# Guidelines:
# זוויות הן עם כיוון השעון
# ישרים מקבילים באותו כיוון
# סדר רציץ של קווים היוצאים\העוברים בנקודה עם כיוון השעון (going through: to, from)
# זווית מעל 180 אחרונה בסדר הקווים בנקודה
# צלעות במצולע הן נגד כיוון השעון
# first build everything then assign value

from segment import Segment
from absangle import AbsAngle
from geohandler import GeoHandler
from point import Point
from functools import partial
from degree import Degree
from length import Length


class Helper:
    def __init__(self):
        """Init points,segments and geo"""
        Degree.reset_all()
        Length.reset_all()
        self.points = []
        self.segments = []
        self.geo = None
        self.did_inita = False
        self.did_inits = False
        self.did_calc = False
        self.to_inits = []
        self.to_inita = []

    """Create new or retrive present"""

    def p(self, name):
        """Create new Point (if needed) and return it"""
        # print(name, [i.name for i in self.points])
        if isinstance(name, Point):
            if name not in self.points:
                self.points.append(name)
            return name
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

    def a(self, name):
        """Create new AbsAngle and return it"""
        if isinstance(name, AbsAngle):
            return name
        return self.g().get_better_name_angle(
            AbsAngle(self.s(name[:-1]), self.p(name[1]), self.s(name[1:]))
        )

    def g(self):
        """Create new GeoHandler (if needed) and return it"""
        if self.geo is None or len(self.geo.points) < len(self.points):
            self.geo = GeoHandler(*self.points)
        return self.geo

    def tri(self, name):
        """Create new triangle by name"""
        pp = [self.p(i) for i in name[:3]]
        for i in range(3):
            self.s(str(pp[(i + 1) % 3]) + str(pp[i]))
        # angles a (bac)
        # fix angle b (abc -> cba)
        ab_idx = pp[1].lines.index(self.s(str(pp[0]) + str(pp[1])))
        bc_idx = pp[1].lines.index(self.s(str(pp[1]) + str(pp[2])))
        pp[1].lines[ab_idx], pp[1].lines[bc_idx] = (
            pp[1].lines[bc_idx],
            pp[1].lines[ab_idx],
        )
        # fix angle c (bca -> acb)
        bc_idx = pp[2].lines.index(self.s(str(pp[1]) + str(pp[2])))
        ca_idx = pp[2].lines.index(self.s(str(pp[2]) + str(pp[0])))
        pp[2].lines[bc_idx], pp[2].lines[ca_idx] = (
            pp[2].lines[ca_idx],
            pp[2].lines[bc_idx],
        )

    def poly(self, name):
        """
        Create Polygon based on name
        - order of points clockwise
        -> direction of sides anti-clockwise
        -> direction of angles clockwise
        """
        name = name[0] + name[1:][::-1]
        pp = [self.p(i) for i in name]
        for i, j in zip(pp, (pp[1:] + pp[:1])):
            # print(i, j)
            self.s(str(i) + str(j))
        # fix first angle (replace index of first and last line)
        firstline_idx = pp[0].lines.index(self.s(name[:2]))
        lastline_idx = pp[0].lines.index(self.s(name[-1] + name[0]))
        pp[0].lines[firstline_idx], pp[0].lines[lastline_idx] = (
            pp[0].lines[lastline_idx],
            pp[0].lines[firstline_idx],
        )

    def poly_diag(self, poly, name):
        """Create diagonal in polygon"""
        self.s(name)
        pfrom = self.p(name[0])
        pto = self.p(name[-1])
        sides = [self.s(i + j) for i, j in zip(poly, poly[1:] + poly[:1])]
        rays_pfrom = [side for side in sides if pfrom in side.get_all_points()]
        rays_pto = [side for side in sides if pto in side.get_all_points()]
        dig = self.s(name)
        self.insert_between(pfrom, rays_pfrom, dig)
        self.insert_between(pto, rays_pto, dig)

    """~~~~~~~~"""

    def insert_between(self, vertex, rays, seg):
        try:
            vertex.lines.remove(seg)
        except ValueError:
            pass
        vertex.lines.insert(max([vertex.lines.index(r) for r in rays]), seg)

    def tri_med(self, tri, name):
        """Build median in existing triangle (end point already exists)"""
        pfrom = self.p(self.get_intersection_point(tri, name))
        pto = self.p(name[0])
        if pfrom == pto:
            pto = self.p(name[-1])
        rays = [self.s(str(pfrom) + p) for p in tri if p != str(pfrom)]
        med_seg = self.s(name)
        pfrom.lines.remove(med_seg)
        pfrom.lines.insert(max([pfrom.lines.index(r) for r in rays]), med_seg)
        across_seg = self.s("".join([i for i in tri if i != str(pfrom)]))
        self.to_inits.append(
            partial(
                self.g().seg_equal_seg,
                across_seg.get_subsegment_to(pto),
                across_seg.get_subsegment_from(pto),
                f"given that {name} is median to {str(across_seg)} in △{tri}",
            )
        )

    def tri_angbi(self, tri, name):
        """Build Angle bisector in existing triangle (end point already exists)"""
        pfrom = self.p(self.get_intersection_point(tri, name))
        pto = self.p(name[0])
        if pfrom == pto:
            pto = self.p(name[-1])
        rays = [self.s(str(pfrom) + p) for p in tri if p != str(pfrom)]
        angbi_seg = self.s(name)
        pfrom.lines.remove(angbi_seg)
        pfrom.lines.insert(max([pfrom.lines.index(r) for r in rays]), angbi_seg)
        other_points = [self.p(i) for i in tri if i != str(pfrom)]

        def func(h, other_points, pfrom, pto, name, tri):
            h.g().aang_equal_aang(
                h.g().get_non_reflex_angle(other_points[0], pfrom, pto),
                h.g().get_non_reflex_angle(other_points[1], pfrom, pto),
                f"given that {name} is angle bisector of angle {h.g().get_non_reflex_angle(other_points[0],pfrom,other_points[1])} in △{tri}",
            )

        self.to_inita.append(partial(func, self, other_points, pfrom, pto, name, tri))

    def tri_alt(self, tri, name):
        """Build Altitude in existing triangle (end point already exists)"""
        pfrom = self.p(self.get_intersection_point(tri, name))
        pto = self.p(name[0])
        if pfrom == pto:
            pto = self.p(name[-1])

        rays = [self.s(str(pfrom) + p) for p in tri if p != str(pfrom)]
        alt_seg = self.s(name)
        pfrom.lines.remove(alt_seg)
        pfrom.lines.insert(max([pfrom.lines.index(r) for r in rays]), alt_seg)
        other_points = [self.p(i) for i in tri if i != str(pfrom)]
        across_seg = self.s("".join([i for i in tri if i != str(pfrom)]))

        def func(h, pfrom, pto, other_points, name, across_seg, tri):
            for i in range(2):
                h.g().aang_equal_deg(
                    h.g().get_non_reflex_angle(pfrom, pto, other_points[i]),
                    90,
                    f"given that {name} is an altitude to side {across_seg} in △{tri}",
                )

        self.to_inita.append(
            partial(func, self, pfrom, pto, other_points, name, across_seg, tri)
        )

    def tri_innerline(self, tri, name):
        """Creates a line inside the tri from one of its vertices"""
        pfrom = self.p(self.get_intersection_point(tri, name))
        pto = self.p(name[0])
        if pfrom == pto:
            pto = self.p(name[-1])
        rays = [self.s(str(pfrom) + p) for p in tri if p != str(pfrom)]
        med_seg = self.s(name)
        pfrom.lines.remove(med_seg)
        pfrom.lines.insert(max([pfrom.lines.index(r) for r in rays]), med_seg)

    def tri_segbi(self, tri, name, side):
        """Build Segment bisector in existing triangle (end point already exists)"""
        # create segment bisector
        self.s(name)

        # the midpoint in segment
        pmid = self.p(self.get_intersection_point(name, self.s(side).midpoints))
        # append Equality of halves
        def eq_of_halves(h, side, pmid, name, tri):
            h.g().seg_equal_seg(
                h.s(side).get_subsegment_to(pmid),
                h.s(side).get_subsegment_from(pmid),
                f"given that {name} is segment bisector to side {side} in △{tri}",
            )

        self.to_inits.append(partial(eq_of_halves, self, side, pmid, name, tri))

        # append perpendicularity of side and segbi
        self.to_inita.append(
            partial(
                self.perps,
                side,
                name,
                f"given that {name} is segment bisector to side {side} in △{tri}",
            )
        )

    def calc(self):
        if not self.did_inita:
            self.inita()
        if not self.did_inits:
            self.inits()
        self.g().calc(not self.did_inita, not self.did_inits)
        self.did_calc = True

    def inits(self):
        self.g().init_segments()
        self.did_inits = True
        [f() for f in self.to_inits]

    def paras(self, *names):
        """Set segments to be parallel by their names"""
        if len(names) < 2:
            return
        first = self.s(names[0])
        for name in names[1:]:
            first.set_parallel(self.s(name))

    def perps(self, seg1, seg2, reason="given"):
        """Set segments to be perpendicular"""
        seg1 = self.s(seg1)
        seg2 = self.s(seg2)
        # intersection point
        interp = seg1.get_intersection_point(seg2)

        def func(h, seg1, interp, seg2, reason):
            h.seta(
                h.g().get_non_reflex_angle(
                    seg1.start if seg1.start != interp else seg1.end,
                    interp,
                    seg2.start if seg2.start != interp else seg2.end,
                ),
                90,
                reason=reason,
            )

        if self.did_inita:
            func(self, seg1, interp, seg2, reason)
        else:
            self.to_inita.append(partial(func, self, seg1, interp, seg2, reason))

    def conts(self, og, new):
        og = self.s(og)
        if new.index(str(og.start)) > new.index(str(og.end)):
            new = new[::-1]
        old_p = og.get_all_points()
        new_p = [self.p(i) for i in new]
        if old_p == new_p or old_p == new_p[::-1]:
            return
        new = Segment(new_p[0], new_p[-1])
        new.set_midpoints(*new_p[1:-1])
        for i in new.get_all_points():
            if i in old_p:
                for j in range(len(i.lines)):
                    if i.lines[j] == og:
                        i.lines[j] = new
                        break
            else:
                i.add_line(new)

        for i in range(len(self.segments)):
            if self.segments[i] == og:
                self.segments[i] = new

    """Angles"""

    def inita(self):
        """Call self.geo.init_angles"""
        self.g().init_angles()
        self.did_inita = True
        [f() for f in self.to_inita]

    def seta(self, name, deg, reason="given"):
        """Set value of angle in geo to deg"""
        if not self.did_inita:
            self.inita()
        self.g().aang_equal_deg(self.a(name), deg, reason)

    def sets(self, name, leng, reason="given"):
        """Set valuie of segment in geo to leng"""
        if not self.did_inits:
            self.inits()

        self.g().seg_equal_leng(self.s(name), leng, reason)

    def geta(self, name):
        """Get angle value from geo by name"""
        if not self.did_calc:
            self.calc()
        try:
            return self.g().angles[self.a(name)]
        except KeyError:
            return sum(
                [self.g().angles[x] for x in self.g().disassemble_angle(self.a(name))]
            )

    def gets(self, name):
        """Get Segment value from geo by name"""
        if not self.did_calc:
            self.calc()
        try:
            return self.g().get_rseg(self.s(name))
        except KeyError:
            return sum(
                [
                    self.g().get_rseg(x)
                    for x in self.g().disassemble_segment(self.s(name))
                ]
            )

    def equala(self, name1, name2, reason="given"):
        """Set angle name1 to be equal to name2"""
        if not self.did_inita:
            self.inita()
        self.g().aang_equal_aang(self.a(name1), self.a(name2), reason)

    def equals(self, name1, name2, reason="given"):
        """Set seg name1 to be equal to name2"""
        if not self.did_inits:
            self.inits()
        self.g().seg_equal_seg(self.s(name1), self.s(name2), reason)

    def isparas(self, name1, name2):
        if not self.did_calc:
            self.calc()
        return self.s(name1).is_parallel(self.s(name2))

    def get_intersection_point(self, iter1, iter2):
        lst = list(
            set([self.p(i) for i in iter1]).intersection(
                set([self.p(i) for i in iter2])
            )
        )
        if len(lst) == 0:
            return None
        return lst[0]

