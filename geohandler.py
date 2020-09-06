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

    # def vertical_angles(self):
    #     lines_intersection = [
    #         (p, l1, l2)
    #         for p in self.points
    #         for l1, l2 in itertools.combinations(p.lines, 2)
    #         if p in l1.midpoints and p in l2.midpoints
    #     ]
    #     for p,l1,l2 in lines_intersection:
    #         self.angs_are_equal()

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
        return
        """
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
            res = []
            for a in (ang1, ang2):
                if a not in self.angles:
                    a = [self.angles[i] for i in self.disassemble_angle(a)]
                else:
                    a = [self.angles[a]]
                res.append(a)
            self.angs_are_equal(
                res[0],
                sum(res[1]),
                f"corresponding angles between {str(p1)} || {str(p2)} and {str(t)}",
            )
        """

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
        self.angles_on_parallel_lines()
        self.angle_sum_on_line()
        self.angle_sum_around_point()
        Degree.variable_reduction(*[i.deg for i in self.angles.values()])
        # print([str(i) for i in self.angles])

    def aang_equal_aang(self, aang1, aang2, reason):
        """Assume AbsAngle1 = AbsAngle2 and act apon it"""
        pass

    def aang_equal_deg(self, aang, deg, reason):
        """Assume (AbsAngle = deg) and act apon it"""
        print("---")
        if isinstance(aang, list):
            rangs = [self.angles[i] for i in aang]
            if all([i.isknown() for i in rangs]):
                return
            print(" + ".join(aang), "=", deg, f"({reason})")
            print(
                AbsAngle.__str__(max(rangs)),
                "=",
                deg,
                "-",
                "(",
                " + ".join([AbsAngle.__str__(i) for i in rangs if i != max(rangs)]),
                ")",
                f"(same)",  #  העברת אגפים וכלל המעבר
            )
            res = self.rang_equal_deg(max(rangs), deg - (sum(rangs) - max(rangs)))

            for pre, aang in res:
                print(aang, "=", pre, "(proven) ->", aang, "=", self.angles[aang].deg)
        else:
            res = []
            # print(aang, self.angles.keys, type(self.angles.keys()))
            if aang in self.angles.keys():
                if self.angles[aang].isknown():
                    return
                res = self.rang_equal_deg(self.angles[aang], deg)
                print(aang, "=", deg, f"({reason})")
            else:
                rangs = [self.angles[i] for i in self.disassemble_angle(aang)]
                if all([i.isknown() for i in rangs]):
                    return
                print(
                    deg,
                    "=",
                    aang,
                    "=",
                    " + ".join([AbsAngle.__str__(i) for i in rangs]),
                    f"({reason}, the whole is the sum of its parts)",
                )
                print(
                    AbsAngle.__str__(max(rangs)),
                    "=",
                    deg,
                    "-",
                    "("
                    + " + ".join(
                        [AbsAngle.__str__(i) for i in rangs if i != max(rangs)]
                    )
                    + ")"
                    if len(rangs) > 2
                    else AbsAngle.__str__(min(rangs)),
                    f"(same)",
                )  #  העברת אגפים וכלל המעבר
                res = self.rang_equal_deg(max(rangs), deg - (sum(rangs) - max(rangs)))

            if len(res) >= 1:
                print(
                    AbsAngle.__str__(max(rangs)),
                    "=",
                    deg,
                    "-",
                    "("
                    + " + ".join([str(i.deg) for i in rangs if i != max(rangs)])
                    + ")",
                    "(evaluation) -> ",  # הצבה
                    AbsAngle.__str__(max(rangs)),
                    "=",
                    max(rangs).deg,
                    "(calc)",  # חישוב
                )
                for pre, aang in res:
                    if aang != max(rangs):
                        print(
                            aang,
                            "=",
                            pre,
                            "(proven) ->",
                            aang,
                            "=",
                            self.angles[aang].deg,
                        )

    def rang_equal_deg(self, ang, deg):
        """Set ang to be deg, Return list of (preDeg,affected aangs)"""
        if ang.deg is None:
            ang.deg = deg
            return []
        else:
            switchval = deg - ang.deg
            if switchval == 0:
                return []
            maxkey = max(switchval.value.keys())
            switchval = switchval / (-switchval.value[maxkey])
            del switchval.value[maxkey]
            # that means every (1 maxkey = switchval)
            res = []
            for ang in self.angles.values():
                pre = ang.deg.new_copy()
                ang.deg.switch(maxkey, switchval)
                if pre != ang.deg:
                    res.append(
                        (pre, list(filter(lambda x: ang == x, self.angles.keys()))[0])
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

