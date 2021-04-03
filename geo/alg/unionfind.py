class UnionFind:
    def __init__(self):
        """Init self to a set by itself"""
        self.par = self
        self.rank = 0

    def find(self):
        """Return the root of self and do path compression"""
        if self.par != self:
            self.par = self.par.find()
        return self.par

    def union(self, other):
        """Union the sets of self and other (by rank)"""
        x, y = self.find(), other.find()
        if x == y:
            return
        if x.rank < y.rank:
            x, y = y, x
        # now x.rank >= y.rank
        y.par = x
        if x.rank == y.rank:
            x.rank += 1

    def is_same(self, other):
        """Check if self and other are in the same set"""
        return self.find() == other.find()
