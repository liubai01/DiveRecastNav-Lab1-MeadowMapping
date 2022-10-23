"""
Check whether two lines would intersect

Refer to: https://github.com/w8r/orourke-compc
"""

import numpy as np
from .DiagBasicOps import *


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
