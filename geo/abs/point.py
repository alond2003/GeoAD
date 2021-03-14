class Point:

    nextId = 0

    def __init__(self, name, x=None, y=None):
        """Create a new point"""
        self.name = name
        self.id = Point.nextId
        Point.nextId += 1
        self.lines = []

        self.x = x
        self.y = y

    def copy(self, p):
        """Copy constructor from Point p"""
        self.name = p.name
        self.id = p.id
        self.lines = p.lines  # does it affect same?

        self.x = p.x
        self.y = p.y

    def add_line(self, *lines):
        """Add line or lines that the point is on"""

        for line in lines:
            if self in line.midpoints:
                # split the segment into 2 segments (self is an endpoint to both)
                self.lines.append(
                    (line.get_subsegment(self.name + line.start.name), line)
                )
                self.lines.append(
                    (line.get_subsegment(self.name + line.end.name), line)
                )
            else:
                self.lines.append((line, line))

        self.lines.sort(key=lambda t: -t[0].get_slope_angle(self))

    def __str__(self):
        """Return the point's name"""
        return self.name

    def __repr__(self):
        """Return the point's name, id and coordinates"""
        return f"<{self.name}({self.id})({self.x},{self.y})>"

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
    def createPoints(names, xs, ys):
        """Return a tuple of Points according to point_names or number of points"""
        return tuple([Point(name, x, y) for name, x, y in zip(names, xs, ys)])
