from segment import Segment
from absangle import AbsAngle
from realangle import RealAngle
from degree import Degree
from geohandler import GeoHandler
from point import Point
from helper import Helper

# http://mathbitsnotebook.com/JuniorMath/Geometry/GEORules.html

"""
Axioms:

@ax1: All straight angles are congruent (180°).
@ax2: The whole is equal to the sum of its parts.
@ax3: A pair of alternate interior angles between 2 parallel lines and a transversal are equal
"""

"""
Theorems:
@th1: the sum of 2 angles on a line is 180° (adjacent supplementary angles / linear pair)
@th2: 2 vertical angles are equal
@th3: all angles around a point sum up to 360°
@th4: Corresponding angles are equal and the sum of two consecutive interior angles is 180° (2pl&t)
@th5: The sum of the measures of the interior angles of a triangle is 180°.
"""


def th1(debug=False):
    """@ax1 & @ax2 -> @th1"""
    # Create line AB, C point on AB, CD line from C
    A, B, C, D = Point.createPoints("A", "B", "C", "D")
    AB = Segment(A, B, True)
    AB.set_midpoints(C)
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
    if debug:
        print(geo.angles)


def th2(debug=False):
    """@th1 -> @th2"""
    # Create lines AB and CD, E is their intersection point
    A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
    AB = Segment(A, B, True)
    AB.set_midpoints(E)
    CD = Segment(C, D, True)
    CD.set_midpoints(E)
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
    if debug:
        print(geo.angles)


def th3(debug=False):
    """@th1 -> @th3"""
    # Create lines AB and CD, E is their intersection point
    A, B, C, D, E = Point.createPoints("A", "B", "C", "D", "E")
    AB = Segment(A, B, True)
    AB.set_midpoints(E)
    CD = Segment(C, D, True)
    CD.set_midpoints(E)
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
    if debug:
        print(geo.angles)


def th4(debug=False):
    """@th1 & @ax3 -> @th4"""
    # Create AB||CD, GFEH transversal: E ∈ AB, F ∈ CD
    A, B, C, D, E, F, G, H = Point.createPoints(8)
    AB = Segment(A, B, True)
    AB.set_midpoints(E)
    CD = Segment(C, D, True)
    CD.set_midpoints(F)
    GH = Segment(G, H, True)
    GH.set_midpoints(F, E)
    AB.set_parallel(CD)
    # Corresponding [מתאימות] angles example (AEG & CFG)
    AE = AB.get_subsegment_to(E)
    GE = GH.get_subsegment_to(E)
    AEG = AbsAngle(AE, E, GE)
    CF = CD.get_subsegment_to(F)
    GF = GH.get_subsegment_to(F)
    CFG = AbsAngle(CF, F, GF)
    # Consecutive interior [חד צדדיות] angles example (GEB & DFH)
    EB = AB.get_subsegment_from(E)
    GEB = AbsAngle(GE, E, EB)
    FD = CD.get_subsegment_from(F)
    FH = GH.get_subsegment_from(F)
    DFH = AbsAngle(FD, F, FH)
    geo = GeoHandler(A, B, C, D, E, F, G, H)
    geo.angles_calc()
    # Prove that corresponding angles are equal
    print(geo.angles[AEG], "=", geo.angles[CFG], end=", ")
    # Prove that the sum of 2 consecutive interior angles is 180°
    print(geo.angles[GEB], "+", geo.angles[DFH], "=", geo.angles[GEB] + geo.angles[DFH])
    if debug:
        print(geo.angles)


def th5(debug=False):
    """@ax3 + @th1 -> @th5"""
    h = Helper()
    h.s("CA", "CB", "ECD", "BA")
    # h.inita()
    # print(h.g().angles)
    # h.g().
    # h.s("DCE", "CB", "CA", "AB")
    h.paras("DCE", "AB")
    if debug:
        h.calc()
        print(h.g().angles)
        print([str(i) for i in h.g().find_all_triangles()])
    return h.geta("BAC") + h.geta("ACB") + h.geta("CBA") == 180


# for i, j in enumerate([th1, th2, th3, th4]):
#     print(f"th{i+1}:", end=" ")
#     j()
#     Degree.reset()

print(th5(True))
