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
        if point in self.midpoints:
            return Segment(self.start,point)
        return None

    def get_subsegment_from(self,point):
        if point in self.midpoints:
            return Segment(point,self.end)
        return None

    def is_subsegment(self,seg):
        return seg.start in self.get_all_points() and seg.end in self.get_all_points()

    def __str__(self):
        return "Segment " + self.start+self.end + ": " + str(self.midpoints)





t = Segment("A","B")
print("hello " +str(t))
t.add_midpoints(["C","D"])
print(t)
