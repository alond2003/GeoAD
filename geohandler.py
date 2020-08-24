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

    def get_angles(self):
        res = []
        for p in self.points:
            if len(p.lines) == 0:
                continue
            elif len(p.lines) == 1 and p in (p.lines[0].start,p.lines[0].end):
                continue
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

                for r1,r2 in zip(rays,rays[1:]+rays[:1]):
                    res.append(Angle(r1,p,r2))

                return res

    def is_180_angle(self,ang):
        maybeline = Segment(ang.get_start_point(),ang.get_end_point())
        maybeline.add_midpoints(ang.vertex)

        return any(type(i) is Segment and i.is_subsegment(maybeline) for i in self.segments)

