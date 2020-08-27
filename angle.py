from segment import Segment
from degree import Degree


class Angle:
    def __init__(self, ray1, vertex, ray2):
        """Initialize angle's degree to None"""
        self.ray1 = ray1
        self.vertex = vertex
        self.ray2 = ray2
        self.deg = None

    def get_start_point(self):
        """Return the startpoint of ray1"""
        return self.ray1.start if self.ray1.end == self.vertex else self.ray1.end

    def get_end_point(self):
        """Return the endpoint of ray2"""
        return self.ray2.start if self.ray2.end == self.vertex else self.ray2.end

    def set_value(self, val=None):
        """Set angle's degree to const, newvar (default is newvar)"""
        if isinstance(val, int):
            self.deg = Degree(False)
            self.deg += {0: val}
        elif val is None:
            self.deg = Degree(True)
        # elif isinstance(val, Degree):
        # self.deg.switch(val)
        else:
            raise TypeError(f"cannot set angle value to {type(val)}")

    def same(self, other):
        """Check if the angles are the same ones (not Necessarily same deg)"""
        return (
            self.ray1 == other.ray1
            and self.vertex == other.vertex
            and self.ray2 == other.ray2
        )

    def __str__(self):
        """Return Angle's name and degree"""
        return (
            "∢"
            + self.get_start_point().name
            + self.vertex.name
            + self.get_end_point().name
            + (f"({str(self.deg)})" if self.deg is not None else "")
        )

    def __lt__(self, other):
        """preforms self < other (Angle or Degree)"""
        if isinstance(other, Degree):
            return self.deg < other
        elif isinstance(other, Angle):
            return self.deg < other.deg

    def __add__(self, other):
        """Return new Degree object that is the sum of the Degrees"""
        if isinstance(other, (Degree, int, float)):
            return self.deg + other
        elif isinstance(other, Angle):
            return self.deg + other.deg

    def __radd__(self, other):
        """Used in (other + self), Same as (self + other) """
        return self + other

    def __sub__(self, other):
        """Return new Degree object that is the difference of the Degrees"""
        if isinstance(other, (Degree, int, float)):
            return self.deg - other
        elif isinstance(other, Angle):
            return self.deg - other.deg

    def __rsub__(self, other):
        """Return new Degree object that is the difference of the Degrees"""
        if isinstance(other, (Degree, int, float)):
            return other - self.deg
