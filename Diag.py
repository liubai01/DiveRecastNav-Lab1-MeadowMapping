"""
Check whether a simple polygon diagonal is an internal diagonal or not.

A diagonal of simple polygon is internal iff
(1) An internal diagonal does not intersect with any edge in polygon (except for edge incident to them)
(2) For an internal diagonal <a, b>, line <a, b> should in the cone of <a-, a, a+>.
    where a- and a+ are previous and next vertex of a.

Refer to: https://github.com/w8r/orourke-compc
"""

from DiagIntersect import *
from DiagBasicOps import *


def diagonalie(verts: np.ndarray, indices: np.ndarray, ia: int, ib: int) -> bool:
    """
    Check whether diagonal <ia, ib> is internal/external diagonal that
    does not intersect with any edge in poly (except for incident edge of ia, ib).
    :param verts:    np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:  np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :param ia:       int,                    index of `indices` (index to array `verts`) of tested poly diagonal
    :param ib:       int,                    index of `indices` (index to array `verts`) of tested poly diagonal
    :return: whether <ia, ib> is an external or internal diagonal
    """
    n = len(indices)

    for now_i in range(n):
        # exclude edges contains point a and point b
        if indices[now_i] == indices[ia] or indices[now_i] == indices[ib]:
            continue
        next_i = (now_i + 1) % n
        if indices[next_i] == indices[ia] or indices[next_i] == indices[ib]:
            continue

        if intersect(
                verts[indices[ia]], verts[indices[ib]],
                verts[indices[now_i]], verts[indices[next_i]]
        ):
            return False
    return True


def in_cone(verts, indices, ia, ib):
    """
    Check whether diagonal <ia, ib> is in the cone of <a-, a, a+>.
    (a- and a+ are previous and next vertex of vertx a)

    Refer to "Computational Geometry in C" Section 1.6.3 for details.

    :param verts:      np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:    np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :param ia:         int,                    index of `indices` (index to array `verts`) of tested poly diagonal
    :param ib:         int,                    index of `indices` (index to array `verts`) of tested poly diagonal
    :return:
    """
    # Check whether (ia, ib) is in cone of (ia-, ia, ia+)
    n = len(indices)
    ia_prev = ia - 1 if ia - 1 >= 0 else n - 1
    ia_next = ia + 1 if ia + 1 < n else 0

    # turn index of `indices` to index of `verts`
    ia, ib = indices[ia], indices[ib]
    ia_prev, ia_next = indices[ia_prev], indices[ia_next]

    # Convex
    if left_on(verts[ia_prev], verts[ia], verts[ia_next]):
        return left(verts[ia], verts[ib], verts[ia_prev]) and \
               left(verts[ib], verts[ia], verts[ia_next])
    # Concave
    return not (left_on(verts[ia], verts[ib], verts[ia_next]) and \
                left_on(verts[ib], verts[ia], verts[ia_prev]))


def diagonal(verts, indices, ia, ib):
    return in_cone(verts, indices, ia, ib) and in_cone(verts, indices, ib, ia) and diagonalie(verts, indices, ia, ib)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Sample test
    verts_poly = np.array(
        [
            [0., 0.], [0., 4.], [2., 4.],
            [1., 3.], [2., 1.], [3., 3.], [4., 1.],
            [1., 0.]
        ][::-1]
    )
    indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

    # Visualize 4 diagonal status
    plt_ids = [221, 222, 223, 224]
    dias = [0, 2, 4, 6]
    dibs = [2, 4, 6, 2]

    for pid, dia, dib in zip(plt_ids, dias, dibs):
        diag = diagonalie(verts_poly, indices_poly, dia, dib)
        lbl = "not intersect" if diag else "intersect"
        if diag:
            internal = in_cone(verts_poly, indices_poly, dia, dib)
            lbl += " (internal)" if internal else " (external)"

        plt.subplot(pid)
        # print polygon
        plt.plot(
            list(verts_poly[:, 0]) + [verts_poly[0, 0]],
            list(verts_poly[:, 1]) + [verts_poly[0, 1]]
        )
        # print sampled diagonal
        plt.plot(
            [verts_poly[dia, 0], verts_poly[dib, 0]],
            [verts_poly[dia, 1], verts_poly[dib, 1]],
            label=lbl
        )
        plt.legend()
    plt.show()
