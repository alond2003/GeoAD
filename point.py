class Point:

    nextId = 0

    def __init__(self,name):
        self.name = name
        self.id = Point.nextId
        Point.nextId += 1
        self.lines = []

    def __str__(self):
        return self.name + f"({self.id})"

    def add_linefrom(self,*lines):
        self.lines += list(lines)

    def __hash__(self):
        return hash(self.id)
        
    def __eq__(self,other):
        return other.id == self.id

    @staticmethod
    # hello
    def createPoints(*point_names):
        res = []
        for i in point_names:
            res.append(Point(i))
        return tuple(res) 
