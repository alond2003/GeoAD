
class Segment:
    
    def __init__(self,pointstart,pointend,isnew=False):
        self.start = pointstart
        self.end = pointend
        self.midpoints = []
        self.isnew = isnew
        if self.isnew:
            self.start.add_linefrom(self)
            self.end.add_linefrom(self)

    def add_midpoints(self,lst):
        if type(lst) is list:
            self.midpoints = lst
            for i in lst:
                i.add_linefrom(self)
        else:
            self.midpoints.append(lst)
            lst.add_linefrom(self)


    def get_all_points(self):
        return [self.start] + self.midpoints + [self.end]
    
    def get_subsegment_to(self,point):
        #what about if point == start?
        if point in self.midpoints:
            res = Segment(self.start,point)
            res.add_midpoints(self.midpoints[0:self.midpoints.index(point)])
            return res
        elif point == self.end:
            return self
        return None

    def get_subsegment_from(self,point):
        #what about if point == end?
        if point in self.midpoints:
            res = Segment(point,self.end)
            res.add_midpoints(self.midpoints[self.midpoints.index(point)+1:])
            return res
        elif point == self.start:
            return self
        return None

    def is_subsegment(self,seg):
        idxs = []
        for i in seg.get_all_points():
            try:
                idxs.append(self.get_all_points().index(i))
            except ValueError:
                return False
        return all(i<j for i,j in zip(idxs,idxs[1:])) or all(i>j for i,j in zip(idxs,idxs[1:]))

    def __str__(self):
        return "Segment " + self.start.name+self.end.name + ": " + str([i.name for i in self.midpoints])

    def __hash__(self):
        return hash(tuple(self.get_all_points()))

    def __eq__(self,other):
        return other.get_all_points() == self.get_all_points() or other.get_all_points()[::-1] == self.get_all_points()



"""
t = Segment("A","B")
print("hello " +str(t))
t.add_midpoints(["C","D"])
print(t)
"""