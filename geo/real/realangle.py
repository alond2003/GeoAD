"""geo/real/realangle.py"""

from geo.abs.abssegment import AbsSegment
from geo.abs.absangle import AbsAngle
from geo.real.expression import Degree

from functools import total_ordering


@total_ordering
class RealAngle(AbsAngle):
    def __init__(self, ray1, vertex, ray2, deg=None):
        """Create an Angle with value"""
        self.deg = deg.new_copy() if deg is not None else None
        AbsAngle.__init__(self, ray1, vertex, ray2)

    def set_value(self, val=None):
        """Set angle's degree based on val [int,float,dict,Degree] (default is newvar)"""
        if isinstance(val, (int, float, dict)):
            self.deg = Degree(False, val)
        elif isinstance(val, Degree):
            self.deg = val.new_copy()
        elif val is None:
            self.deg = Degree()
        else:
            raise TypeError(f"cannot set angle value to {type(val)}")

    def get_expression(self):
        """Return self.deg"""
        return self.deg

    def new_copy(self):
        """Return a new copy of this object"""
        return RealAngle(
            self.ray1,
            self.vertex,
            self.ray2,
            self.deg.new_copy() if self.deg is not None else None,
        )

    def isknown(self):
        """Check if the angles's degree is known or has variables in it"""
        return (self.deg is not None) and self.deg.isknown()

    def __str__(self):
        """Return Angle's name and degree"""
        return (
            AbsAngle.__str__(self)
            + "("
            + (str(self.deg) if self.deg is not None else "")
            + ")"
        )

    def __lt__(self, other):
        """Compare self to Degree or RealAngle"""
        if isinstance(other, RealAngle):
            return self.deg < other.deg
        else:
            return self.deg < other

    def __eq__(self, other):
        """Compare self to Degree/RealAngle or AbsAngle"""
        if isinstance(other, RealAngle):
            return self.deg == other.deg
        elif isinstance(other, AbsAngle):
            return (
                self.get_end_point() == other.get_end_point()
                and self.vertex == other.vertex
                and self.get_start_point() == other.get_start_point()
            )
        else:
            return self.deg == other

    def __add__(self, other):
        """Return Degree of sum"""
        if isinstance(other, RealAngle):
            return self.deg + other.deg
        else:
            return self.deg + other

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, RealAngle):
            return self.deg - other.deg
        else:
            return self.deg - other

    def __rsub__(self, other):
        return other - self.deg

    def __abs__(self):
        """Return AbsAngle from this RealAngle"""
        return AbsAngle(self.ray1, self.vertex, self.ray2)

    def __int__(self):
        """Return the value of the degree"""
        return int(self.deg)

    @classmethod
    def from_absangle(cls, absang, deg=None):
        """Create a RealAngle based on an AbsAngle"""
        return RealAngle(absang.ray1, absang.vertex, absang.ray2, deg)
