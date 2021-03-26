class UnionFind:
    def __init__(self):
        """Init self to a set by itself"""
        self.par = self
        self.rank = 1

    def find(self):
        """Return the root of self and do path compression"""
        if self.par != self:
            self.par = self.par.find()
        return self.par

    def union(self, other):
        """Union the sets of self and other (by rank)"""
        if self.find() == other.find():
            return
        if self.find().rank > other.find().rank:
            other.find().par = self.find()
        elif other.find().rank > self.find().rank:
            self.find().par = other.find()
        else:
            self.find().par = other
            other.find().rank += 1

    def is_same(self, other):
        """Check if self and other are in the same set"""
        return self.find() == other.find()

