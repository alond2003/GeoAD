from angle import Angle
from segment import Segment

class GeoHandler:

    def __init__(self,points):
        self.points = points

        self.segments = set()
        for p in self.points:
            for l in p.lines:
                self.segments.add(l)
        self.segments = list(self.segments)

    def get_angles_around_point(self,p):
        if len(p.lines) == 0 or (len(p.lines) == 1 and p in (p.lines[0].start,p.lines[0].end)):
            return []
        else:
            rays = []
            for l in p.lines:
                if p not in (l.start,l.end):
                    rays.append(l.get_subsegment_to(p))
                else:
                    rays.append(l)

            for l in p.lines:
                if p not in (l.start,l.end):
                    rays.append(l.get_subsegment_from(p))

            res = []
            for r1,r2 in zip(rays,rays[1:]+rays[:1]):
                res.append(Angle(r1,p,r2))
            return res

    def get_angles(self):
        res = []
        for p in self.points:
            res += self.get_angles_around_point(p)
        return res

    def get_better_name_angle(self,ang:Angle):
        true_rays = []
        for ray in [ang.ray1,ang.ray2]:
            tempray = None
            if ray not in self.segments:
                for l in self.segments:
                    if l.is_subsegment(ray):
                        otherpoint = ray.end if ang.vertex == ray.start else ray.start
                        if l.get_all_points().index(ang.vertex) < l.get_all_points().index(otherpoint):
                            tempray = l.get_subsegment_from(ang.vertex)
                        else:
                            tempray = l.get_subsegment_to(ang.vertex)
                        break
                true_rays.append(tempray)
            else:
                true_rays.append(ray)
        return Angle(true_rays[0],ang.vertex,true_rays[1])

    def find_all_180_angles(self):
        return list(filter(self.is_180_angle,self.get_angles()))

    def is_180_angle(self,ang):
        maybeline = Segment(ang.get_start_point(),ang.get_end_point())
        maybeline.add_midpoints(ang.vertex)

        return any(type(i) is Segment and i.is_subsegment(maybeline) for i in self.segments)


    def disassemble_angle(self,ang):
        ang = self.get_better_name_angle(ang)
        sub_angles = self.get_angles_around_point(ang.vertex)
        i = 0
        found = False
        while i<len(sub_angles):
            if sub_angles[i].ray1 == ang.ray1:
                found = True
                break
            i += 1
        
        if not found:
            raise Exception(f"didn't found the ray of the given angle ({str(ang)}) around the vertex ({ang.vertex.name})")

        res = []
        while sub_angles[i].ray1 != ang.ray2:
            res.append(sub_angles[i])
            i = (i+1)%len(sub_angles)

        return res 



