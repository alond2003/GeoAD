from geo.abs.point import Point


class RealPoint(Point):
    def __init__(self, x, y, p):
        """Create RealPoint based on Point p and coordinates (x,y)"""
        self.x = x
        self.y = y
        self.copy(p)

    def __repr__(self):
        """Return the point's name, id and coordinates"""
        return f"<{self.name}({self.id})({self.x},{self.y})>"
