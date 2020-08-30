from segment import Segment
from degree import Degree
from absangle import AbsAngle

from functools import total_ordering


@total_ordering
class RealAngle(AbsAngle):
    def __init__(self, ray1, vertex, ray2, deg=None):
        """Create an Angle with value"""
        self.deg = deg
        AbsAngle.__init__(self, ray1, vertex, ray2)

    def set_value(self, val=None):
        """Set angle's degree based on val [int,float,dict,Degree] (default is newvar)"""
        if isinstance(val, (int, float, dict)):
            self.deg = Degree(False, val)
        elif isinstance(val, Degree):
            self.deg = val
        elif val is None:
            self.deg = Degree()
        else:
            raise TypeError(f"cannot set angle value to {type(val)}")

    def __str__(self):
        """Return Angle's name and degree"""
        return (
            AbsAngle.__str__(self)
            + "("
            + (str(self.deg) if self.deg is not None else "")
            + ")"
        )

    def __lt__(self, other):
        if isinstance(other, RealAngle):
            return self.deg < other.deg
        else:
            return self.deg < other

    def __eq__(self, other):
        if isinstance(other, RealAngle):
            return self.deg == other.deg
        else:
            return self.deg < other

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

    @classmethod
    def fromAbsAngle(cls, absang, deg=None):
        """Create a RealAngle based on an AbsAngle"""
        return RealAngle(absang.ray1, absang.vertex, absang.ray2, deg)
