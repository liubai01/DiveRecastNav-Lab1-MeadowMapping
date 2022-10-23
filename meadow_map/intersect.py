"""
Check whether two lines would intersect

Refer to: https://github.com/w8r/orourke-compc
"""

import numpy as np
from .basic_ops import between, left, collinear


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
        return between(a, b, c)

    if collinear(a, b, d):
        return between(a, b, d)

    if collinear(c, d, a):
        return between(c, d, a)

    if collinear(c, d, b):
        return between(c, d, b)

    cd_cross = np.logical_xor(left(a, b, c), left(a, b, d))
    ab_cross = np.logical_xor(left(c, d, a), left(c, d, b))

    return ab_cross and cd_cross
