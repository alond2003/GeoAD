class Segment:
    
    def __init__(self,pointstart,pointend):
        self.start = pointstart
        self.end = pointend
        self.midpoints = []

    def add_midpoints(self,lst):
        self.midpoints = lst

    def get_all_points(self):
        return [self.start] + self.midpoints + [self.end]
    
    def get_subsegment_to(self,point):
        #what about if point == start or == end?
        if point in self.midpoints:
            res = Segment(self.start,point)
            res.add_midpoints(self.midpoints[0:self.midpoints.index(point)])
            return res
        return None

    def get_subsegment_from(self,point):
        #what about if point == start or == end?
        if point in self.midpoints:
            res = Segment(point,self.end)
            res.add_midpoints(self.midpoints[self.midpoints.index(point)+1:])
            return res
        return None

    def is_subsegment(self,seg):
        idxs = []
        for i in seg.get_all_points:
            idxs.append(self.get_all_points().index(i))
        return all(i<j for i,j in zip(idxs,idxs[1:])) or all(i>j for i,j in zip(idxs,idxs[1:]))

    def __str__(self):
        return "Segment " + self.start+self.end + ": " + str(self.midpoints)





t = Segment("A","B")
print("hello " +str(t))
t.add_midpoints(["C","D"])
print(t)
