"""
Check whether two lines would intersect

Refer to: https://github.com/w8r/orourke-compc
"""

import numpy as np
from DiagBasicOps import *


def intersect(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> bool:
    """
    Check whether 2D-line ab intersects with 2D-line cd
    :param a:  np.ndarray, a 2D vector (point of line ab)
    :param b:  np.ndarray, a 2D vector (point of line ab)
    :param c:  np.ndarray, a 2D vector (point of line cd)
    :param d:  np.ndarray, a 2D vector (point of line cd)
    :return: whether line intersects
    """
    if collinear(a, b, c):
        return True if between(a, b, c) else False

    if collinear(a, b, d):
        return True if between(a, b, d) else False

    if collinear(c, d, a):
        return True if between(c, d, a) else False

    if collinear(c, d, b):
        return True if between(c, d, b) else False

    return np.logical_xor(left(a, b, c), left(a, b, d)) and np.logical_xor(left(c, d, a), left(c, d, b))


if __name__ == "__main__":
    # Sample test
    import matplotlib.pyplot as plt

    a1 = np.array([0.5, 0.5])
    a2 = np.array([5.0, 5.0])

    b1 = np.array([0.5, 4.0])
    b2 = np.array([5.5, 2.0])

    c1 = np.array([1.0, 0.5])
    c2 = np.array([8.0, 5.0])

    print("Intersection of a && b")
    print(intersect(a1, a2, b1, b2))

    print("Intersection of a && c")
    print(intersect(a1, a2, c1, c2))

    print("Intersection of b && c")
    print(intersect(b1, b2, c1, c2))

    # Visualize 2D-lines: <a1, a2>, <b1, b2>, <c1, c2>
    plt.plot([a1[0], a2[0]], [a1[1], a2[1]], label="a")
    plt.plot([b1[0], b2[0]], [b1[1], b2[1]], label="b")
    plt.plot([c1[0], c2[0]], [c1[1], c2[1]], label="c")

    plt.legend()
    plt.show()
