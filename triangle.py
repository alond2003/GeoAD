class Triangle:
    def __init__(self, points, sides, aangs, aconv, sconv):
        """Init 3 points, sides, and angles"""
        self.points = points
        self.sides = sides
        self.aangs = aangs
        self.aconv = aconv
        self.sconv = sconv

    def __str__(self):
        """Return name of triangle"""
        return "".join([i.name for i in self.points])

