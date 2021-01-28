'''from geo.abs.point import Point
from geo.abs.segment import Segment
from enum import Enum
from typing import List
from geo.real.expression import Degree

# greek_alphabet = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C0\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"

# print(greek_alphabet)


class Test(Enum):
    Alpha = 0
    Beta = 1

    def __str__(self):
        GA = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C0\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"
        return GA[int(self.value)]


print(Test.Alpha)
print(Test(0))


def a(x: List[int]):
    """Does shit"""
    for i in x:
        print(i)


a([1, 2, 3])


class Dog:
    def __init__(self):
        self.a = 3

    def __add__(self, other):
        if isinstance(other, Dog):
            return self.a + other.a
        elif isinstance(other, int):
            return self.a + other
        raise Exception("fuck")


# print("shit")
# d = Dog()
# dg = Dog()
# print(2 + d)

# print("oyoyo im here")
# da = Degree()
# da += 1
# print(da)
# ba = da.new_copy()


# test that array copying is by reference and not by value
from geo.abs.point import Point
from geo.abs.segment import Segment
from geo.real.realpoint import RealPoint

A, B, C, D = Point.createPoints("A", "B", "C", "D")
for i in (A, B, C, D):
    print(i)

d = RealPoint(0, 0, D)
print(f"{d.lines=}")

AD = Segment(A, D, isnew=True)
print(f"{d.lines=}")
print(f"{D.lines=}")


'''

from geo import *

h = Helper()