class Point:

    next_id = 0

    def __init__(self, name, x=None, y=None):
        """Create a new point"""
        self.name = name
        self.id = Point.next_id
        Point.next_id += 1
        self.lines = []

        self.x = x
        self.y = y

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

        # sort self.lines by slope_angle
        self.lines.sort(key=lambda t: -t[0].get_slope_angle(self))

    def remove_line(self, *lines):
        """Remove line or lines from self.lines"""
        rm_idxs = []
        for idx, (_, line) in enumerate(self.lines):
            if line in lines:
                rm_idxs.append(idx)
        for idx in rm_idxs[::-1]:
            del self.lines[idx]

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
    def createPoints(names, xs, ys):
        """Return a tuple of Points according to points' names,xs and ys"""
        return tuple([Point(name, x, y) for name, x, y in zip(names, xs, ys)])
