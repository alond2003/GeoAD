from numpy import argmax
import itertools

from geo.abs.point import Point
from geo.abs.abssegment import AbsSegment
from geo.abs.absangle import AbsAngle
from geo.real.realsegment import RealSegment
from geo.real.realangle import RealAngle
from geo.real.expression import Degree
from geo.real.expression import Length
from geo.comp.polygon import Polygon
from geo.comp.triangle import Triangle
from geo.comp.quadrilateral import Quadrilateral
from geo.comp.convertor import Convertor


class Handler:
    def __init__(self, *points):
        """Create a Handler object, keep all Points and collect all Segments"""
        self.points = list(points)

        self.segments = list(set([l for p in self.points for _, l in p.lines]))

    """ THEOREMS """

    def angle_sum_on_line(self):
        """_th1: the sum of 2 angles on a line is 180°"""
        for ang180, seg in self.find_all_180_angles():
            self.aang_equal_deg(
                ang180, Degree(False, 180), f"angle upon line {seg} is 180"
            )

    def vertical_angles(self):
        """_th2: 2 vertical angles are equal"""
        for p in self.points:
            for a1, a2 in itertools.combinations(self.get_angles_around_point(p), 2):
                if (
                    self.is_180_angle(AbsAngle(a1.ray1, p, a2.ray1))
                    or self.is_180_angle(AbsAngle(a2.ray1, p, a1.ray1))
                ) and (
                    self.is_180_angle(AbsAngle(a1.ray2, p, a2.ray2))
                    or self.is_180_angle(AbsAngle(a2.ray2, p, a1.ray2))
                ):
                    self.aang_equal_aang(a1, a2, "vertical angles")

    def angle_sum_around_point(self):
        """_th3: all angles around a point sum up to 360°"""
        for p in self.points:
            parts = self.get_angles_around_point(p)
            if len(parts) != 0:
                self.aang_equal_deg(
                    parts, Degree(False, 360), f"sum of angles around point {p}"
                )

    def angles_on_parallel_lines(self):
        """_ax3 + _th4: corresponding,alteranting and consecutive angles between 2 parallel lines and a transversal are equal"""
        if len(self.segments) < 3:
            return

        parallels_transversal = [
            (p1, p2, t)
            for p1, p2 in itertools.combinations(self.segments, 2)
            if p1.is_parallel(p2)
            for t in self.segments
            if t.get_intersection_point(p1) is not None
            and t.get_intersection_point(p2) is not None
        ]

        for *p, t in parallels_transversal:
            tp = [t.get_intersection_point(p[0]), t.get_intersection_point(p[1])]
            if t.get_all_points().index(tp[0]) > t.get_all_points().index(tp[1]):
                p[0], p[1] = p[1], p[0]
                tp[0], tp[1] = tp[1], tp[0]
            # make sure both p are the same direction
            for s in p:
                s.better_direction()

            aangs = [[], []]
            for i in range(2):
                pe = p[i].get_subsegment_from(tp[i])
                te = t.get_subsegment_from(tp[i])
                ps = p[i].get_subsegment_to(tp[i])
                ts = t.get_subsegment_to(tp[i])
                order = [pe, te, ps, ts]
                for j in range(4):
                    if (
                        order[j] is not None
                        and order[j].is_valid()
                        and order[(j + 1) % 4] is not None
                        and order[(j + 1) % 4].is_valid()
                    ):
                        aangs[i].append(
                            self.get_non_reflex_angle(
                                order[j].end
                                if order[j].end != tp[i]
                                else order[j].start,
                                tp[i],
                                order[(j + 1) % 4].end
                                if order[(j + 1) % 4].end != tp[i]
                                else order[(j + 1) % 4].start,
                            )
                        )
                    else:
                        aangs[i].append(None)

            # זוויות מתאימות
            # Corresponding angles
            for i in range(4):
                if aangs[0][i] is None or aangs[1][i] is None:
                    continue
                self.aang_equal_aang(
                    aangs[0][i],
                    aangs[1][i],
                    f"Corresponding angles are equal between {p[0]} || {p[1]} and {t}",
                )

            # זוויות מתחלפות
            # alternate angles
            for i in range(4):
                coridx = (i + 2) % 4
                if aangs[0][i] is None or aangs[1][coridx] is None:
                    continue
                self.aang_equal_aang(
                    aangs[0][i],
                    aangs[1][coridx],
                    f"alteranting angles are equal between {p[0]} || {p[1]} and {t}",
                )

            # זוויות חד צדדיות
            # consecutive angles
            for i in range(4):
                considx = 3 - i
                if aangs[0][i] is None or aangs[1][considx] is None:
                    continue
                self.aang_equal_deg(
                    [aangs[0][i], aangs[1][considx]],
                    Degree(False, 180),
                    f"sum of consecutive angles between {p[0]} || {p[1]} and {t}",
                )

    def converse_angles_on_parallel_lines(self):
        """_th5: Converse of angles between parallel lines (alternate interior / corresponding / consecutive)"""
        if len(self.segments) < 3:
            return

        pos_parallels_transversal = [
            (p1, p2, t)
            for p1, p2 in itertools.combinations(self.segments, 2)
            if not p1.is_parallel(p2) and p1.get_intersection_point(p2) is None
            for t in self.segments
            if t.get_intersection_point(p1) is not None
            and t.get_intersection_point(p2) is not None
        ]

        for *p, t in pos_parallels_transversal:
            if p[0].is_parallel(p[1]):
                continue
            tp = [t.get_intersection_point(p[0]), t.get_intersection_point(p[1])]
            if t.get_all_points().index(tp[0]) > t.get_all_points().index(tp[1]):
                p[0], p[1] = p[1], p[0]
                tp[0], tp[1] = tp[1], tp[0]
            # make sure both p are the same direction
            for s in p:
                s.better_direction()
            aangs = [[], []]
            for i in range(2):
                pe = p[i].get_subsegment_from(tp[i])
                te = t.get_subsegment_from(tp[i])
                ps = p[i].get_subsegment_to(tp[i])
                ts = t.get_subsegment_to(tp[i])
                order = [pe, te, ps, ts]
                for j in range(4):
                    if (
                        order[j] is not None
                        and order[j].is_valid()
                        and order[(j + 1) % 4] is not None
                        and order[(j + 1) % 4].is_valid()
                    ):
                        aangs[i].append(
                            self.get_non_reflex_angle(
                                order[j].end
                                if order[j].end != tp[i]
                                else order[j].start,
                                tp[i],
                                order[(j + 1) % 4].end
                                if order[(j + 1) % 4].end != tp[i]
                                else order[(j + 1) % 4].start,
                            )
                        )
                    else:
                        aangs[i].append(None)

            # זוויות מתאימות
            # Corresponding angles
            for i in range(4):
                if aangs[0][i] is None or aangs[1][i] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(self.aconv[aangs[1][i]]):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][i]}, converse corresponding angles between {p[0]}, {p[1]} and traverse {t}",
                    )

            # זוויות מתחלפות
            # alternate angles
            for i in range(4):
                altidx = (i + 2) % 4
                if aangs[0][i] is None or aangs[1][altidx] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(self.aconv[aangs[1][altidx]]):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][altidx]}, converse alternating angles between {p[0]}, {p[1]} and traverse {t}",
                    )

            # זוויות חד צדדיות
            # consecutive angles
            for i in range(4):
                considx = 3 - i
                if aangs[0][i] is None or aangs[1][considx] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(self.aconv[aangs[1][considx]]):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][considx]}, converse consecutive angles between {p[0]}, {p[1]} and traverse {t}",
                    )

    def angle_sum_in_triangle(self):
        """_th6: The sum of the measures of the interior angles of a triangle is 180°"""
        for t in self.find_all_triangles():
            self.aang_equal_deg(
                t.aangs,
                Degree(False, 180),
                f"the sum of the interior angles of △{t} is 180°",
            )

    def angle_sum_in_quadrilateral(self):
        """_th7: The sum of the measures of the interior angles of a Quadrilateral is 360°"""
        for q in self.find_all_quadrilateral():
            self.aang_equal_deg(
                q.aangs,
                Degree(False, 360),
                f"the sum of the interior angles in quadrilateral {q} is 360°",
            )

    def exterior_angle_in_triangle(self):
        """_th8: the size of an exterior angle at a vertex of a triangle equals the sum of the sizes of the interior angles at the other two vertices of the triangle"""
        tri_side_seg = [
            (tri, side, seg)
            for tri in self.find_all_triangles()
            for side in tri.sides
            for seg in self.segments
            if seg.is_subsegment(side)
            and not (
                (seg.start == side.start or seg.start == side.end)
                and (seg.end == side.start or seg.end == side.end)
            )  # and not seg's endpoints are the same as side's
        ]
        for tri, side, seg in tri_side_seg:
            # side is subsegment of seg
            start = (seg.get_all_points().index(side.start), side.start)
            end = (seg.get_all_points().index(side.end), side.end)
            if start[0] > end[0]:
                start, end = end, start
            if start[0] != 0:
                external_angle = self.get_non_reflex_angle(
                    seg.start,
                    start[1],
                    [p for p in tri.points if p not in side.get_all_points()][0],
                )
                self.aang_equal_aang(
                    external_angle,
                    [tri.get_angle_from_point(p) for p in tri.points if p != start[1]],
                    f"external angle to {tri.get_angle_from_point(start[1])} in △{tri}",
                )
            if end[0] != len(seg.get_all_points()) - 1:
                external_angle = self.get_non_reflex_angle(
                    seg.end,
                    end[1],
                    [p for p in tri.points if p not in side.get_all_points()][0],
                )
                self.aang_equal_aang(
                    external_angle,
                    [tri.get_angle_from_point(p) for p in tri.points if p != end[1]],
                    f"external angle to {tri.get_angle_from_point(end[1])} in △{tri}",
                )

    """ CALC """

    def init_angles(self):
        """Init angles with 180 or variable"""
        self.rangles = dict(((i, None) for i in self.get_angles()))
        for abs_ang in self.rangles.keys():
            if self.is_180_angle(abs_ang):
                self.rangles[abs_ang] = RealAngle.fromAbsAngle(
                    abs_ang, Degree(False, d=180)
                )
            else:
                self.rangles[abs_ang] = RealAngle.fromAbsAngle(abs_ang, Degree())
        self.aconv = Convertor(self.disassemble_angle, self.get_rang)

    def init_segments(self):
        """Init segments with length value"""
        rseg_list = sum(
            [RealSegment.fromSegment(i).get_all_subsegments() for i in self.segments],
            [],
        )
        self.rsegments = {}
        for rseg in rseg_list:
            rseg.set_value()
            self.rsegments[abs(rseg)] = rseg

        self.sconv = Convertor(self.disassemble_segment, self.get_rseg)

    def calc(self, inita=True, inits=True):
        """Get information through theroms and given data"""
        if inita:
            self.init_angles()
        if inits:
            self.init_segments()

        # print(self.angles)
        self.vertical_angles()
        self.angle_sum_on_line()
        self.angle_sum_in_triangle()
        self.angle_sum_in_quadrilateral()
        self.exterior_angle_in_triangle()
        self.angles_on_parallel_lines()
        self.converse_angles_on_parallel_lines()
        self.angle_sum_around_point()
        # Degree.variable_reduction(*[i.deg for i in self.angles.values()])
        # print([str(i) for i in self.angles])

    """ BASIC CONVERTOR METHODS"""

    def disassemble_angle(self, ang):
        """Return a list of all the elementary AbsAngles that are included in ang"""
        ang = self.get_better_name_angle(ang)
        sub_angles = self.get_angles_around_point(ang.vertex)
        i = 0
        found = False
        while i < len(sub_angles):
            if sub_angles[i].ray1 == ang.ray1:
                found = True
                break
            i += 1

        if not found:
            raise Exception(
                f"didn't found the ray of the given angle ({ang}) around the vertex ({ang.vertex.name})"
            )

        res = []
        while sub_angles[i].ray1 != ang.ray2:
            res.append(sub_angles[i])
            i = (i + 1) % len(sub_angles)

        return res

    def disassemble_segment(self, seg):
        """Return list of all SubSegments (all elementary AbsSegments that are included in seg)"""
        seg = self.get_full_seg(seg.start, seg.end)
        points = seg.get_all_points()
        return [AbsSegment(*points[i : i + 2]) for i in range(len(points) - 1)]

    def get_rang(self, aang):
        """Return RealAngle from elementry AbsAngle"""
        return self.rangles[aang]

    def get_rseg(self, seg):
        """Return RealSegment from elementry AbsSegment"""
        return self.rsegments[seg]

    """ BASIC SEGMENT_CALC METHODS"""

    def get_full_seg(self, startpoint, endpoint):
        """Return AbsSegment from 2 points"""
        maybeline = AbsSegment(startpoint, endpoint)
        for i in self.segments:
            if i.is_subsegment(maybeline):
                return i.get_subsegment(startpoint.name + endpoint.name)
        return None

    def is_elementry_seg(self, seg):
        return len(self.disassemble_segment(seg)) == 1

    """ POLYGONS """

    def find_all_polygons(self, num_of_sides):
        """Return list of all polygons with num_of_sides sides"""
        res = []
        for point_list in itertools.combinations(self.points, num_of_sides):
            for perm in self.circle_perm(point_list):
                if self.is_pointlist_poly(list(perm)):
                    res.append(self.create_poly_from_pointlist(list(perm)))
        return res

    def is_pointlist_poly(self, pointlist):
        """Checks if pointlist is a polygon"""
        sides = [
            AbsSegment(pfrom, pto)
            for pfrom, pto in zip(pointlist, pointlist[1:] + pointlist[:1])
        ]

        # if not (all segments exist) -> no poly
        if not all(
            [any([seg.is_subsegment(side) for seg in self.segments]) for side in sides]
        ):
            return False

        # if (3 points on same line) -> no poly

        sides = [self.get_full_seg(seg.start, seg.end) for seg in sides]
        if any(
            [
                [p in seg.get_all_points() for p in pointlist].count(True) > 2
                for seg in self.segments
            ]
        ):
            return False
        # if (non-neighbor sides intersect) -> no poly
        if any(
            [
                side.get_intersection_point(non_adj_side) is not None
                for side_idx, side in enumerate(sides)
                for non_adj_idx, non_adj_side in enumerate(sides)
                if non_adj_idx != side_idx
                and non_adj_idx != (side_idx + 1) % len(sides)
                and non_adj_idx != (side_idx - 1 + len(sides)) % len(sides)
            ]
        ):
            return False
        return True

    def create_poly_from_pointlist(self, pointlist):
        """Create Polygon from pointlist (pointlist is a polygon)"""
        sides = [
            self.get_full_seg(pfrom, pto)
            for pfrom, pto in zip(pointlist, pointlist[1:] + pointlist[:1])
        ]
        # choose aangs based on most non-reflex angles
        aangs = [[], []]
        counter = [0, 0]
        for pfrom, vertex, pto in zip(
            pointlist[-1:] + pointlist[:-1], pointlist, pointlist[1:] + pointlist[:1]
        ):
            from_seg = self.get_full_seg(pfrom, vertex)
            to_seg = self.get_full_seg(vertex, pto)

            aangs[0].append(AbsAngle(from_seg, vertex, to_seg))
            aangs[1].append(AbsAngle(to_seg, vertex, from_seg))
            non_reflex_aang = self.get_non_reflex_angle(pfrom, vertex, pto)
            for i in range(2):
                if non_reflex_aang == aangs[i][-1]:
                    counter[i] += 1
                    break

        aangs = aangs[argmax(counter)]
        return Polygon(pointlist, sides, aangs, self.aconv, self.sconv)

    def find_all_triangles(self):
        return [Triangle.fromPolygon(p) for p in self.find_all_polygons(3)]

    def find_all_quadrilateral(self):
        return [Quadrilateral.fromPolygon(p) for p in self.find_all_polygons(4)]

    """ SET EQUAL/PARALLEL """

    def aang_equal_aang(self, aang1, aang2, reason="given"):
        """Assume AbsAngle1 = AbsAngle2 and act apon it"""
        mes = "---\n"
        # print("---")
        if not (isinstance(aang1, list) or isinstance(aang2, list)):
            aangs = [self.disassemble_angle(a) for a in [aang1, aang2]]
            mes += f"{aang1} = {aang2} ({reason})\n"
            # print(aang1, "=", aang2)
        else:
            if not isinstance(aang1, list):
                aang1 = [aang1]
            if not isinstance(aang2, list):
                aang2 = [aang2]
            mes += f"{' + '.join(map(str,aang1))} = {' + '.join(map(str,aang2))} ({reason})\n"
            aangs = [
                sum([self.disassemble_angle(a) for a in aang], [])
                for aang in [aang1, aang2]
            ]
        rangs = [[self.rangles[a] for a in l] for l in aangs]
        if all(r.isknown() for r in rangs[0] + rangs[1]):
            return

        if len(aangs[0]) + len(aangs[1]) > 2 or (
            (isinstance(aang1, list) and len(aang1) != len(aangs[0]))
            or (isinstance(aang2, list) and len(aang2) != len(aangs[1]))
        ):
            mes += (
                " + ".join(map(str, aangs[0]))
                + " = "
                + " + ".join(map(str, aangs[1]))
                + "\n"
            )
            # print(" + ".join(aangs[0]), "=", " + ".join(aangs[1]))
        max_rang = max(*rangs[0], *rangs[1])
        minus_group, plus_group = rangs
        if abs(max_rang) in aangs[1]:
            minus_group, plus_group = plus_group, minus_group
        minus_group = [i for i in minus_group if abs(i) != max_rang]
        if not (len(rangs[0]) == 1 and rangs[0][0] == abs(max_rang)):

            mes += (
                str(abs(max_rang))
                + " = "
                + " + ".join([str(abs(i)) for i in plus_group])
                + (
                    "- "
                    + (
                        f"({' + '.join([str(abs(i)) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(abs(minus_group[0]))
                    )
                    if len(minus_group) > 0
                    else ""
                )
                + "\n"
            )
            # print(abs(max_rang), "=", " + ".join([str(abs(i)) for i in plus_group]), ("- " + (f"({' + '.join([str(abs(i)) for i in minus_group])})" if len(minus_group) > 1 else str(abs(minus_group[0]))) if len(minus_group) > 0 else ""))

        # pre_calc_rangs = [i.new_copy() for i in rangs]
        unchanged_max_rang = max_rang.new_copy()
        plus_group = [i.new_copy() for i in plus_group]
        minus_group = [i.new_copy() for i in minus_group]
        res = self.rang_equal_deg(max_rang, sum(plus_group) - sum(minus_group))
        if len(res) <= 1:
            # print("*", end="")
            return
        print(mes, end="")
        if len(res) == 2 and max_rang == sum(plus_group) - sum(minus_group):
            # print הצבה and final value
            print(
                abs(max_rang),
                "=",
                " + ".join([str(i.deg) for i in plus_group]),
                (
                    "- "
                    + (
                        f"({' + '.join([str(i.deg) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(minus_group[0].deg)
                    )
                    if len(minus_group) > 0
                    else ""
                ),
                "(eval)",
                end=" ",
            )
            print("->", abs(max_rang), "=", max_rang.deg, "(calc)")
        else:

            # print הצבה and צמצום and find var
            print(
                unchanged_max_rang.deg,
                "=",
                " + ".join([str(i.deg) for i in plus_group]),
                (
                    "- "
                    + (
                        f"({' + '.join([str(i.deg) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(minus_group[0].deg)
                    )
                    if len(minus_group) > 0
                    else ""
                ),
                "(eval)",
            )
            print(
                unchanged_max_rang.deg,
                "=",
                sum(plus_group) - sum(minus_group),
                f"(same)",
            )
            print(
                Degree(False, {res[0][0]: 1}),
                "=",
                res[0][1],
                f"(found var {Degree(False, {res[0][0]: 1})})",
            )

            rem = []
            for pre, aa in res[1:]:
                if aa in aangs[0] or aa in aangs[1]:
                    res.insert(1, (pre, aa))
                    rem.append((pre, aa))
            for x, y in rem:
                for k in range(len(res) - 1, 0, -1):
                    if res[k] == (x, y):
                        res.pop(k)
                        break

            # for all angles affected:
            for preval, aa in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    aa,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({res[0][1]})"),
                    "->",
                    aa,
                    "=",
                    self.rangles[aa].deg,
                )

    def seg_equal_seg(self, seg1, seg2, reason="given"):
        """Assume Segment1 = Segment2 and act apon it"""
        mes = "---\n"
        # print("---")
        if not (isinstance(seg1, list) or isinstance(seg2, list)):
            segs = [self.disassemble_segment(s) for s in [seg1, seg2]]
            mes += f"{seg1} = {seg2} ({reason})\n"
            # print(aang1, "=", aang2)
        else:
            if not isinstance(seg1, list):
                seg1 = [seg1]
            if not isinstance(seg2, list):
                seg2 = [seg2]
            mes += f"{' + '.join(map(str,seg1))} = {' + '.join(map(str,seg2))} ({reason})\n"
            segs = [
                sum([self.disassemble_segment(a) for a in seg], [])
                for seg in [seg1, seg2]
            ]
        rsegs = [[self.get_rseg(s) for s in l] for l in segs]
        if all(r.isknown() for r in rsegs[0] + rsegs[1]):
            return

        if (
            len(segs[0]) + len(segs[1]) > 2
            and (not isinstance(seg1, list) or len(seg1) != len(segs[0]))
            and (not isinstance(seg2, list) or len(seg2) != len(segs[1]))
        ):
            mes += (
                " + ".join(map(str, segs[0]))
                + " = "
                + " + ".join(map(str, segs[1]))
                + "\n"
            )
            # print(" + ".join(aangs[0]), "=", " + ".join(aangs[1]))
        max_rseg = max(*rsegs[0], *rsegs[1])
        minus_group, plus_group = rsegs
        if abs(max_rseg) in segs[1]:
            minus_group, plus_group = plus_group, minus_group
        minus_group = [i for i in minus_group if abs(i) != max_rseg]
        if not (len(rsegs[0]) == 1 and rsegs[0][0] == abs(max_rseg)):

            mes += (
                str(abs(max_rseg))
                + " = "
                + " + ".join([str(abs(i)) for i in plus_group])
                + (
                    "- "
                    + (
                        f"({' + '.join([str(abs(i)) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(abs(minus_group[0]))
                    )
                    if len(minus_group) > 0
                    else ""
                )
                + "\n"
            )
            # print(abs(max_rang), "=", " + ".join([str(abs(i)) for i in plus_group]), ("- " + (f"({' + '.join([str(abs(i)) for i in minus_group])})" if len(minus_group) > 1 else str(abs(minus_group[0]))) if len(minus_group) > 0 else ""))

        # pre_calc_rangs = [i.new_copy() for i in rangs]
        unchanged_max_rseg = max_rseg.new_copy()
        plus_group = [i.new_copy() for i in plus_group]
        minus_group = [i.new_copy() for i in minus_group]
        res = self.rseg_equal_leng(max_rseg, sum(plus_group) - sum(minus_group))
        if len(res) <= 1:
            # print("*", end="")
            return
        print(mes, end="")
        if len(res) == 2 and max_rseg == sum(plus_group) - sum(minus_group):
            # print הצבה and final value
            print(
                abs(max_rseg),
                "=",
                " + ".join([str(i.leng) for i in plus_group]),
                (
                    "- "
                    + (
                        f"({' + '.join([str(i.leng) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(minus_group[0].leng)
                    )
                    if len(minus_group) > 0
                    else ""
                ),
                "(eval)",
                end=" ",
            )
            print("->", abs(max_rseg), "=", max_rseg.leng, "(calc)")
        else:

            # print הצבה and צמצום and find var
            print(
                unchanged_max_rseg.leng,
                "=",
                " + ".join([str(i.leng) for i in plus_group]),
                (
                    "- "
                    + (
                        f"({' + '.join([str(i.leng) for i in minus_group])})"
                        if len(minus_group) > 1
                        or len(minus_group[0].deg.value.keys()) > 1
                        else str(minus_group[0].leng)
                    )
                    if len(minus_group) > 0
                    else ""
                ),
                "(eval)",
            )
            print(
                unchanged_max_rseg.leng,
                "=",
                sum(plus_group) - sum(minus_group),
                f"(same)",
            )
            print(
                Length(False, {res[0][0]: 1}),
                "=",
                res[0][1],
                f"(found var {Length(False, {res[0][0]: 1})})",
            )

            rem = []
            for pre, ss in res[1:]:
                if ss in segs[0] or ss in segs[1]:
                    res.insert(1, (pre, ss))
                    rem.append((pre, ss))
            for x, y in rem:
                for k in range(len(res) - 1, 0, -1):
                    if res[k] == (x, y):
                        res.pop(k)
                        break

            # for all segments affected:
            for preval, ss in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    ss,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({res[0][1]})"),
                    "->",
                    ss,
                    "=",
                    self.rsegments[ss].leng,
                )

    def aang_equal_deg(self, aang, deg, reason="given"):
        """Assume (AbsAngle = deg) and act apon it"""
        mes = "---\n"
        # print("---")
        if isinstance(aang, list):
            mes += (
                " + ".join([str(i) for i in aang]) + " = " + str(deg) + f" ({reason})\n"
            )
            if not all([i in self.rangles for i in aang]):
                aang = sum([self.disassemble_angle(i) for i in aang], [])
            rangs = [self.rangles[i] for i in aang]
            # print(" + ".join([str(i) for i in aang]), "=", deg, f"({reason})")
        else:
            if aang in self.rangles:
                rangs = [self.rangles[aang]]
                mes += str(aang) + " = " + str(deg) + f" ({reason})\n"
                # print(aang, "=", deg, f"({reason})")
            else:
                rangs = self.aconv[aang]
                mes += (
                    str(deg)
                    + " = "
                    + str(aang)
                    + " = "
                    + " + ".join([str(abs(i)) for i in rangs])
                    + f" ({reason}, the whole is the sum of its parts)\n"
                )
                # print(deg, "=", aang, "=", " + ".join([str(abs(i)) for i in rangs]), f"({reason}, the whole is the sum of its parts)")
        if all([i.isknown() for i in rangs]):
            # print("*", end="")
            return
        if len(rangs) > 1:
            mes += (
                str(abs(max(rangs)))
                + " = "
                + str(deg)
                + " - "
                + (
                    "("
                    + " + ".join([str(abs(i)) for i in rangs if abs(i) != max(rangs)])
                    + ")"
                    if len(rangs) > 2
                    else str(abs(min(rangs)))
                )
                + f" (same)\n"
            )
            # print(str(abs(max(rangs))), "=", deg, "-", "(" + " + ".join([str(abs(i)) for i in rangs if i != max(rangs)]) + ")" if len(rangs) > 2 else str(abs(min(rangs))), f"(same)")

        pre_calc_rangs = [i.new_copy() for i in rangs]
        changed_rang = max(rangs)
        unchanged_rang = changed_rang.new_copy()
        res = self.rang_equal_deg(max(rangs), deg - (sum(rangs) - max(rangs)))
        if len(res) <= 1:
            # print("*", resend="")
            return
        print(mes, end="")
        # trying to exterminate unnecesory printing (eval same as calc same as reason)
        if len(res) == 2 and len(rangs) == 1:
            return
        if len(res) == 2 and changed_rang == deg - (
            sum(pre_calc_rangs) - unchanged_rang
        ):
            # print הצבה and final value
            print(
                str(abs(changed_rang)),
                "=",
                deg,
                "- ("
                + " + ".join(
                    [str(i.deg) for i in pre_calc_rangs if abs(i) != unchanged_rang]
                )
                + ")"
                if len(rangs) > 2 or len(min(pre_calc_rangs).deg.value.keys()) > 1
                else ("-" + str(min(pre_calc_rangs).deg) if len(rangs) == 2 else ""),
                f"(eval)",
                end=" ",
            )
            print("->", str(abs(changed_rang)), "=", changed_rang.deg, "(calc)")
        else:

            # print הצבה and צמצום and find var
            print(
                unchanged_rang.deg,
                "=",
                deg,
                "- ("
                + " + ".join(
                    [str(i.deg) for i in pre_calc_rangs if abs(i) != unchanged_rang]
                )
                + ")"
                if len(rangs) > 2 or len(min(pre_calc_rangs).deg.value.keys()) > 1
                else ("-" + str(min(pre_calc_rangs).deg) if len(rangs) == 2 else ""),
                f"(eval)",
            )
            print(
                unchanged_rang.deg,
                "=",
                deg - sum((i for i in pre_calc_rangs if abs(i) != unchanged_rang)),
                f"(same)",
            )
            print(
                Degree(False, {res[0][0]: 1}),
                "=",
                res[0][1],
                f"(found var {Degree(False, {res[0][0]: 1})})",
            )

            # for all angles affected:
            for preval, aa in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    aa,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({res[0][1]})"),
                    "->",
                    aa,
                    "=",
                    self.rangles[aa].deg,
                )

    def seg_equal_leng(self, seg, leng, reason="given"):
        """Assume (Segment = leng) and act apon it"""
        mes = "---\n"
        # print("---")
        if isinstance(seg, list):
            mes += (
                " + ".join([str(i) for i in seg]) + " = " + str(leng) + f" ({reason})\n"
            )
            if not all([self.is_elementry_seg(i) for i in seg]):
                seg = sum([self.disassemble_segment(i) for i in seg], [])
            rsegs = [self.get_rseg(i) for i in seg]
            # print(" + ".join([str(i) for i in aang]), "=", deg, f"({reason})")
        else:
            if self.is_elementry_seg(seg):
                rsegs = [self.get_rseg(seg)]
                mes += str(seg) + " = " + str(leng) + f" ({reason})\n"
                # print(aang, "=", deg, f"({reason})")
            else:
                rsegs = [self.get_rseg(i) for i in self.disassemble_segment(seg)]
                mes += (
                    str(leng)
                    + " = "
                    + str(seg)
                    + " = "
                    + " + ".join([str(abs(i)) for i in rsegs])
                    + f" ({reason}, the whole is the sum of its parts)\n"
                )
                # print(deg, "=", aang, "=", " + ".join([str(abs(i)) for i in rangs]), f"({reason}, the whole is the sum of its parts)")
        if all([i.isknown() for i in rsegs]):
            # print("*", end="")
            return
        if len(rsegs) > 1:
            mes += (
                str(abs(max(rsegs)))
                + " = "
                + str(leng)
                + " - "
                + (
                    "("
                    + " + ".join([str(abs(i)) for i in rsegs if abs(i) != max(rsegs)])
                    + ")"
                    if len(rsegs) > 2
                    else str(abs(min(rsegs)))
                )
                + f" (same)\n"
            )
            # print(str(abs(max(rangs))), "=", deg, "-", "(" + " + ".join([str(abs(i)) for i in rangs if i != max(rangs)]) + ")" if len(rangs) > 2 else str(abs(min(rangs))), f"(same)")

        pre_calc_rsegs = [i.new_copy() for i in rsegs]
        changed_rseg = max(rsegs)
        unchanged_rseg = changed_rseg.new_copy()
        res = self.rseg_equal_leng(max(rsegs), leng - (sum(rsegs) - max(rsegs)))
        if len(res) <= 1:
            # print("*", resend="")
            return
        print(mes, end="")
        if len(res) == 2 and changed_rseg == leng - (
            sum(pre_calc_rsegs) - unchanged_rseg
        ):
            # print הצבה and final value
            print(
                str(abs(changed_rseg)),
                "=",
                leng,
                "- ("
                + " + ".join(
                    [str(i.leng) for i in pre_calc_rsegs if abs(i) != unchanged_rseg]
                )
                + ")"
                if len(rsegs) > 2 or len(min(pre_calc_rsegs).leng.value.keys()) > 1
                else ("-" + str(min(pre_calc_rsegs).leng) if len(rsegs) == 2 else ""),
                f"(eval)",
                end=" ",
            )
            print("->", str(abs(changed_rseg)), "=", changed_rseg.leng, "(calc)")
        else:

            # print הצבה and צמצום and find var
            print(
                unchanged_rseg.leng,
                "=",
                leng,
                "- ("
                + " + ".join(
                    [str(i.leng) for i in pre_calc_rsegs if abs(i) != unchanged_rseg]
                )
                + ")"
                if len(rsegs) > 2 or len(min(pre_calc_rsegs).leng.value.keys()) > 1
                else ("-" + str(min(pre_calc_rsegs).leng) if len(rsegs) == 2 else ""),
                f"(eval)",
            )
            print(
                unchanged_rseg.leng,
                "=",
                leng - sum((i for i in pre_calc_rsegs if abs(i) != unchanged_rseg)),
                f"(same)",
            )
            print(
                Length(False, {res[0][0]: 1}),
                "=",
                res[0][1],
                f"(found var {Length(False, {res[0][0]: 1})})",
            )

            # for all angles affected:
            for preval, ss in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    ss,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({res[0][1]})"),
                    "->",
                    ss,
                    "=",
                    self.get_rseg(ss).leng,
                )

    def rang_equal_deg(self, rang, deg):
        """Set ang to be deg, Return list of (preDeg,affected Aangs), list[0] = (varswitched.key,switchval)"""
        if rang.deg is None:
            rang.deg = deg
            return []
        else:
            switchval = deg - rang.deg
            if switchval == 0:
                return []
            maxkey = max(switchval.value.keys())
            switchval = switchval / (-switchval.value[maxkey])
            del switchval.value[maxkey]
            # that means every (1 maxkey = switchval)
            res = [(maxkey, switchval)]
            for ang in self.rangles.values():
                pre = ang.deg.new_copy()
                ang.deg.switch(maxkey, switchval)
                if pre != ang.deg:  # if value did change
                    if (
                        rang
                        == list(filter(lambda x: abs(ang) == x, self.rangles.keys()))[0]
                    ):  # if this is the main rang
                        res.insert(
                            1,
                            (
                                pre,
                                list(
                                    filter(lambda x: abs(ang) == x, self.rangles.keys())
                                )[0],
                            ),
                        )  # insert it first to res
                    else:
                        res.append(
                            (
                                pre,
                                list(
                                    filter(lambda x: abs(ang) == x, self.rangles.keys())
                                )[0],
                            )
                        )
            return res

    def rseg_equal_leng(self, rseg, leng):
        """Set rseg to be length, Return list of (preLen, affected Segs), list[0] = (varswitched.key,switchval)"""
        if rseg.leng is None:
            rseg.leng = leng
            return []
        else:
            switchval = leng - rseg.leng
            if switchval == 0:
                return []
            maxkey = max(switchval.value.keys())
            switchval = switchval / (-switchval.value[maxkey])
            del switchval.value[maxkey]
            # that means every (1 maxkey = switchval)
            res = [(maxkey, switchval)]
            for seg in self.rsegments.values():
                pre = seg.leng.new_copy()
                seg.leng.switch(maxkey, switchval)
                if pre != seg.leng:
                    if abs(rseg) == abs(seg):
                        res.insert(1, (pre, abs(seg)))
                    else:
                        res.append((pre, abs(seg)))
            return res

    def set_parallel(self, p1, p2, reason="given"):
        """Set p1 || p2 based on resaon"""
        print("---")
        p1 = [
            s
            for s in self.segments
            if p1.start in s.get_all_points() and p1.end in s.get_all_points()
        ][0]
        p2 = [
            s
            for s in self.segments
            if p2.start in s.get_all_points() and p2.end in s.get_all_points()
        ][0]
        p1.set_parallel(p2)
        print(f"{str(p1)} || {str(p2)} ({reason})")

    """ BASIC ABS_ANGLE METOHDS """

    def get_non_reflex_angle(self, pfrom, vertex, pto):
        """Return non reflex angle based on 3 points"""
        ans = [
            AbsAngle(
                self.get_full_seg(pfrom, vertex), vertex, self.get_full_seg(vertex, pto)
            )
        ]
        ans.append(AbsAngle(ans[0].ray2, vertex, ans[0].ray1))
        # ans[0] and ans[1] are the two options, both close a circle around the vertex

        for i in range(2):
            a = ans[i]
            arr = self.disassemble_angle(a)

            a_sum = sum(self.aconv[a])
            # if a is known to be less than 180, return a
            if a_sum.isknown() and a_sum < 180:
                return a
            for ii in range(len(arr)):
                for j in range(ii, len(arr)):
                    # if a contains a subsum that is >= 180, return the other ans
                    a_sum = sum([self.rangles[aa] for aa in arr[ii : (j + 1)]])
                    if a_sum == 180 or all(
                        [val > 0 for key, val in (a_sum - 180).value.items()]
                    ):
                        return ans[0] if i == 1 else ans[1]

        # use x,y to understand which is acute
        return min(ans, key=lambda aa: aa.get_angle_size_from_coordinates())

    def get_angles_around_point(self, p):
        """Return a list of all the elementary AbsAngles around a point"""
        if len(p.lines) == 0:
            return []
        elif len(p.lines) == 1 and p in (p.lines[0][0].start, p.lines[0][0].end):
            return []

        rays = [line for line, _ in p.lines]

        return [AbsAngle(r1, p, r2) for r1, r2 in zip(rays, rays[1:] + rays[:1])]

    def get_angles(self):
        """Return a list of all the elementary AbsAngles"""
        res = []
        for p in self.points:
            res += self.get_angles_around_point(p)
        return res

    def get_better_name_angle(self, ang):
        """Find a better representation for the AbsAngle and return it"""
        true_rays = []
        for ray in [ang.ray1, ang.ray2]:
            # find the biggest segment from vertex instead of ray
            if ray in self.segments:
                true_rays.append(ray)
            else:
                for seg in self.segments:
                    if seg.is_subsegment(ray):
                        l = seg
                        break
                otherpoint = ray.end if ang.vertex == ray.start else ray.start
                opt1 = l.get_subsegment_from(ang.vertex)
                opt2 = l.get_subsegment_to(ang.vertex)
                if otherpoint in opt1.get_all_points():
                    true_rays.append(opt1)
                else:
                    true_rays.append(opt2)

        return AbsAngle(true_rays[0], ang.vertex, true_rays[1])

    def find_all_180_angles(self):
        """Return a list of (180° AbsAngles,segment on)"""
        res = []
        for l in self.segments:
            for p in l.midpoints:
                res.append(
                    (AbsAngle(l.get_subsegment_to(p), p, l.get_subsegment_from(p)), l)
                )
                res.append(
                    (AbsAngle(l.get_subsegment_from(p), p, l.get_subsegment_to(p)), l)
                )
        return res

    def is_180_angle(self, ang):
        """Check if an angle is 180°"""
        if isinstance(ang, RealAngle):
            if ang == 180:
                return True
        maybeline = AbsSegment(ang.get_start_point(), ang.get_end_point())
        maybeline.set_midpoints(ang.vertex)

        return any(i.is_subsegment(maybeline) for i in self.segments)

    @staticmethod
    def circle_perm(lst):
        """Return all possible permutation to put lst on a circle"""
        res = [i for i in itertools.permutations(lst[1:])]
        i = 0
        while i < len(res):
            res.remove(res[i][::-1])
            i += 1
        res = [(lst[0],) + i for i in res]
        return res
