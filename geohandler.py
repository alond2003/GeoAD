from angle import Angle

class GeoHandler:

    def __init__(self,points=[]):
        self.points = points

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


