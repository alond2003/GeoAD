# Guidelines:
# זוויות הן עם כיוון השעון
# ישרים מקבילים באותו כיוון
# סדר רציץ של קווים היוצאים\העוברים בנקודה עם כיוון השעון (going through: to, from)
# זווית מעל 180 אחרונה בסדר הקווים בנקודה
# צלעות במצולע הן נגד כיוון השעון
# first build everything then assign value

import itertools
from geo.abs.abssegment import AbsSegment
from geo.abs.absangle import AbsAngle
from geo.handler import Handler
from geo.abs.point import Point

from functools import partial
from geo.real.expression import Expression, Degree, Length
from geo.filehandler import get_points_from_file


class Helper:
    def __init__(self):
        """Init points,segments and geo"""
        Degree.reset_all()
        Length.reset_all()
        self.points = []
        self.segments = []
        self.geo = None
        self.to_inits = []
        self.to_inita = []
        self.did_calc = False
        self.given_dict = {}

    """Create new or retrive present"""

    def p(self, name, x=None, y=None):
        """Create new Point (if needed) and return it"""
        # print(name, [i.name for i in self.points])
        if isinstance(name, Point):
            if name not in self.points:
                self.points.append(name)
            return name
        if name not in [i.name for i in self.points]:
            self.points.append(Point(name, x, y))
        for p in self.points:
            if p.name == name:
                return p

    def ps(self, names, xs=itertools.cycle([None]), ys=itertools.cycle([None])):
        """Create a tuple of points"""
        return tuple([self.p(name, x, y) for name, x, y in zip(names, xs, ys)])

    def ps_from_file(self, path):
        """Create a tuple of points from ggb file"""
        res = get_points_from_file(path)
        names = [name for name, *_ in res]
        xs = [x for name, x, y in res]
        ys = [y for *_, y in res]
        return self.ps(names, xs, ys)

    def s(self, *names):
        """Create new AbsSegment(s) (if needed) and return it (them)"""
        res = []
        for name in names:
            for pname in name:
                self.p(pname)
            maybe = AbsSegment(self.p(name[0]), self.p(name[-1]))
            for seg in self.segments:
                if seg.is_subsegment(maybe):
                    return seg.get_subsegment(name)
            self.segments.append(AbsSegment(self.p(name[0]), self.p(name[-1]), True))
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
        """Create new Handler (if needed) and return it"""
        if self.geo is None or len(self.geo.points) < len(self.points):
            self.geo = Handler(*self.points)
        return self.geo

    def given(self, cls, symbol):
        """Create new given Expression (if needed) and return it"""
        if not issubclass(cls, Expression):
            raise TypeError(f"{cls} cannot be given, must be Expression")
        try:
            return self.given_dict[(cls, symbol)]
        except KeyError:
            self.given_dict[(cls, symbol)] = cls.given(symbol)
            return self.given_dict[(cls, symbol)]

    def tri(self, name):
        """Create new triangle by name"""
        self.poly(name)

    def poly(self, name):
        """
        Create Polygon based on name
        """
        p_arr = [self.p(p_name) for p_name in name]
        for pfrom, pto in zip(p_arr, p_arr[1:] + p_arr[:1]):
            self.s(f"{pfrom}{pto}")

    """~~~~~~~~"""

    def tri_med(self, tri, name):
        """Build median in existing triangle (end point should already exists)"""
        # create median segment
        pfrom = self.p(self.get_intersection_point(tri, name))
        across_seg = self.s("".join([i for i in tri if i != str(pfrom)]))
        for p in name:
            if self.p(p) in across_seg.get_all_points():
                pto = self.p(p)
                break
        self.s(name)
        # set median to be the middle of the triangle side

        def func(h, across_seg, pto, pfrom, name, tri):
            h.g().seg_equal_seg(
                across_seg.get_subsegment_to(pto),
                across_seg.get_subsegment_from(pto),
                f"given that {name} is median to {str(across_seg)} in △{tri}",
            )

        self.to_inits.append(partial(func, self, across_seg, pto, pfrom, name, tri))

    def tri_angbi(self, tri, name):
        """Build Angle bisector in existing triangle (end point already exists)"""
        pfrom = self.p(self.get_intersection_point(tri, name))
        across_seg = self.s("".join([i for i in tri if i != str(pfrom)]))
        for p in name:
            if self.p(p) in across_seg.get_all_points():
                pto = self.p(p)
                break
        self.s(name)

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
        across_seg = self.s("".join([i for i in tri if i != str(pfrom)]))

        for p in name:
            if self.p(p) in across_seg.get_all_points():
                pto = self.p(p)
                break
        self.s(name)

        other_points = [self.p(i) for i in tri if i != str(pfrom)]

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
        self.inita()
        self.inits()
        self.g().calc(False, False)
        self.did_calc = True

    def inits(self):
        if not self.did_calc:
            self.g().init_segments()
        for f in self.to_inits:
            f()
        self.to_inits = []

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

        self.to_inita.append(partial(func, self, seg1, interp, seg2, reason))

    def conts(self, og, new):
        og = self.s(og)
        if new.index(str(og.start)) > new.index(str(og.end)):
            new = new[::-1]
        new_p = [self.p(i) for i in new]
        og.update_midpoints(*new_p[1:-1])

    """Angles"""

    def inita(self):
        """Call self.geo.init_angles"""
        if not self.did_calc:
            self.g().init_angles()
        for f in self.to_inita:
            f()
        self.to_inita = []

    def seta(self, name, deg, reason="given"):
        """Set value of angle in geo to deg"""

        def func(h, name, deg, reason):
            h.g().aang_equal_deg(h.a(name), deg, reason)

        self.to_inita.append(partial(func, self, name, deg, reason))

    def sets(self, name, leng, reason="given"):
        """Set value of segment in geo to leng"""

        def func(h, name, deg, reason):
            h.g().seg_equal_leng(h.s(name), leng, reason)

        self.to_inits.append(partial(func, self, name, leng, reason))

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

        def func(h, name, deg, reason):
            h.g().aang_equal_aang(h.a(name1), h.a(name2), reason)

        self.to_inita.append(partial(func, self, name1, name2, reason))

    def equals(self, name1, name2, reason="given"):
        """Set seg name1 to be equal to name2"""

        def func(h, name, deg, reason):
            h.g().seg_equal_seg(h.s(name1), h.s(name2), reason)

        self.to_inita.append(partial(func, self, name1, name2, reason))

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
