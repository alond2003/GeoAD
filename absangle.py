from segment import Segment
from degree import Degree


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

    def same(self, other):
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

