from angle import Angle
from segment import Segment
from degree import Degree
from point import Point


class GeoHandler:
    def __init__(self, points):
        """Create a GeoHandler object, keep all Points and collect all Segments"""
        self.points = points

        self.segments = set()
        for p in self.points:
            for l in p.lines:
                self.segments.add(l)
        self.segments = list(self.segments)

    def angles_calc(self):
        """init values for each elementary angle and try to minimize the unknown variables"""
        self.angles = self.get_angles()
        for ang in self.angles:
            if self.is_180_angle(ang):
                self.angles.remove(ang)
            else:
                ang.set_value()

        for ang180 in self.find_all_180_angles():
            # print(ang180, "=>", [str(i) for i in self.disassemble_angle(ang180)])
            parts = self.get_same(self.disassemble_angle(ang180))
            # print(ang180, "->", [str(i) for i in parts])
            # print(0 + parts[0])
            # print(sum(parts))
            # print(max(parts))
            # print(type(sum(parts)))
            # print(type(max(parts)))
            # print(180 - (sum(parts) - max(parts)))
            # max(parts).set_value(180 - (sum(parts) - max(parts)))
            self.ang_is_equal(max(parts), 180 - (sum(parts) - max(parts)))
            # print(sum(parts))
            # print(max(parts).deg)
            print([str(i) for i in self.angles])

    def ang_is_equal(self, ang, deg):
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
            for ang in self.angles:
                ang.deg.switch(maxkey, switchval)

    def get_same(self, ang_list):
        """Return list of angles from self.angles that are the same as ang_list"""
        return [i for i in self.angles if any(i.same(j) for j in ang_list)]

    def get_angles_around_point(self, p: Point):
        """Return a list of all the elementary angles around a point"""
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

            return [Angle(r1, p, r2) for r1, r2 in zip(rays, rays[1:] + rays[:1])]

    def get_angles(self):
        """Return a list of all the elementary angles"""
        res = []
        for p in self.points:
            res += self.get_angles_around_point(p)
        return res

    def get_better_name_angle(self, ang):
        """Find a better representation for the Angle and return it"""
        true_rays = []
        for ray in [ang.ray1, ang.ray2]:
            tempray = None
            if ray not in self.segments:
                for l in self.segments:
                    if l.is_subsegment(ray):
                        otherpoint = ray.end if ang.vertex == ray.start else ray.start
                        if l.get_all_points().index(
                            ang.vertex
                        ) < l.get_all_points().index(otherpoint):
                            tempray = l.get_subsegment_from(ang.vertex)
                        else:
                            tempray = l.get_subsegment_to(ang.vertex)
                        break
                true_rays.append(tempray)
            else:
                true_rays.append(ray)
        return Angle(true_rays[0], ang.vertex, true_rays[1])

    def find_all_180_angles(self):
        """Return a list of all the 180° angles"""
        res = []
        for l in self.segments:
            for p in l.midpoints:
                res.append(Angle(l.get_subsegment_to(p), p, l.get_subsegment_from(p)))
                res.append(Angle(l.get_subsegment_from(p), p, l.get_subsegment_to(p)))
        return res

    def is_180_angle(self, ang):
        """Check if an angle is 180°"""
        maybeline = Segment(ang.get_start_point(), ang.get_end_point())
        maybeline.add_midpoints(ang.vertex)

        return any(
            isinstance(i, Segment) and i.is_subsegment(maybeline) for i in self.segments
        )

    def disassemble_angle(self, ang):
        """Return a list of all the elementary angles that are included in ang"""
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

