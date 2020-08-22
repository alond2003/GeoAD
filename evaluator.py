from segment import Segment
from angle import Angle

class Evaluator:

    def __init__(self):
        self.all = []

    def add(self,x):
        if type(x) is list:
            self.all += x
        else:
            self.all.append(x)

    def calc(self,x):
        if type(x) is Segment:
            raise Exception("length not supported yet")
        elif type(x) is Angle:
            if self.is_180_angle(x):
                return 180
            else:
                raise Exception("non-straight angles not supported yet")

    def is_180_angle(self,ang):
        maybeline = Segment(ang.get_start(),ang.get_end())

        for i in self.all:
            if type(i) is Segment and i.is_subsegment(maybeline):
                return True
        return False

    def __str__(self):
        return ", ".join(map(str,self.all))
