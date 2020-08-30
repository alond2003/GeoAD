from unionfind import UnionFind


class Segment:
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

    def add_midpoints(self, x):
        """add a list of midpoints or one midpoint"""
        if isinstance(x, list):
            self.midpoints = x
            if self.isnew:
                for i in x:
                    i.add_line(self)
        else:
            self.midpoints.append(x)
            if self.isnew:
                x.add_line(self)

    def get_all_points(self):
        """Return a list containing startpoint, midpoints and endpoint"""
        return [self.start] + self.midpoints + [self.end]

    def get_subsegment_to(self, point):
        """Return subsegment to point (containing all the midpoints in between)"""
        # TODO: what about if point == start?
        if point in self.midpoints:
            res = Segment(self.start, point)
            res.add_midpoints(self.midpoints[0 : self.midpoints.index(point)])
            res.parallel = self.parallel
            return res
        elif point == self.end:
            return self
        return None

    def get_subsegment_from(self, point):
        """Return subsegment from point (containing all the midpoints in between)"""
        # TODO: what about if point == end?
        if point in self.midpoints:
            res = Segment(point, self.end)
            res.add_midpoints(self.midpoints[self.midpoints.index(point) + 1 :])
            res.parallel = self.parallel
            return res
        elif point == self.start:
            return self
        return None

    def is_subsegment(self, other):
        """Check if other is a subsegment of this Segment"""
        idxs = []
        for i in other.get_all_points():
            try:
                idxs.append(self.get_all_points().index(i))
            except ValueError:
                return False
        return all(i < j for i, j in zip(idxs, idxs[1:])) or all(
            i > j for i, j in zip(idxs, idxs[1:])
        )

    def are_inclusive(self, other):
        """Check if (self is subsegment of other) or (other is subsegment of self)"""
        return self.is_subsegment(other) or other.is_subsegment(self)

    def is_parallel(self, other):
        """Check if self is paraller to other"""
        return self.parallel.is_same(other.parallel)

    def set_parallel(self, other):
        """Set that self is parallel to other"""
        self.parallel.union(other.parallel)

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

