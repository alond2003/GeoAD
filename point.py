class Point:

    nextId = 0

    def __init__(self, name):
        """Create a new point"""
        self.name = name
        self.id = Point.nextId
        Point.nextId += 1
        self.lines = []

    def add_line(self, *lines):
        """Add line or lines that the point is on"""
        self.lines += list(lines)

    def __str__(self):
        """Return the point's name and id"""
        return self.name + f"({self.id})"

    def __hash__(self):
        """Used for hashing Segment and set(Point)"""
        return hash(self.id)

    def __eq__(self, other):
        """Compare Points' id"""
        return other.id == self.id

    @staticmethod
    def createPoints(*point_names):
        """Return a tuple of Points according to point_names"""
        return tuple([Point(i) for i in point_names])
