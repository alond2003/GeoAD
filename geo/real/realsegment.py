from geo.abs.abssegment import AbsSegment
from geo.real.expression import Length
from functools import total_ordering


@total_ordering
class RealSegment(AbsSegment):
    def __init__(self, *points, leng=None):
        """Create an Segment with length"""
        self.leng = leng.new_copy() if leng is not None else None
        AbsSegment.__init__(self, points[0], points[-1])
        self.set_midpoints(*points[1:-1])

    def set_value(self, val=None):
        """Set segmnt's length based on val [int,float,dict,Length] (default is newvar)"""
        if isinstance(val, (int, float, dict)):
            self.leng = Length(False, val)
        elif isinstance(val, Length):
            self.leng = val.new_copy()
        elif val is None:
            self.leng = Length()
        else:
            raise TypeError(f"cannot set segment value to {type(val)}")

    def get_value(self):
        """Return self.leng"""
        return self.leng

    def new_copy(self):
        """Return a new copy of this object"""
        return RealSegment(
            *self.get_all_points(),
            leng=self.leng.new_copy() if self.leng is not None else None,
        )

    def isknown(self):
        """Check if the segment's length is known or has variables in it"""
        return (self.leng is not None) and self.leng.isknown()

    def get_all_subsegments(self):
        """Return a list of all Realsubsegments"""
        points = self.get_all_points()
        return [RealSegment(*points[i : i + 2]) for i in range(len(points) - 1)]

    def __str__(self):
        """Return Segment's name and length"""
        return (
            AbsSegment.__str__(self)
            + "("
            + (str(self.leng) if self.leng is not None else "")
            + ")"
        )

    def __repr__(self):
        """Same as __str__"""
        return str(self)

    def __lt__(self, other):
        if isinstance(other, RealSegment):
            return self.leng < other.leng
        else:
            return self.leng < other

    def __eq__(self, other):
        if isinstance(other, RealSegment):
            return self.leng == other.leng
        elif isinstance(other, AbsSegment):
            return other == abs(self)
        else:
            return self.leng == other

    def __add__(self, other):
        """Return Length of sum"""
        if isinstance(other, RealSegment):
            return self.leng + other.leng
        else:
            return self.leng + other

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, RealSegment):
            return self.leng - other.leng
        else:
            return self.leng - other

    def __rsub__(self, other):
        return other - self.leng

    def __abs__(self):
        """Return Segment from this RealSegemnt"""
        res = AbsSegment(self.start, self.end)
        res.set_midpoints(*self.midpoints)
        return res

    def __int__(self):
        """Return the value of the length"""
        return int(self.leng)

    @classmethod
    def fromSegment(cls, seg, leng=None):
        """Create a RealSegment based on Segment"""
        return RealSegment(*seg.get_all_points(), leng=leng)
