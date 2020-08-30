from segment import Segment
from absangle import AbsAngle
from realangle import RealAngle
from degree import Degree
from geohandler import GeoHandler
from point import Point

# http://mathbitsnotebook.com/JuniorMath/Geometry/GEORules.html

"""
Axioms:

@ax1: All straight angles are congruent (180°).
@ax2: The whole is equal to the sum of its parts.

"""

"""
Theorems:

@th1: the sum of 2 angles on a line is 180° (adjacent supplementary angles / linear pair)
@th2: 2 vertical angles are equal
@th3: all angles around a point sum up to 360°
"""


def th1():
    """@ax1 & @ax2 -> @th1"""
    # Create line AB, C point on AB, CD line from C
    A, B, C, D = Point.createPoints("A", "B", "C", "D")
    AB = Segment(A, B, True)
    AB.add_midpoints(C)
    CD = Segment(C, D, True)
    # Create Angle ACD
    AC = AB.get_subsegment_to(C)
    ACD = AbsAngle(AC, C, CD)
    # Create Angle DCB
    CB = AB.get_subsegment_from(C)
    DCB = AbsAngle(CD, C, CB)
    # Prove the sum of the angles is equal to 180°
    geo = GeoHandler(A, B, C, D)
    geo.angles_calc()
    print(geo.angles[ACD], "+", geo.angles[DCB], "=", geo.angles[ACD] + geo.angles[DCB])
    # print(geo.angles)


def th2():
    """@th1 -> @th2"""
    # Create lines AB and CD, E is their intersection point
    A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
    AB = Segment(A, B, True)
    AB.add_midpoints(E)
    CD = Segment(C, D, True)
    CD.add_midpoints(E)
    # Create Angle AEC
    AE = AB.get_subsegment_to(E)
    CE = CD.get_subsegment_to(E)
    AEC = AbsAngle(AE, E, CE)
    # Create Angle BED
    EB = AB.get_subsegment_from(E)
    ED = CD.get_subsegment_from(E)
    BED = AbsAngle(EB, E, ED)
    # Prove the 2 vertical Angles are equal
    geo = GeoHandler(A, B, C, D, E)
    geo.angles_calc()
    print(geo.angles[AEC], "=", geo.angles[BED])
    # print(geo.angles)


def th3():
    """@th1 -> @th3"""
    # Create lines AB and CD, E is their intersection point
    A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
    AB = Segment(A, B, True)
    AB.add_midpoints(E)
    CD = Segment(C, D, True)
    CD.add_midpoints(E)
    # Create the 4 angles around point E
    AE = AB.get_subsegment_to(E)
    CE = CD.get_subsegment_to(E)
    AEC = AbsAngle(AE, E, CE)
    EB = AB.get_subsegment_from(E)
    CEB = AbsAngle(CE, E, EB)
    ED = CD.get_subsegment_from(E)
    BED = AbsAngle(EB, E, ED)
    DEA = AbsAngle(ED, E, AE)
    # Prove the sum of all point around point E is 360°
    geo = GeoHandler(A, B, C, D, E)
    geo.angles_calc()
    print(
        geo.angles[AEC],
        "+",
        geo.angles[CEB],
        "+",
        geo.angles[BED],
        "+",
        geo.angles[DEA],
        "=",
        geo.angles[AEC] + geo.angles[CEB] + geo.angles[BED] + geo.angles[DEA],
    )
    # print(geo.angles)


for i, j in enumerate([th1, th2, th3]):
    print(f"th{i}:", end=" ")
    j()
    Degree.reset()
