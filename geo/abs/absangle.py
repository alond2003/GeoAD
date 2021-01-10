from geo.abs.segment import Segment
from geo.real.expression import Degree


class AbsAngle:
    def __init__(self, ray1, vertex, ray2):
        """Create abstruct angle"""
        self.ray1 = ray1
        self.vertex = vertex
        self.ray2 = ray2

    def get_start_point(self):
        """Return the startpoint of ray1"""
        return self.ray1.start if self.ray1.end == self.vertex else self.ray1.end

    def get_end_point(self):
        """Return the endpoint of ray2"""
        return self.ray2.start if self.ray2.end == self.vertex else self.ray2.end

    def get_minimized_absangle(self):
        """Return an AbsAngle with the smallest rays possible (common for all same angles)"""
        mr = []
        for r in [self.ray1, self.ray2]:
            if r.start == self.vertex:
                mr.append(r.get_subsegment_to(r.get_all_points()[1]))
            else:
                mr.append(r.get_subsegment_from(r.get_all_points()[-2]))
        return AbsAngle(mr[0], self.vertex, mr[1])

    def reverse(self):
        """Switch ray1 & ray2"""
        self.ray1, self.ray2 = self.ray2, self.ray1

    def __hash__(self):
        """custom hash function such that every same angle gets the same hash"""
        ang = self.get_minimized_absangle()
        return hash((ang.get_start_point(), ang.vertex, ang.get_end_point()))

    def __eq__(self, other):
        """Check if the angles are the same abstruct angle"""
        return (
            self.ray1.are_inclusive(other.ray1)
            and self.vertex == other.vertex
            and self.ray2.are_inclusive(other.ray2)
        )

    def __str__(self):
        """Return Angle's name"""
        return (
            "∢"
            + self.get_start_point().name
            + self.vertex.name
            + self.get_end_point().name
        )

    def __repr__(self):
        """Return str(self)"""
        return str(self)
