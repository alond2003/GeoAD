import itertools
from absangle import AbsAngle
from realangle import RealAngle
from segment import Segment
from degree import Degree
from point import Point


class GeoHandler:
    def __init__(self, *points):
        """Create a GeoHandler object, keep all Points and collect all Segments"""
        self.points = list(points)

        self.segments = list(set([l for p in self.points for l in p.lines]))

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
        """@ax3: 2 alternate interior angles between 2 parallel lines and a transversal are equal"""
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
        for p1, p2, t in parallels_transversal:
            tp1 = t.get_intersection_point(p1)
            tp2 = t.get_intersection_point(p2)
            if t.get_all_points().index(tp1) > t.get_all_points().index(tp2):
                p1, p2 = p2, p1
                tp1, tp2 = tp2, tp1
            ang1 = AbsAngle(t.get_subsegment_from(tp1), tp1, p1.get_subsegment_to(tp1))
            ang2 = AbsAngle(t.get_subsegment_to(tp2), tp2, p2.get_subsegment_from(tp2))
            self.aang_equal_aang(
                ang1,
                ang2,
                f"corresponding angles between {str(p1)} || {str(p2)} and {str(t)}",
            )

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
        self.angles_on_parallel_lines()
        self.angle_sum_on_line()
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
            mes += " + ".join(aangs[0]) + " = " + " + ".join(aangs[1]) + "\n"
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
            rangs = [self.angles[i] for i in aang]
            mes += (
                " + ".join([str(i) for i in aang]) + " = " + str(deg) + f" ({reason})\n"
            )
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

