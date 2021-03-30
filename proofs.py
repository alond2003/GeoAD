from geo.problemcollection import ProblemCollection
from geo.filehandler import print_points_from_file as _pggb
from geo.helper import Helper
from geo.real.expression import Degree

# http://mathbitsnotebook.com/JuniorMath/Geometry/GEORules.html

"""
Axioms:

_ax1: All straight angles are congruent (180°).
_ax2: The whole is equal to the sum of its parts.
_ax3: A pair of alternate interior angles between 2 parallel lines and a transversal are equal
"""

"""
Theorems:
_th1: The sum of 2 angles on a line is 180° (adjacent supplementary angles / linear pair)
_th2: Two vertical angles are equal
_th3: All angles around a point sum up to 360°
_th4: Corresponding angles are equal and the sum of two consecutive interior angles is 180° (2pl&t)
_th5: Converse of angles between parallel lines (alternate interior / corresponding / consecutive) 
_th6: The sum of the measures of the interior angles of a triangle is 180°
_th7: The sum of the measures of the interior angles of a Quadrilateral is 360°
_th8: The size of an exterior angle at a vertex of a triangle equals the sum of the sizes of the interior angles at the other two vertices of the triangle
"""


class ProofCollection(ProblemCollection):
    @classmethod
    def all(cls):
        ans = []
        for p in dir(cls):
            attr = getattr(cls, p)
            if p.startswith("t") and callable(attr):
                if p not in ["all", "check_all", "check_prob"]:
                    ans.append(attr)
        return ans

    @staticmethod
    def th1(print_proof=False):
        """_ax1 & _ax2 -> _th1"""
        h = Helper()
        h.ps_from_file(r"ggb_files\th1.ggb")
        h.s("ACB", "CD")
        h.calc(print_proof, use_theorems=[])
        # by ax1, ∢ACB = 180°
        ACB = h.a("ACB")
        # by ax2, ∢ACB is the sum of its parts
        parts = h.g().disassemble_angle(ACB)
        # therefore, we know sum(parts) = 180
        if print_proof:
            print(f"ACB = 180, {ACB} = {' + '.join(map(str,parts))}")
            print(f"⇓")
            print(f"{' + '.join(map(str,parts))} = 180")

        return None, None

    @staticmethod
    def th2(print_proof=False):
        """_th1 -> _th2"""
        h = Helper()
        h.ps_from_file(r"ggb_files\th2.ggb")
        h.s("AEB", "CED")
        h.calc(print_proof, use_theorems=[1])
        if print_proof:
            print(
                f"{h.a('AEC')} = {h.geta('AEC')}, {h.a('BED')} = {h.geta('BED')}"
            )
            print(f"⇓")
            print(f"{h.a('AEC')} = {h.a('BED')}")
        return (h.geta("AEC") == h.geta("BED"),), (True,)

    @staticmethod
    def th3(print_proof=False):
        """_th1 -> _th3"""
        h = Helper()
        h.ps_from_file(r"ggb_files\th3.ggb")
        h.s("AEB", "CED")
        h.calc(print_proof, use_theorems=[1])
        E = h.p("E")
        aangs_around_E = h.g().get_angles_around_point(E)
        sum_aangs_around_E = sum(h.geta(*aangs_around_E))
        if print_proof:
            print(
                " + ".join(map(str, aangs_around_E)),
                "=",
                " + ".join(map(str, h.geta(*aangs_around_E))),
                "=",
                sum_aangs_around_E,
            )
            print("⇓")
            print(" + ".join(map(str, aangs_around_E)), "=", sum_aangs_around_E)

        return (sum_aangs_around_E,), (360,)
        # return sum(h.geta(*h.g().get_angles_around_point(h.p("E")))))

    @staticmethod
    def th4(print_proof=False):
        """_th1 & _ax3 -> _th4"""

        """example of types of angles:
                             /
                            /
                         8 / 7
            --------------/------
                       5 / 6
                        /
                       /
                    4 / 3
            ---------/-------
                  1 / 2
                   /
                  /
            5 = 3 (alternate interior angles)
            1 = 5 (Corresponding angles)
            3+6 = 180° (consecutive interior angles)
        """

        h = Helper()
        h.ps_from_file(r"ggb_files\th4.ggb")
        h.s("AEB", "CFD", "HEFG")
        h.paras("AB", "CD")
        # ax3 - set ∢GEA = ∢HFD (alternate interior angles, AB || CD, HEFG traversal)
        h.equala("GEA", "HFD")
        h.calc(print_proof, use_theorems=[1, 2, 3])
        # Corresponding angles example (GEA & GFC)
        corresponding = h.geta("GEA") == h.geta("GFC")
        # Consecutive interior angles example (BEG & HFD)
        consecutive = h.geta("BEG") + h.geta("HFD") == 180
        if print_proof:
            print(
                f"{h.a('GEA')} = {h.geta('GEA')}, {h.a('GFC')} = {h.geta('GFC')}"
            )
            print("⇓")
            print(f"{h.a('GEA')} = {h.a('GFC')} (corresponding)")
            print()
            print(
                f"{h.a('BEG')} + {h.a('HFD')} = ({h.geta('BEG')}) + ({h.geta('HFD')}) = {sum(h.geta('BEG','HFD'))}"
            )
            print("⇓")
            print(f"{h.a('BEG')} + {h.a('HFD')} = 180 (consecutive)")

        return (corresponding, consecutive), (True, True)

    @staticmethod
    def th5(print_proof=False):
        """_ax3 + _th4 -> _th5 (proof by contradiction)
        3 part Proof:
        1. Converse alternate interior angles (proof by contradiction)
        2. Converse corresponding angles (proof based on 1)
        3. Converse consecutive interior angles (proof based on 1)
        """
        # READ: https://en.wikipedia.org/wiki/Playfair%27s_axiom

        ans = [[], []]

        """ 1. Prove Converse Alternate Interior angles """
        # We Need to prove that AB || CD, based on equal alternate interior angles
        h = Helper()
        h.ps_from_file(r"ggb_files\th5_1.ggb")
        h.s("AEB", "CFD", "HEFG")
        # Assume CD is not parallel to AB
        # Therefore, there must be a different parallel to CD that goes through E
        # That parallel is IJ
        h.s("IEJ")
        h.paras("IJ", "CD")
        # It is given that BEG == CFH
        h.equala("BEG", "CFH")
        # Let's calc
        h.calc(print_proof, use_theorems=[1, 2, 3, 4])
        # We get that BEJ is zero
        ans[0].append(h.geta("BEJ") == 0)
        ans[1].append(True)
        # Therefore IJ is the same as AB
        # And therefore our assumption that AB is not parallel to CD was wrong
        # Thus, AB || CD
        if print_proof:
            print(f"{h.a('BEJ')} = {h.geta('BEJ')})")
            print(f"⇓")
            print(f"(IJ is the same as CD) -> AB || CD")

            print("\n")

        """ 2. Prove Converse equal corresponding angles """
        # We need to prove that AB || CD, based on equal corresponding angles
        h = Helper()
        h.ps_from_file(r"ggb_files\th5_2.ggb")
        h.s("AEB", "CFD", "HEFG")
        # it is given that HEB == HFD
        h.equala("HEB", "HFD")
        # lets see if GEA == HFD
        h.calc(print_proof, use_theorems=[1, 2, 3, 4])
        ans[0].append(h.geta("GEA") == h.geta("HFD"))
        ans[1].append(True)
        # because they are a pair of equal alternate interior angles, AB || CD (as was proven in 1)
        if print_proof:
            print(
                f"{h.a('GEA')} = {h.geta('GEA')} = {h.geta('HFD')} = {h.a('HFD')}"
            )
            print(f"⇓")
            print(
                f"AB || CD (Converse alternate interior angles - proven before)"
            )

            print("\n")

        """ 3. Prove converse consecutive interior angles """
        # We need to prove that AB || CD, based on consecutive interior angles
        h = Helper()
        h.ps_from_file(r"ggb_files\th5_3.ggb")
        h.s("AEB", "CFD", "HEFG")
        # it is given that BEG + HFD == 180
        x = h.given(Degree, "x")
        h.seta("BEG", x)
        h.seta("HFD", 180 - x)
        # lets see if GEA == HFD
        h.calc(print_proof, use_theorems=[1, 2, 3, 4])
        ans[0].append(h.geta("GEA") == h.geta("HFD"))
        ans[1].append(True)
        # because they are a pair of equal alternate interior angles, AB || CD (as was proven in 1)
        if print_proof:
            print(
                f"{h.a('GEA')} = {h.geta('GEA')} = {h.geta('HFD')} = {h.a('HFD')}"
            )
            print(f"⇓")
            print(
                f"AB || CD (Converse alternate interior angles - proven before)"
            )

        return tuple(ans[0]), tuple(ans[1])

    @staticmethod
    def th6(print_proof=False):
        """_ax3 + _th1 -> _th6"""

        h = Helper()
        h.ps_from_file(r"ggb_files\th6.ggb")
        h.tri("ABC")
        h.s("DCE")
        h.paras("AB", "DE")
        h.calc(print_proof, use_theorems=[1, 2, 3, 4, 5])
        if print_proof:
            print(
                f"{h.a('CAB')} + {h.a('ABC')} + {h.a('BCA')} = ({h.geta('CAB')}) + ({h.geta('ABC')}) + ({h.geta('BCA')})",
                f"= {sum(h.geta('CAB', 'ABC', 'BCA'))}",
            )
            print(f"⇓")
            print(f"sum of angles in △ABC is 180°")

        return (sum(h.geta("CAB", "ABC", "BCA")),), (180,)

    @staticmethod
    def th7(print_proof=False):
        """_ax2 + _th6 -> _th7"""
        h = Helper()
        h.ps_from_file(r"ggb_files\th7.ggb")
        h.poly("ABCD")
        h.s("AC")
        h.calc(print_proof, use_theorems=[1, 2, 3, 4, 5, 6])
        if print_proof:
            print(
                " + ".join(map(str, h.a("BAD", "ADC", "DCB", "CBA"))),
                "=",
                f"({') + ('.join(map(str, h.geta('BAD', 'ADC', 'DCB', 'CBA')))})",
                "=",
                sum(h.geta("BAD", "ADC", "DCB", "CBA")),
            )
            print(f"⇓")
            print(f"sum of angles in ▱ ABCD is 360°")

        return (sum(h.geta("BAD", "ADC", "DCB", "CBA")),), (360,)

    @staticmethod
    def th8(print_proof=False):
        """_th1 + _th6 -> _th8"""
        h = Helper()
        h.ps_from_file(r"ggb_files\th8.ggb")
        h.tri("ACB")
        h.conts("AC", "ACD")
        h.calc(print_proof, use_theorems=range(1, 8))
        if print_proof:
            print(
                f"{h.a('BCD')} = {h.geta('BCD')},",
                f"{h.a('BAC')} + {h.a('CBA')} = ({h.geta('BAC')}) + ({h.geta('CBA')})",
                f"= {sum(h.geta('BAC','CBA'))}",
            )
            print(f"⇓")
            print(f"{h.a('BCD')} = {h.a('BAC')} + {h.a('CBA')}")

        return (h.geta("BCD") == sum(h.geta("BAC", "CBA")),), (True,)

    # @staticmethod
    # def _thn(print_proof=False):

    #     h = Helper()
    #     h.ps_from_file()
    #     _pggb()


if __name__ == "__main__":
    # ProofCollection.check_all()
    print(ProofCollection.th6(True))
