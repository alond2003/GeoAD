from segment import Segment
from angle import Angle
from evaluator import Evaluator

print("start\n")

AB = Segment("A","B")
AB.add_midpoints(["C"])
CD = Segment("C","D")
ACD = Angle(AB.get_subsegment_to("C"),"C",CD)
print(AB)
print(CD)
print(ACD)

ACB = Angle(AB.get_subsegment_to("C"),"C",AB.get_subsegment_from("C"))
print(ACB)
eval = Evaluator()
eval.add([AB,CD])
print(str(ACB) + " = " + str(eval.calc(ACB)))
# print(str(ACD) + " = " + str(eval.calc(ACD)))
print("\nend")