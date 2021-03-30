from numpy import argmax
import itertools

from geo.abs.point import Point
from geo.abs.abssegment import AbsSegment
from geo.abs.absangle import AbsAngle
from geo.real.realsegment import RealSegment
from geo.real.realangle import RealAngle
from geo.real.expression import Degree
from geo.real.expression import Length
from geo.comp.polygon import Polygon, Triangle, Quadrilateral
from geo.comp.convertor import Convertor


class Handler:

    MAX_CALC_CYCLES = 10

    # Theorem dictionary that maps theorem number to function
    THEOREM_DICT = {}

    def __init__(self, *points):
        """Create a Handler object, keep all Points and collect all Segments"""
        Handler.initialize_therem_dict()

        self.points = list(points)
        self.segments = list(set([l for p in self.points for _, l in p.lines]))

        # a list of proof blocks, initialized every time calc is called
        self.proof = None

        # angle & segment convertors
        # initalized in self.init_angles & self.init_segments respectively
        self.aconv, self.sconv = None, None

    """ THEOREMS """

    def angle_sum_on_line(self):
        """_th1: the sum of 2 angles on a line is 180°"""
        for ang180, seg in self.find_all_180_angles():
            self.abs_equal_exp(
                ang180, Degree(False, 180), f"angle upon line {seg} is 180"
            )

    def vertical_angles(self):
        """_th2: 2 vertical angles are equal"""
        for p in self.points:
            for a1, a2 in itertools.combinations(
                self.get_angles_around_point(p), 2
            ):
                if (
                    self.is_180_angle(AbsAngle(a1.ray1, p, a2.ray1))
                    or self.is_180_angle(AbsAngle(a2.ray1, p, a1.ray1))
                ) and (
                    self.is_180_angle(AbsAngle(a1.ray2, p, a2.ray2))
                    or self.is_180_angle(AbsAngle(a2.ray2, p, a1.ray2))
                ):
                    self.abs_equal_abs(a1, a2, "vertical angles")

    def angle_sum_around_point(self):
        """_th3: all angles around a point sum up to 360°"""
        for p in self.points:
            parts = self.get_angles_around_point(p)
            if len(parts) != 0:
                self.abs_equal_exp(
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
            tp = [
                t.get_intersection_point(p[0]),
                t.get_intersection_point(p[1]),
            ]
            if t.get_all_points().index(tp[0]) > t.get_all_points().index(
                tp[1]
            ):
                p[0], p[1] = p[1], p[0]
                tp[0], tp[1] = tp[1], tp[0]
            # make sure both p are the same direction
            p[0].better_direction()
            p[1].better_direction(p[0].get_slope_angle())

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

            # Corresponding angles
            for i in range(4):
                if aangs[0][i] is None or aangs[1][i] is None:
                    continue
                self.abs_equal_abs(
                    aangs[0][i],
                    aangs[1][i],
                    f"Corresponding angles are equal between {p[0]} || {p[1]} and {t}",
                )

            # alternate angles
            for i in range(4):
                coridx = (i + 2) % 4
                if aangs[0][i] is None or aangs[1][coridx] is None:
                    continue
                self.abs_equal_abs(
                    aangs[0][i],
                    aangs[1][coridx],
                    f"alteranting angles are equal between {p[0]} || {p[1]} and {t}",
                )

            # consecutive angles
            for i in range(4):
                considx = 3 - i
                if aangs[0][i] is None or aangs[1][considx] is None:
                    continue
                self.abs_equal_exp(
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
            tp = [
                t.get_intersection_point(p[0]),
                t.get_intersection_point(p[1]),
            ]
            if t.get_all_points().index(tp[0]) > t.get_all_points().index(
                tp[1]
            ):
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

            # Corresponding angles
            for i in range(4):
                if aangs[0][i] is None or aangs[1][i] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(self.aconv[aangs[1][i]]):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][i]}, converse corresponding angles between {p[0]}, {p[1]} and traverse {t}",
                    )

            # alternate angles
            for i in range(4):
                altidx = (i + 2) % 4
                if aangs[0][i] is None or aangs[1][altidx] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(
                    self.aconv[aangs[1][altidx]]
                ):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][altidx]}, converse alternating angles between {p[0]}, {p[1]} and traverse {t}",
                    )

            # consecutive angles
            for i in range(4):
                considx = 3 - i
                if aangs[0][i] is None or aangs[1][considx] is None:
                    continue
                if sum(self.aconv[aangs[0][i]]) == sum(
                    self.aconv[aangs[1][considx]]
                ):
                    self.set_parallel(
                        *p,
                        f"{aangs[0][i]} = {sum(self.aconv[aangs[0][i]])} = {aangs[1][considx]}, converse consecutive angles between {p[0]}, {p[1]} and traverse {t}",
                    )

    def angle_sum_in_triangle(self):
        """_th6: The sum of the measures of the interior angles of a triangle is 180°"""
        for t in self.find_all_triangles():
            self.abs_equal_exp(
                t.aangs,
                Degree(False, 180),
                f"the sum of the interior angles of △{t} is 180°",
            )

    def angle_sum_in_quadrilateral(self):
        """_th7: The sum of the measures of the interior angles of a Quadrilateral is 360°"""
        for q in self.find_all_quadrilateral():
            self.abs_equal_exp(
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
                    [p for p in tri.points if p not in side.get_all_points()][
                        0
                    ],
                )
                self.abs_equal_abs(
                    external_angle,
                    [
                        tri.get_angle_from_point(p)
                        for p in tri.points
                        if p != start[1]
                    ],
                    f"external angle to {tri.get_angle_from_point(start[1])} in △{tri}",
                )
            if end[0] != len(seg.get_all_points()) - 1:
                external_angle = self.get_non_reflex_angle(
                    seg.end,
                    end[1],
                    [p for p in tri.points if p not in side.get_all_points()][
                        0
                    ],
                )
                self.abs_equal_abs(
                    external_angle,
                    [
                        tri.get_angle_from_point(p)
                        for p in tri.points
                        if p != end[1]
                    ],
                    f"external angle to {tri.get_angle_from_point(end[1])} in △{tri}",
                )

    """ CALC """

    def init_angles(self):
        """Init angles with 180 or variable"""
        self.rangles = dict(((i, None) for i in self.get_angles()))
        for abs_ang in self.rangles.keys():
            if self.is_180_angle(abs_ang):
                self.rangles[abs_ang] = RealAngle.from_absangle(
                    abs_ang, Degree(False, d=180)
                )
            else:
                self.rangles[abs_ang] = RealAngle.from_absangle(
                    abs_ang, Degree()
                )
        self.aconv = Convertor(self.disassemble_angle, self.get_rang)

    def init_segments(self):
        """Init segments with length value"""
        rseg_list = sum(
            [
                RealSegment.from_abssegment(i).get_all_subsegments()
                for i in self.segments
            ],
            [],
        )
        self.rsegments = {}
        for rseg in rseg_list:
            rseg.set_value()
            self.rsegments[abs(rseg)] = rseg

        self.sconv = Convertor(self.disassemble_segment, self.get_rseg)

    def calc(
        self,
        inita=True,
        inits=True,
        print_proof=True,
        after_init=lambda: None,
        use_theorems=None,
    ):
        """Get information through theroms and given data"""
        self.proof = []
        if inita:
            self.init_angles()
        if inits:
            self.init_segments()

        after_init()

        if print_proof:
            print(self.rangles)

        last_len = -1
        for _ in range(self.MAX_CALC_CYCLES):
            last_len = len(self.proof)

            if use_theorems is None:
                for th in self.THEOREM_DICT.keys():
                    self.apply_theorem(th)
            else:
                for th in use_theorems:
                    self.apply_theorem(th)

            if len(self.proof) == last_len:
                break
            # Degree.variable_reduction(*[i.deg for i in self.angles.values()])
            # print([str(i) for i in self.angles])
        if print_proof:
            self.print_proof()

    def apply_theorem(self, th):
        """Apply Theorom th"""
        therorem_func = self.THEOREM_DICT[th]
        therorem_func(self)

    def print_proof(self):
        """Prints self.proof"""
        print("---\n".join(self.proof))

    """ SET EQUAL/PARALLEL """

    def abs_equal_abs(self, abs1, abs2, reason="given"):
        """Assume Abs1=Abs2 and act apon it"""
        message = ""
        abs_arr = [abs1, abs2]
        abs_sum_strs = [None, None]
        for i in range(2):
            if not isinstance(abs_arr[i], list):
                abs_arr[i] = [abs_arr[i]]
            abs_sum_strs[i] = " + ".join(map(str, abs_arr[i]))

        message += f"{abs_sum_strs[0]} = {abs_sum_strs[1]} ({reason})\n"

        reals = [
            sum([self.conv(a) for a in abs_lst], []) for abs_lst in abs_arr
        ]
        # if some angles were not elementry
        if sum([len(lst) for lst in reals]) > sum(
            [len(lst) for lst in abs_arr]
        ):
            message += " = ".join(
                [" + ".join([str(abs(r)) for r in reals[i]]) for i in range(2)]
            )
            message += " \n"

        max_real = max(*reals[0], *reals[1])
        if abs(max_real) in reals[0]:
            minus_group, plus_group = reals
        else:  # elif abs(max_real) in reals[1]:
            plus_group, minus_group = reals
        minus_group = [r for r in minus_group if abs(r) != max_real]
        if len(minus_group) > 0:
            message += (
                f"{abs(max_real)} = {' + '.join([str(abs(r)) for r in plus_group])}"
                f" - ({' + '.join([str(abs(r)) for r in minus_group])})\n"
            )

        message += (
            f"{abs(max_real)} = "
            f"{' + '.join([str(r.get_expression()) for r in plus_group])}"
        )

        should_add_parentheses = len(minus_group) > 1 or (
            len(minus_group) == 1
            and len(minus_group[0].get_expression().value.keys()) > 1
        )
        should_not_add_parentheses = len(minus_group) == 1
        if should_add_parentheses:
            message += f" - ({' + '.join([str(r.get_expression()) for r in minus_group])})"
        elif should_not_add_parentheses:
            message += f"- {minus_group[0].get_expression()}"

        message += " (eval)\n"
        if self.abs_equal_exp(
            abs(max_real), sum(plus_group) - sum(minus_group)
        ):
            self.proof[-1] = message + self.proof[-1]

    def abs_equal_exp(self, aabs, exp, reason="given"):
        """Assume (Abs = Exp) and act apon it. Return if new data was found"""
        message = ""
        reals = []

        # if aabs is elementry
        if not isinstance(aabs, list) and self.is_elementry(aabs):
            reals = self.conv(aabs)
            message += f"{aabs} = {exp} ({reason})\n"
        else:
            if not isinstance(aabs, list):
                aabs = [aabs]
            reals = sum([self.conv(a) for a in aabs], [])

            message += (
                f"{exp} = {' + '.join(map(str,aabs))} = "
                f"{' + '.join(map(str,map(abs,reals)))} ({reason}"
                f", the whole is the sum of its parts)\n"
            )

        # if we already know, there is no point to continue
        if all([r.isknown() for r in reals]):
            return False

        # the real that will be evaluated
        eval_real = max(reals)
        # a copy of eval_real
        eval_real_copy = eval_real.new_copy()
        # all reals accept eval_real
        other_reals = [r for r in reals if abs(r) != abs(eval_real)]
        # copy of other_reals
        other_reals_copy = [r.new_copy() for r in other_reals]

        # reduct to (eval_real = exp - sum(other_reals))
        if len(other_reals) > 0:
            if len(other_reals) == 1:
                other_reals_sum = str(abs(other_reals[0]))
            else:
                other_reals_sum = (
                    f"({' + '.join(map(str,map(abs,other_reals)))})"
                )
            message += f"{abs(eval_real)} = {exp} - {other_reals_sum} (same)\n"

        res = self.real_equal_exp(eval_real, exp - sum(other_reals))

        if len(res) <= 1:
            return False  # nothing has been discovered
        if len(res) == 2 and len(other_reals) == 0:
            pass  # skip unnecessary printing
        else:
            # - (sum(other_reals))
            minus_other_reals_copy_sum = ""
            should_add_parentheses = len(other_reals_copy) > 1 or (
                len(other_reals_copy) == 1
                and len(other_reals_copy[0].get_expression().value.keys()) > 1
            )
            should_not_add_parentheses = len(other_reals) == 1
            if should_add_parentheses:
                # add parentheses
                minus_other_reals_copy_sum = (
                    f" - ("
                    f"{' + '.join([str(r.get_expression()) for r in other_reals_copy])}"
                    f")"
                )

            elif should_not_add_parentheses:
                # no parentheses
                minus_other_reals_copy_sum = (
                    f" -{other_reals_copy[0].get_expression()}"
                )

            # check for other repercussions
            if len(res) == 2 and eval_real == exp - sum(other_reals_copy):
                # no other repercussions from switching

                # message += evaluation -> final value
                message += (
                    f"{abs(eval_real)} = {exp}{minus_other_reals_copy_sum} (eval)"
                    f" -> {abs(eval_real)} = {eval_real.get_expression()} (calc)\n"
                )
            else:
                # there are other repercussions from switching

                # message += evaluation (eval)
                message += (
                    f"{eval_real_copy.get_expression()} = {exp}{minus_other_reals_copy_sum}"
                    f" (eval)\n"
                )
                # message += reduction (same)
                message += (
                    f"{eval_real_copy.get_expression()} = "
                    f"{exp - sum(other_reals_copy)} (same)\n"
                )
                # message += (var = found) (found var)
                var_found = Degree(False, {res[0][0]: 1})
                message += (
                    f"{var_found} = {res[0][1]} (found var {var_found})\n"
                )
                # for all reals affected
                for pre_exp, r in res[1:]:
                    # message += (abs = proven = eval -> abs = final)
                    message += (
                        f"{r} = {pre_exp} = "
                        f"{pre_exp.__str__(res[0][0],f'({res[0][1]})')}"
                        f" -> {r} = {sum(self.conv(r))}\n"
                    )
        self.proof.append(message)
        return True

    def real_equal_exp(self, real, exp):
        """Set real to be exp, Return list of (preExp, affected Reals), list[0] = (varswitched.key,switchval)"""
        # if real has no value, set it to be exp
        if real.get_expression() is None:
            real.set_value(exp)
            return []
        # if real's value is the same as exp, we cannot continue
        switch_val = exp - real.get_expression()
        if switch_val == 0:
            return []

        # choose key,value to switch in all reals
        max_key = max(switch_val.value.keys())
        switch_val = switch_val / (-switch_val.value[max_key])
        del switch_val.value[max_key]
        """example:
            exp = real
            3x = 7y
            switch_val = exp - real = 3x-7y
            switch_val = (3x-7y)/7, remove y -> y = 3/7x
        """
        # that means every (1 max_key = switch_val)
        res = [(max_key, switch_val)]
        if isinstance(real, RealAngle):
            reals = self.rangles.values()
        elif isinstance(real, RealSegment):  # else:
            reals = self.rsegments.values()

        for new_real in reals:
            pre_val = new_real.get_expression().new_copy()
            # make the switch for new_real
            new_real.get_expression().switch(max_key, switch_val)
            # if the value has changed as a result of the switch
            if pre_val != new_real.get_expression():
                # if abs(new_real) is real, insert it at the front
                if abs(new_real) == abs(real):
                    res.insert(1, (pre_val, abs(real)))
                else:
                    res.append((pre_val, abs(new_real)))
        return res

    def set_parallel(self, p1, p2, reason="given"):
        """Set p1 || p2 based on resaon"""
        for s in self.segments:
            if s.is_subsegment(p1):
                p1 = s
            if s.is_subsegment(p2):
                p2 = s

        p1.set_parallel(p2)
        self.proof.append(f"{str(p1)} || {str(p2)} ({reason})\n")

    """ GENERIC REAL/ABS METHODS"""

    def conv(self, aabs):
        """Convert abs to real using aconv/sconv"""
        if isinstance(aabs, AbsAngle):
            return self.aconv[aabs]
        if isinstance(aabs, AbsSegment):
            return self.sconv[aabs]

    def is_elementry(self, aabs):
        """Return if aabs is elementry angle/segment"""
        return len(self.conv(aabs)) == 1

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
            [
                any([seg.is_subsegment(side) for seg in self.segments])
                for side in sides
            ]
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
            pointlist[-1:] + pointlist[:-1],
            pointlist,
            pointlist[1:] + pointlist[:1],
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
        return [Triangle.from_polygon(p) for p in self.find_all_polygons(3)]

    def find_all_quadrilateral(self):
        return [
            Quadrilateral.from_polygon(p) for p in self.find_all_polygons(4)
        ]

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

    """ BASIC ABS_ANGLE METOHDS """

    def get_non_reflex_angle(self, pfrom, vertex, pto):
        """Return non reflex angle based on 3 points"""
        ans = [
            AbsAngle(
                self.get_full_seg(pfrom, vertex),
                vertex,
                self.get_full_seg(vertex, pto),
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
        elif len(p.lines) == 1 and p in (
            p.lines[0][0].start,
            p.lines[0][0].end,
        ):
            return []

        rays = [line for line, _ in p.lines]

        return [
            AbsAngle(r1, p, r2) for r1, r2 in zip(rays, rays[1:] + rays[:1])
        ]

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
                    (
                        AbsAngle(
                            l.get_subsegment_to(p), p, l.get_subsegment_from(p)
                        ),
                        l,
                    )
                )
                res.append(
                    (
                        AbsAngle(
                            l.get_subsegment_from(p), p, l.get_subsegment_to(p)
                        ),
                        l,
                    )
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

    @classmethod
    def initialize_therem_dict(cls):
        """Initialize THEOREM_DICT if needed"""
        if cls.THEOREM_DICT != {}:
            return
        cls.THEOREM_DICT = {
            1: cls.angle_sum_on_line,
            2: cls.vertical_angles,
            3: cls.angle_sum_around_point,
            4: cls.angles_on_parallel_lines,
            5: cls.converse_angles_on_parallel_lines,
            6: cls.angle_sum_in_triangle,
            7: cls.angle_sum_in_quadrilateral,
            8: cls.exterior_angle_in_triangle,
        }

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
