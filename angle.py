from segment import Segment

class Angle:

    def __init__(self,ray1:Segment, vertex,ray2):
        self.ray1 = ray1
        self.vertex = vertex
        self.ray2 = ray2

    def get_start_point(self):
        return self.ray1.start if self.ray1.end == self.vertex else self.ray1.end

    def get_end_point(self):
        return self.ray2.start if self.ray2.end == self.vertex else self.ray2.end

    def __str__(self):
        return "∢" + self.get_start_point().name + self.vertex.name + self.get_end_point().name
