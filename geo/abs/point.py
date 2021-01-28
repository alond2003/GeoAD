class Point:

    nextId = 0

    def __init__(self, name):
        """Create a new point"""
        self.name = name
        self.id = Point.nextId
        Point.nextId += 1
        self.lines = []

    def copy(self, p):
        """Copy constructor from Point p"""
        self.name = p.name
        self.id = p.id
        self.lines = p.lines  # does it affect same?

    def add_line(self, *lines):
        """Add line or lines that the point is on"""
        self.lines += list(lines)

    def __str__(self):
        """Return the point's name"""
        return self.name

    def __repr__(self):
        """Return the point's name and id"""
        return "<" + self.name + f"({self.id})>"

    def __hash__(self):
        """Used for hashing Segment and set(Point)"""
        return hash(self.id)

    def __eq__(self, other):
        """Compare Points' id"""
        return other.id == self.id

    @staticmethod
    def numtoname(n):
        ans = ""
        while n > 0:
            ans = chr(65 + (n - 1) % 26) + ans
            n = (n - 1) // 26
        return ans

    @staticmethod
    def createPoints(*point_names):
        """Return a tuple of Points according to point_names or number of points"""
        if len(point_names) == 1 and isinstance(point_names[0], int):
            return tuple([Point(Point.numtoname(i + 1)) for i in range(point_names[0])])
        return tuple([Point(i) for i in point_names])