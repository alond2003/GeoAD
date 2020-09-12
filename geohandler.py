import itertools
from realsegment import RealSegment
from realangle import RealAngle
from absangle import AbsAngle
from segment import Segment
from degree import Degree
from point import Point
from length import Length
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
        points = seg.get_all_points()
        return [Segment(*points[i : i + 2]) for i in range(len(points) - 1)]

    def get_rseg(self, seg):
        """Return RealSegment from elementry Segment"""
        lst = [i for i in self.rsegments if seg == i]
        if len(lst) == 0:
            return KeyError
        return lst[0]

    def get_rang(self, aang):
        """Return RealAngle from elementry AbsAngle"""
        return self.angles[aang]

    def find_all_triangles(self):
        """Return list of all triangles (point's order doesn't matter)"""
        res = []
        for i, j, k in itertools.combinations(self.points, 3):
            sides = [Segment(i, j), Segment(j, k), Segment(k, i)]
            if all(
                [
                    any([seg.is_subsegment(side) for seg in self.segments])
                    for side in sides
                ]
            ) and not any(
                [
                    i in seg.get_all_points()
                    and j in seg.get_all_points()
                    and k in seg.get_all_points()
                    for seg in self.segments
                ]
            ):
                # create triangle
                points = [i, j, k]
                sides = [self.get_full_seg(s.start, s.end) for s in sides]
                aangs = [
                    self.get_non_reflex_angle(*(points[n:] + points[:n]))
                    for n in range(3)
                ]
                aconv = Convertor(self.disassemble_angle, self.get_rang)
                sconv = Convertor(self.disassemble_segment, self.get_rseg)
                res.append(Triangle(points, sides, aangs, aconv, sconv))
        return res

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

    def aang_equal_aang(self, aang1, aang2, reason):
        """Assume AbsAngle1 = AbsAngle2 and act apon it"""
        aangs = [self.disassemble_angle(a) for a in [aang1, aang2]]
        rangs = [[self.angles[a] for a in l] for l in aangs]
        if all(r.isknown() for r in rangs[0] + rangs[1]):
            return

        mes = "---\n"
        # print("---")
        mes += f"{aang1} = {aang2} ({reason})\n"
        # print(aang1, "=", aang2)
        if len(aangs[0]) + len(aangs[1]) > 2:
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
        if len(res) == 2 and changed_rang == deg - (
            sum(pre_calc_rangs) - unchanged_rang
        ):
            # print הצבה and final value
            print(
                str(abs(changed_rang)),
                "=",
                deg,
                "-",
                "("
                + " + ".join(
                    [str(i.deg) for i in pre_calc_rangs if abs(i) != unchanged_rang]
                )
                + ")"
                if len(rangs) > 2 or len(min(pre_calc_rangs).deg.value.keys()) > 1
                else str(min(pre_calc_rangs).deg),
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
                "-",
                "("
                + " + ".join(
                    [str(i.deg) for i in pre_calc_rangs if abs(i) != unchanged_rang]
                )
                + ")"
                if len(rangs) > 2 or len(min(pre_calc_rangs).deg.value.keys()) > 1
                else str(min(pre_calc_rangs).deg),
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
                if pre != ang.deg:
                    if (
                        rang
                        == list(filter(lambda x: abs(ang) == x, self.angles.keys()))[0]
                    ):
                        res.insert(
                            1,
                            (
                                pre,
                                list(
                                    filter(lambda x: abs(ang) == x, self.angles.keys())
                                )[0],
                            ),
                        )
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

