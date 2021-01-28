class Polygon:
    def __init__(self, points, sides, aangs, aconv, sconv):
        """Init points, sides, and angles"""
        self.points = points
        self.sides = sides
        self.aangs = aangs
        self.aconv = aconv
        self.sconv = sconv

    def get_angle_from_point(self, p):
        """Return the interior angle of point p"""
        for a in self.aangs:
            if a.vertex == p:
                return a
        return None

    def __str__(self):
        """Return name of Polygon"""
        return "".join([i.name for i in self.points])

    def __repr__(self):
        return str(self)