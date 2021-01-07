from geo.abs.segment import Segment
from geo.abs.absangle import AbsAngle
from geo.real.realangle import RealAngle
from geo.real.degree import Degree
from geo.handler import Handler
from geo.abs.point import Point
from geo.helper import Helper

# http://mathbitsnotebook.com/JuniorMath/Geometry/GEORules.html

"""
Axioms:

@ax1: All straight angles are congruent (180°).
@ax2: The whole is equal to the sum of its parts.
@ax3: A pair of alternate interior angles between 2 parallel lines and a transversal are equal
"""

"""
Theorems:
@th1: The sum of 2 angles on a line is 180° (adjacent supplementary angles / linear pair)
@th2: Two vertical angles are equal
@th3: All angles around a point sum up to 360°
@th4: Corresponding angles are equal and the sum of two consecutive interior angles is 180° (2pl&t)
@th5: Converse of angles between parallel lines (alternate interior / corresponding / consecutive) 
@th6: Tgit he sum of the measures of the interior angles of a triangle is 180°
@th7: The sum of the measures of the interior angles of a Quadrilateral is 360°
@th8: The size of an exterior angle at a vertex of a triangle equals the sum of the sizes of the interior angles at the other two vertices of the triangle
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
    geo = Handler(A, B, C, D)
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
    geo = Handler(A, B, C, D, E)
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
    geo = Handler(A, B, C, D, E)
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
    geo = Handler(A, B, C, D, E, F, G, H)
    geo.angles_calc()
    # Prove that corresponding angles are equal
    print(geo.angles[AEG], "=", geo.angles[CFG], end=", ")
    # Prove that the sum of 2 consecutive interior angles is 180°
    print(geo.angles[GEB], "+", geo.angles[DFH], "=", geo.angles[GEB] + geo.angles[DFH])
    if debug:
        print(geo.angles)


def th5(debug=False):
    """@ax3 + @th3 -> @th5 (proof by contradiction)"""
    # 3 part Proof:
    # 1. Converse alternate interior angles (proof by contradiction)
    # 2. Converse corresponding angles (proof based on 1)
    # 3. Converse consecutive interior angles (proof based on 1)

    """ 1. Prove Converse Alternate Interior angles """
    # Need to prove that AB || CD, based on equal alternate interior angles
    h = Helper()
    # Traverse GH (E in AB, F in CD)
    h.s("GEFH")
    # AB
    h.s("BEA")
    # CD
    h.s("DFC")
    # assume CD is not parallel to AB
    # therefore there must be a different parallel to CD that goes through E
    # That parallel is IJ
    h.s("IEJ")
    h.paras("IJ", "DC")
    # it is given that BEH == CFG
    h.equala("BEH", "CFG")
    # let's calc
    h.calc()
    # we get that BEI is zero
    if debug:
        print(h.geta("BEI"))
    # therefore IJ and therefore our assumption was wrong
    # Thus, AB || CD
    yield "AB || CD (proof by contradiction)"

    if debug:
        print("\n", "------------------------------------------\n" * 3)

    """ 2. Prove Converse equal corresponding angles """
    # Need to prove that AB || CD, based on equal corresponding angles
    h = Helper()
    # AB
    h.s("AEB")
    # CD
    h.s("CFD")
    # Traverse GH (E in AB, F in CD)
    h.s("GEFH")
    # it is given that GFD == GEB
    h.equala("GFD", "GEB")
    # lets see if GFD == HEA
    if debug:
        print(h.geta("GFD"), h.geta("HEA"))
    # because they are a pair of equal alternate interior angles, AB || CD (as was proven in 1)
    yield "AB || CD (proof by Converse Alternate Interior Angles)"

    if debug:
        print("\n", "------------------------------------------\n" * 3)

    """ 3. Prove converse consecutive interior angles """
    # Need to prove that AB || CD, based on consecutive interior angles
    h = Helper()
    # AB
    h.s("AEB")
    # CD
    h.s("CFD")
    # Traverse GH (E in AB, F in CD)
    h.s("GEFH")
    # it is given that GFD + BEH == 180
    x = Degree.given("x")
    h.seta("GFD", x)
    h.seta("BEH", 180 - x)
    # lets see if GFD == HEA
    if debug:
        print(h.geta("GFD"), h.geta("HEA"))
    # because they are a pair of equal alternate interior angles, AB || CD (as was proven in 1)
    yield "AB || CD (proof by Converse Alternate Interior Angles)"


def th6(debug=False):
    """@ax3 + @th1 -> @th6"""
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


def th7(debug=False):
    """@ax2 + @th6 -> @th7"""
    h = Helper()
    h.poly("ABCD")
    h.poly_diag("ABCD", "AC")
    if debug:
        h.calc()
        print(h.g().angles)
        print(
            " + ".join(
                map(
                    lambda x: f"({str(x)})",
                    [h.a("BAD"), h.a("ADC"), h.a("DCB"), h.a("CBA")],
                )
            ),
            "=",
            " + ".join(
                [
                    f"({str(i.deg) if isinstance(i, RealAngle) else str(i)})"
                    for i in [
                        h.geta("BAD"),
                        h.geta("ADC"),
                        h.geta("DCB"),
                        h.geta("CBA"),
                    ]
                ]
            ),
            "=",
            sum([h.geta("BAD"), h.geta("ADC"), h.geta("DCB"), h.geta("CBA")]),
        )
    return sum([h.geta("BAD"), h.geta("ADC"), h.geta("DCB"), h.geta("CBA")]) == 360


def th8(debug=False):
    """@th1 + @th6 -> @th8"""
    h = Helper()
    # h.s("BC", "AB", "ACD")
    h.tri("ABC")
    h.conts("AC", "ACD")
    if debug:
        h.calc()
        print(h.g().segments)
        print(h.g().angles)
    return h.geta("BAC"), h.geta("CBA"), h.geta("BCD")


print(list(th5(True)))
