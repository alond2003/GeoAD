import math

from geo.alg.unionfind import UnionFind
from geo.abs.point import Point


class AbsSegment:
    def __init__(self, pointstart, pointend, isnew=False):
        """ if isnew: add this line to the start & end points"""
        self.start = pointstart
        self.end = pointend
        self.midpoints = []
        self.parallel = UnionFind()
        self.isnew = isnew
        if self.isnew:
            self.start.add_line(self)
            self.end.add_line(self)

    def set_midpoints(self, *x):
        """Set line's midpoints"""
        self.midpoints = list(x)
        if self.isnew:
            for p in x:
                p.add_line(self)

    def update_midpoints(self, *x):
        """Add midpoints to segment"""
        if self.isnew:
            # remove all instances of this segment in Point.lines
            for p in self.midpoints:
                rm = []
                for i in range(p.lines):
                    if p.lines[i][1] == self:
                        rm.append(i)
                for idx in rm[::-1]:
                    del p.lines[idx]
            # set the midpoints to x
            self.midpoints = list(x)
            # re-add this segment to Point.lines
            for p in self.midpoints:
                p.add_line(self)
        else:
            self.midpoints = list(x)

    def get_all_points(self):
        """Return a list containing startpoint, midpoints and endpoint"""
        return [self.start] + self.midpoints + [self.end]

    def get_subsegment_to(self, point):
        """Return subsegment to point (containing all the midpoints in between)"""
        if point in self.midpoints:
            res = AbsSegment(self.start, point)
            res.set_midpoints(*self.midpoints[0 : self.midpoints.index(point)])
            res.parallel = self.parallel
            return res
        elif point == self.end:
            return self
        elif point == self.start:
            return AbsSegment(point, point)
        return None

    def get_subsegment_from(self, point):
        """Return subsegment from point (containing all the midpoints in between)"""
        if point in self.midpoints:
            res = AbsSegment(point, self.end)
            res.set_midpoints(*self.midpoints[self.midpoints.index(point) + 1 :])
            res.parallel = self.parallel
            return res
        elif point == self.start:
            return self
        elif point == self.end:
            return AbsSegment(point, point)
        return None

    def is_subsegment(self, other):
        """Check if other is a subsegment of this Segment"""
        idxs = []
        for p in other.get_all_points():
            try:
                idxs.append(self.get_all_points().index(p))
            except ValueError:
                # if p not in this segment's points, other is not a subsegment
                return False

        # return True if all the idxs are ordered, one after another in self.get_all_points()
        return all(i < j for i, j in zip(idxs, idxs[1:])) or all(
            i > j for i, j in zip(idxs, idxs[1:])
        )

    def get_subsegment(self, name):
        """Get subsegment based on name (2 points segment)"""
        p = [
            list(filter(lambda x: x.name == name[i], self.get_all_points()))[0]
            for i in range(2)
        ]
        if p[0] == self.start:
            return self.get_subsegment_to(p[1])
        elif p[0] == self.end:
            return self.get_subsegment_from(p[1])
        elif p[1] == self.end or p[1] == self.start:
            return self.get_subsegment(name[::-1])
        else:
            furthest, closest = p[0], p[1]
            if self.get_all_points().index(furthest) < self.get_all_points().index(
                closest
            ):
                furthest, closest = closest, furthest
            return self.get_subsegment_to(furthest).get_subsegment_from(closest)

    def are_inclusive(self, other):
        """Check if (self is subsegment of other) or (other is subsegment of self)"""
        return self.is_subsegment(other) or other.is_subsegment(self)

    def is_parallel(self, other):
        """Check if self is paraller to other"""
        return self.parallel.is_same(other.parallel)

    def set_parallel(self, other):
        """Set that self is parallel to other"""
        self.parallel.union(other.parallel)

    def get_intersection_point(self, other):
        """Return the intersection point or None if there isn't any"""
        if self.is_parallel(other):
            return None
        lst = list(set(self.get_all_points()).intersection(set(other.get_all_points())))
        if len(lst) == 0:
            return None
        return lst[0]

    def reverse(self):
        """Reverse self.start and self.end"""
        self.start, self.end = self.end, self.start
        self.midpoints = self.midpoints[::-1]

    def get_slope_angle(self, p=None):
        """Return the angle of the slope in correlation to point p (default is self.start)"""
        if p is None:
            p = self.start
        if (
            self.end.x is None
            or self.end.y is None
            or self.start.x is None
            or self.start.y is None
        ):
            return 0
        dy = self.end.y - self.start.y
        dx = self.end.x - self.start.x

        other_p = [i for i in (self.end, self.start) if i != p][0]
        if dx == 0:
            if other_p.y > p.y:
                return 90
            else:
                return 270
        if dy == 0:
            if other_p.x > p.x:
                return 0
            else:
                return 180

        arctan = math.degrees(math.atan(dy / dx))

        if other_p.x < p.x:
            return (arctan + 180 + 360) % 360
        return (arctan + 360) % 360

    def better_direction(self):
        """Reverse segment if needed (for min slope angle)"""
        slope_ang = self.get_slope_angle()
        self.reverse()
        new_slope_ang = self.get_slope_angle()
        if new_slope_ang > slope_ang:
            self.reverse()

    def is_valid(self):
        """Checks if self is a valid segment (has startpoint and endpoint)"""
        return (
            self.start is not None
            and self.end is not None
            and self.start != self.end
            and isinstance(self.start, Point)
            and isinstance(self.end, Point)
        )

    def __repr__(self):
        """Return Segment's name and midpoints"""
        return (
            "<"
            + self.start.name
            + self.end.name
            + ":"
            + str([str(i) for i in self.midpoints])
            + ">"
        )

    def __str__(self):
        """Return Segment's name"""
        return self.start.name + self.end.name

    def __hash__(self):
        """Used for set(Segment)"""
        return hash(tuple(self.get_all_points()))

    def __eq__(self, other):
        """Check Segment == Segment"""
        return (
            other.get_all_points() == self.get_all_points()
            or other.get_all_points()[::-1] == self.get_all_points()
        )
