from geo.alg.unionfind import UnionFind


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

    def set_midpoints(self, *x):
        """add a midpoints"""
        self.midpoints = list(x)
        if self.isnew:
            for i in x:
                i.add_line(self)

    def get_all_points(self):
        """Return a list containing startpoint, midpoints and endpoint"""
        return [self.start] + self.midpoints + [self.end]

    def get_subsegment_to(self, point):
        """Return subsegment to point (containing all the midpoints in between)"""
        if point in self.midpoints:
            res = Segment(self.start, point)
            res.set_midpoints(*self.midpoints[0 : self.midpoints.index(point)])
            res.parallel = self.parallel
            return res
        elif point == self.end:
            return self
        return None

    def get_subsegment_from(self, point):
        """Return subsegment from point (containing all the midpoints in between)"""
        if point in self.midpoints:
            res = Segment(point, self.end)
            res.set_midpoints(*self.midpoints[self.midpoints.index(point) + 1 :])
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

    def get_subsegment(self, name):
        """Get subsegment based on name"""
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
            furthest = p[0]
            if self.get_all_points().index(p[0]) < self.get_all_points().index(p[1]):
                furthest = p[1]
            closest = p[1] if furthest == p[0] else p[0]
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
