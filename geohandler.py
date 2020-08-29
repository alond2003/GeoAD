from absangle import AbsAngle
from realangle import RealAngle
from segment import Segment
from degree import Degree
from point import Point


class GeoHandler:
    def __init__(self, points):
        """Create a GeoHandler object, keep all Points and collect all Segments"""
        self.points = points

        self.segments = list(set([l for p in self.points for l in p.lines]))

    def angles_calc(self):
        """init values for each elementary angle and try to minimize the unknown variables"""
        # TODO: add better documentation
        self.angles = dict(((i, None) for i in self.get_angles()))
        for abs_ang in self.angles.keys():
            if self.is_180_angle(abs_ang):
                self.angles[abs_ang] = RealAngle.fromAbsAngle(abs_ang, Degree(d=180))
            else:
                self.angles[abs_ang] = RealAngle.fromAbsAngle(abs_ang, Degree())

        for ang180 in self.find_all_180_angles():
            parts = [self.angles[i] for i in self.disassemble_angle(ang180)]
            self.ang_is_equal(max(parts), 180 - (sum(parts) - max(parts)))
            # print([str(i) for i in self.angles])

    def ang_is_equal(self, ang, deg):
        """minimize variables if can by data ang == deg"""
        if ang.deg is None:
            ang.deg = deg
        else:
            switchval = deg - ang.deg
            if switchval == 0:
                return
            maxkey = max(switchval.value.keys())
            switchval = switchval / (-switchval.value[maxkey])
            del switchval.value[maxkey]
            # that means every (1 maxkey = switchval)
            for ang in self.angles.values():
                ang.deg.switch(maxkey, switchval)

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
        """Return a list of all the 180° AbsAngles"""
        res = []
        for l in self.segments:
            for p in l.midpoints:
                res.append(
                    AbsAngle(l.get_subsegment_to(p), p, l.get_subsegment_from(p))
                )
                res.append(
                    AbsAngle(l.get_subsegment_from(p), p, l.get_subsegment_to(p))
                )
        return res

    def is_180_angle(self, ang):
        """Check if an angle is 180°"""
        maybeline = Segment(ang.get_start_point(), ang.get_end_point())
        maybeline.add_midpoints(ang.vertex)

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

