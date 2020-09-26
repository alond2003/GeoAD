import itertools
from quadrilateral import Quadrilateral
from realsegment import RealSegment
from realangle import RealAngle
from absangle import AbsAngle
from segment import Segment
from degree import Degree
from point import Point
from length import Length
from polygon import Polygon
from triangle import Triangle
from convertor import Convertor


class GeoHandler:
    def __init__(self, *points):
        """Create a GeoHandler object, keep all Points and collect all Segments"""
        self.points = list(points)

        self.segments = list(set([l for p in self.points for l in p.lines]))

    """ THEOREMS """

    def vertical_angles(self):
        """@th2: 2 vertical angles are equal"""
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

    def angle_sum_on_line(self):
        """@th1: the sum of 2 angles on a line is 180°"""
        for ang180, seg in self.find_all_180_angles():
            self.aang_equal_deg(
                ang180, Degree(False, 180), f"angle upon line {seg} is 180"
            )

    def angle_sum_around_point(self):
        """@th3: all angles around a point sum up to 360°"""
        for p in self.points:
            parts = self.get_angles_around_point(p)
            if len(parts) != 0:
                self.aang_equal_deg(
                    parts, Degree(False, 360), f"sum of angles around point {p}"
                )

    def angles_on_parallel_lines(self):
        """@ax3 + @th4: corresponding,alteranting and consecutive angles between 2 parallel lines and a transversal are equal"""
        if len(self.segments) < 3:
            return

        parallels_transversal = [
            (p1, p2, t)
            for p1, p2 in itertools.combinations(self.segments, 2)
            if p1.is_parallel(p2) and p1 != p2
            for t in self.segments
            if t.get_intersection_point(p1) is not None
            and t.get_intersection_point(p2) is not None
        ]

        for *p, t in parallels_transversal:
            tp = [t.get_intersection_point(p[0]), t.get_intersection_point(p[1])]
            if t.get_all_points().index(tp[0]) > t.get_all_points().index(tp[1]):
                p[0], p[1] = p[1], p[0]
                tp[0], tp[1] = tp[1], tp[0]
            aangs = [[], []]
            for i in range(2):
                pe = p[i].get_subsegment_from(tp[i])
                te = t.get_subsegment_from(tp[i])
                ps = p[i].get_subsegment_to(tp[i])
                ts = t.get_subsegment_to(tp[i])
                order = [pe, te, ps, ts]
                for j in range(4):
                    if order[j] is not None and order[(j + 1) % 4] is not None:
                        aangs[i].append(AbsAngle(order[j], tp[i], order[(j + 1) % 4]))
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
                    f"Corresponding angles are equal between {str(p[0])} || {str(p[1])} and {str(t)}",
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
                    f"alteranting angles are equal between {str(p[0])} || {str(p[1])} and {str(t)}",
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
                    f"sum of consecutive angles between {str(p[0])} || {str(p[1])} and {str(t)}",
                )

    def angle_sum_in_triangle(self):
        """@th5: The sum of the measures of the interior angles of a triangle is 180°"""
        triangles = self.find_all_triangles()
        for t in triangles:
            self.aang_equal_deg(
                t.aangs,
                Degree(False, 180),
                f"the sum of the interior angles of △{str(t)} is 180°",
            )

    def exterior_angle_in_triangle(self):
        """@th6: the size of an exterior angle at a vertex of a triangle equals the sum of the sizes of the interior angles at the other two vertices of the triangle"""
        for tri in self.find_all_triangles():
            for side in tri.sides:
                for seg in self.segments:
                    if seg.is_subsegment(side) and not (
                        (seg.start == side.start or seg.start == side.end)
                        and (seg.end == side.start or seg.end == side.end)
                    ):
                        # side is subsegment of seg
                        start = (seg.get_all_points().index(side.start), side.start)
                        end = (seg.get_all_points().index(side.end), side.end)
                        if start[0] > end[0]:
                            start, end = end, start
                        if start[0] != 0:
                            external_angle = self.get_non_reflex_angle(
                                seg.start,
                                start[1],
                                [
                                    p
                                    for p in tri.points
                                    if p not in side.get_all_points()
                                ][0],
                            )
                            # add list support for aang=aang
                            # write tri.get_angle_from_point
                            self.aang_equal_aang(
                                external_angle,
                                [
                                    tri.get_angle_from_point(p)
                                    for p in tri.points
                                    if p != start[1]
                                ],
                                f"external angle to {str(tri.get_angle_from_point(start[1]))} in △{str(tri)}",
                            )
                        if end[0] != len(seg.get_all_points()) - 1:
                            external_angle = self.get_non_reflex_angle(
                                seg.end,
                                end[1],
                                [
                                    p
                                    for p in tri.points
                                    if p not in side.get_all_points()
                                ][0],
                            )
                            # add list support for aang=aang
                            # write tri.get_angle_from_point
                            self.aang_equal_aang(
                                external_angle,
                                [
                                    tri.get_angle_from_point(p)
                                    for p in tri.points
                                    if p != end[1]
                                ],
                                f"external angle to {str(tri.get_angle_from_point(end[1]))} in △{str(tri)}",
                            )
                        break

    """ CALC """

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
        self.exterior_angle_in_triangle()
        self.angles_on_parallel_lines()
        self.angle_sum_around_point()
        # Degree.variable_reduction(*[i.deg for i in self.angles.values()])
        # print([str(i) for i in self.angles])

    """ BASIC SEGMENT_CALC METHODS"""

    def get_full_seg(self, startpoint, endpoint):
        """Return Segment from 2 points"""
        maybeline = Segment(startpoint, endpoint)
        for i in self.segments:
            if i.is_subsegment(maybeline):
                return i.get_subsegment(startpoint.name + endpoint.name)
        return None

    def init_segments(self):
        """Init segments with length value"""
        self.rsegments = sum(
            [RealSegment.fromSegment(i).get_all_subsegments() for i in self.segments],
            [],
        )
        for i in self.rsegments:
            i.set_value()

    def disassemble_segment(self, seg):
        """Return list of all SubSegments"""
        seg = self.get_full_seg(seg.start, seg.end)
        points = seg.get_all_points()
        return [Segment(*points[i : i + 2]) for i in range(len(points) - 1)]

    def is_elementry_seg(self, seg):
        return len(self.disassemble_segment(seg)) == 1

    def get_rseg(self, seg):
        """Return RealSegment from elementry Segment"""
        lst = [i for i in self.rsegments if seg == abs(i)]
        if len(lst) == 0:
            raise KeyError
        return lst[0]

    def get_rang(self, aang):
        """Return RealAngle from elementry AbsAngle"""
        return self.angles[aang]

    def find_all_polygons(self, numofsides):
        """Return list of all polygons with numofsides sides"""
        # TODO problem with Convex Polygons
        res = []
        for point_list in itertools.combinations(self.points, numofsides):
            for perm in self.circle_perm(point_list):
                sides = [
                    Segment(perm[i], perm[(i + 1) % len(perm)])
                    for i in range(len(perm))
                ]
                # if (all segments exist) and (no 3 points on same line) and (no non-neighbor sides intersect)
                if (
                    all(
                        [
                            any([seg.is_subsegment(side) for seg in self.segments])
                            for side in sides
                        ]
                    )
                    and not any(
                        [
                            [p in seg.get_all_points() for p in perm].count(True) > 2
                            for seg in self.segments
                        ]
                    )
                    and not any(
                        [
                            side.get_intersection_point(non_adj_side) is not None
                            for side_idx, side in enumerate(sides)
                            for non_adj_idx, non_adj_side in enumerate(sides)
                            if non_adj_idx != side_idx
                            and non_adj_idx != (side_idx + 1) % len(sides)
                            and non_adj_idx != (side_idx - 1 + len(sides)) % len(sides)
                        ]
                    )
                ):
                    # create Polygon
                    points = list(perm)
                    sides = [self.get_full_seg(s.start, s.end) for s in sides]
                    # do aangs based on most non-reflex angles
                    aangs = [
                        self.get_non_reflex_angle(i, j, k)
                        for i, j, k in zip(
                            points[-1:] + points[:-1], points, points[1:] + points[:1]
                        )
                    ]
                    aconv = Convertor(self.disassemble_angle, self.get_rang)
                    sconv = Convertor(self.disassemble_segment, self.get_rseg)
                    res.append(Polygon(points, sides, aangs, aconv, sconv))
                    break
        return res

    def find_all_triangles(self):
        return [Triangle.fromPolygon(p) for p in self.find_all_polygons(3)]

    def find_all_quadrilateral(self):
        return [Quadrilateral.fromPolygon(p) for p in self.find_all_polygons(3)]

    """ BASIC ANGLES_CALC METHODS """

    def init_angles(self):
        """Init angles with 180 or variable"""
        self.angles = dict(((i, None) for i in self.get_angles()))
        for abs_ang in self.angles.keys():
            if self.is_180_angle(abs_ang):
                self.angles[abs_ang] = RealAngle.fromAbsAngle(
                    abs_ang, Degree(False, d=180)
                )
            else:
                self.angles[abs_ang] = RealAngle.fromAbsAngle(abs_ang, Degree())

    def angles_calc(self, init=True):
        """Try to minimize the unknown variables"""
        # TODO: add better documentation
        if init:
            self.init_angles()

        # print(self.angles)
        self.vertical_angles()
        self.angle_sum_on_line()
        self.angles_on_parallel_lines()
        self.angle_sum_around_point()
        Degree.variable_reduction(*[i.deg for i in self.angles.values()])
        # print([str(i) for i in self.angles])

    ####### make these function work for segment also

    def aang_equal_aang(self, aang1, aang2, reason):
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
        rangs = [[self.angles[a] for a in l] for l in aangs]
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
                f"(found var {str(Degree(False, {res[0][0]: 1}))})",
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
                    preval.__str__(res[0][0], f"({str(res[0][1])})"),
                    "->",
                    aa,
                    "=",
                    self.angles[aa].deg,
                )

    def seg_equal_seg(self, seg1, seg2, reason):
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
                f"(found var {str(Length(False, {res[0][0]: 1}))})",
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
                    preval.__str__(res[0][0], f"({str(res[0][1])})"),
                    "->",
                    ss,
                    "=",
                    self.angles[ss].leng,
                )

    def aang_equal_deg(self, aang, deg, reason):
        """Assume (AbsAngle = deg) and act apon it"""
        mes = "---\n"
        # print("---")
        if isinstance(aang, list):
            mes += (
                " + ".join([str(i) for i in aang]) + " = " + str(deg) + f" ({reason})\n"
            )
            if not all([i in self.angles for i in aang]):
                aang = sum([self.disassemble_angle(i) for i in aang], [])
            rangs = [self.angles[i] for i in aang]
            # print(" + ".join([str(i) for i in aang]), "=", deg, f"({reason})")
        else:
            if aang in self.angles:
                rangs = [self.angles[aang]]
                mes += str(aang) + " = " + str(deg) + f" ({reason})\n"
                # print(aang, "=", deg, f"({reason})")
            else:
                rangs = [self.angles[i] for i in self.disassemble_angle(aang)]
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
                f"(found var {str(Degree(False, {res[0][0]: 1}))})",
            )

            # for all angles affected:
            for preval, aa in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    aa,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({str(res[0][1])})"),
                    "->",
                    aa,
                    "=",
                    self.angles[aa].deg,
                )

    def seg_equal_leng(self, seg, leng, reason):
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
                f"(found var {str(Length(False, {res[0][0]: 1}))})",
            )

            # for all angles affected:
            for preval, ss in res[1:]:
                # print: abs(ang) = proven = הצבה -> abs(ang) = ang
                print(
                    ss,
                    "=",
                    preval,
                    "=",
                    preval.__str__(res[0][0], f"({str(res[0][1])})"),
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
            for ang in self.angles.values():
                pre = ang.deg.new_copy()
                ang.deg.switch(maxkey, switchval)
                if pre != ang.deg:  # if value did change
                    if (
                        rang
                        == list(filter(lambda x: abs(ang) == x, self.angles.keys()))[0]
                    ):  # if this is the main rang
                        res.insert(
                            1,
                            (
                                pre,
                                list(
                                    filter(lambda x: abs(ang) == x, self.angles.keys())
                                )[0],
                            ),
                        )  # insert it first to res
                    else:
                        res.append(
                            (
                                pre,
                                list(
                                    filter(lambda x: abs(ang) == x, self.angles.keys())
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
            for seg in self.rsegments:
                pre = seg.leng.new_copy()
                seg.leng.switch(maxkey, switchval)
                if pre != seg.leng:
                    if abs(rseg) == abs(seg):
                        res.insert(1, (pre, abs(seg)))
                    else:
                        res.append((pre, abs(seg)))
            return res

    ############

    """ BASIC ABS_ANGLE METOHDS """

    def get_non_reflex_angle(self, pfrom, vertex, pto):
        """Return acute angle based on 3 points"""
        ans1 = AbsAngle(
            self.get_full_seg(pfrom, vertex), vertex, self.get_full_seg(vertex, pto)
        )
        ans2 = AbsAngle(ans1.ray2, vertex, ans1.ray1)
        for i in range(2):
            a = ans1 if i == 0 else ans2
            arr = self.disassemble_angle(a)
            if (
                sum([self.angles[aa] for aa in arr]).isknown()
                and sum([self.angles[aa] for aa in arr]) < 180
            ):
                return a
            for i in range(len(arr)):
                for j in range(i, len(arr)):
                    if sum([self.angles[aa] for aa in arr[i : (j + 1)]]) == 180 or all(
                        [
                            val > 0
                            for key, val in (
                                sum([self.angles[aa] for aa in arr[i : (j + 1)]]) - 180
                            ).value.items()
                        ]
                    ):
                        return ans1 if a == ans2 else ans2

        res = AbsAngle(None, vertex, None)
        for aang in self.get_angles_around_point(vertex):
            if res.ray1 is None and (
                pfrom in aang.ray1.get_all_points() or pto in aang.ray1.get_all_points()
            ):
                res.ray1 = aang.ray1.get_subsegment(
                    str(vertex)
                    + str(pto if pto in aang.ray1.get_all_points() else pfrom)
                )
            if (
                res.ray1 is not None
                and (pfrom if pto in res.ray1.get_all_points() else pto)
                in aang.ray2.get_all_points()
            ):
                res.ray2 = aang.ray2.get_subsegment(
                    str(vertex) + str(pto if res.get_start_point() == pfrom else pfrom)
                )

                return res

    def get_angles_around_point(self, p):
        """Return a list of all the elementary AbsAngles around a point"""
        if len(p.lines) == 0:
            return []
        elif len(p.lines) == 1 and p in (p.lines[0].start, p.lines[0].end):
            return []
        else:
            rays = []
            for l in p.lines:
                if p not in (l.start, l.end):
                    rays.append(l.get_subsegment_to(p))
                else:
                    rays.append(l)

            for l in p.lines:
                if p not in (l.start, l.end):
                    rays.append(l.get_subsegment_from(p))

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
            if ray in self.segments:
                true_rays.append(ray)
            else:
                l = [l for l in self.segments if l.is_subsegment(ray)][0]
                otherpoint = ray.end if ang.vertex == ray.start else ray.start
                if l.get_all_points().index(ang.vertex) < l.get_all_points().index(
                    otherpoint
                ):
                    true_rays.append(l.get_subsegment_from(ang.vertex))
                else:
                    true_rays.append(l.get_subsegment_to(ang.vertex))
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
        maybeline = Segment(ang.get_start_point(), ang.get_end_point())
        maybeline.set_midpoints(ang.vertex)

        return any(i.is_subsegment(maybeline) for i in self.segments)

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
                f"didn't found the ray of the given angle ({str(ang)}) around the vertex ({ang.vertex.name})"
            )

        res = []
        while sub_angles[i].ray1 != ang.ray2:
            res.append(sub_angles[i])
            i = (i + 1) % len(sub_angles)

        return res

    @staticmethod
    def circle_perm(lst):
        res = [i for i in itertools.permutations(lst[1:])]
        i = 0
        while i < len(res):
            res.remove(res[i][::-1])
            i += 1
        res = [(lst[0],) + i for i in res]
        return res

