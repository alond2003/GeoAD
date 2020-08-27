"""
x + y + z + w = 13
2x + 3y − w = −1
−3x + 4y + z + 2w = 10
x + 2y − z + w = 1

"""

import numpy as np

A = np.array([[1, 1, 1, 1], [2, 3, 0, -1], [-3, 4, 1, 2], [1, 2, -1, 1]])
B = np.array([13, -1, 10, 1])
X = np.linalg.solve(A, B)
print(list(X))
