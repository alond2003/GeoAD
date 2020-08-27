from enum import Enum


class DegreeVar(Enum):
    Alpha = 0
    Beta = 1
    Gamma = 2
    Delta = 3
    Epsilon = 4
    Zeta = 5
    Eta = 6
    Theta = 7
    Iota = 8
    Kappa = 9
    Lambda = 10
    Mu = 11
    Nu = 12
    Xi = 13
    Omicron = 14
    Pi = 15
    Rho = 16
    Sigma = 17
    Tau = 18
    Upsilon = 19
    Phi = 20
    Psi = 21
    Omega = 22

    GA = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C0\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"

    def __str__(self):
        return DegreeVar.GA.value[int(self.value)]


# problem - what if i'm using more then 23 values?
# the representating will be easy (just A1,A2 and so forth)
# but adding values dynamicly to enum class is not the point of enum classes
# ):
# print(DegreeVar(23))
