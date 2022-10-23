"""
Basic operations of Computational Geometry,
which would be used in Meadow Mapping

Refer to: https://github.com/w8r/orourke-compc
"""
import numpy as np
from utils import *


def left(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> bool:
    """
    Check whether 2D-point z is at left of 2D-line xy in 2D space.
    :param x: np.ndarray, a 2D vector (point of line xy)
    :param y: np.ndarray, a 2D vector (point of line xy)
    :param z: np.ndarray, a 2D vector (point)
    :return: whether point z is at left of xy
    """
    xy = y - x
    yz = z - y
    return (xy[0] * yz[1] - xy[1] * yz[0]) > 0


def left_on(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> bool:
    """
    Check whether 2D-point z is at left or on of 2D-line xy in 2D space.
    :param x: np.ndarray, a 2D vector (point of line xy)
    :param y: np.ndarray, a 2D vector (point of line xy)
    :param z: np.ndarray, a 2D vector (point)
    :return: whether point z is at left of or on xy
    """
    xy = y - x
    yz = z - y
    return (xy[0] * yz[1] - xy[1] * yz[0]) >= 0


def collinear(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> bool:
    """
    Check whether 2D points x, y, z are on the same 2D-line in 2D space.
    :param x: np.ndarray, a 2D vector (point)
    :param y: np.ndarray, a 2D vector (point)
    :param z: np.ndarray, a 2D vector (point)
    :return: whether there is a line pass x, y, z at the same time
    """
    xy = y - x
    yz = z - y

    area = xy[0] * yz[1] - xy[1] * yz[0]
    # distance of z to line xy
    dist = area / (xy[0] * xy[0] + xy[1] * xy[1] + 1e-6)

    return np.abs(dist) < 1e-6


def between(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> bool:
    """
    Assume 2D-points x, y, z are collinear. Test whether z is
    between 2D-line xy or not.
    :param x: np.ndarray, a 2D vector (point of line xy)
    :param y: np.ndarray, a 2D vector (point of line xy)
    :param z: np.ndarray, a 2D vector (point)
    :return:
    """
    if x[0] != y[0]:
        if x[0] <= z[0] <= y[0]:
            return True
        if x[0] >= z[0] >= y[0]:
            return True
    else:
        if x[1] <= z[1] <= y[1]:
            return True
        if x[1] >= z[1] >= y[1]:
            return True
    return False


if __name__ == "__main__":
    # Sample test
    a = np.array([0, 0], dtype=np.float64)
    b = np.array([8, 4], dtype=np.float64)
    c = np.array([0, 1], dtype=np.float64)
    d = np.array([4, 2], dtype=np.float64)
    e = np.array([4.2, 2.2], dtype=np.float64)

    # Print All points
    print("a: {}".format(a))
    print("b: {}".format(b))
    print("c: {}".format(c))
    print("d: {}".format(d))
    print()

    print("c is left to ab?")
    print(left(a, b, c))
    print()

    print("d is left ab?")
    print(left(a, b, d))
    print()

    print("d is left or on ab?")
    print(left_on(a, b, d))
    print()

    print("d is on ab?")
    print(collinear(a, b, d))
    print()

    print("d is between ab?")
    print(collinear(a, b, d) and between(a, b, d))
    print()

    print("b is between ad?")
    print(collinear(a, d, b) and between(a, d, b))
    print()

    print("e is on ab?")
    print(collinear(a, b, e))
    print()

    plt.scatter([a[0]], [a[1]], label="a")
    plt.scatter([b[0]], [b[1]], label="b")
    plt.scatter([c[0]], [c[1]], label="c")
    plt.scatter([d[0]], [d[1]], label="d")
    plt.scatter([e[0]], [e[1]], label="e")

    plt.plot([a[0], b[0]], [a[1], b[1]])

    plt.legend()
    plt.show()
