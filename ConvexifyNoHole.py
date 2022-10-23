"""
Turn a simple (concave) polygon into convex polys based on a divide-and-conquer method.
The method bases on Arkin, Ronald C.'s report "Path planning for a vision-based autonomous robot".

@inproceedings{arkin1987path,
  title={Path planning for a vision-based autonomous robot},
  author={Arkin, Ronald C},
  booktitle={Mobile Robots I},
  volume={727},
  pages={240--250},
  year={1987},
  organization={SPIE}
}
"""
import Diag
from DiagBasicOps import *
import numpy as np


def find_concave_vertex(verts: np.ndarray, indices: np.ndarray) -> int:
    """
    Return the index of `indices` where a concave vertex is at.
    :param verts:      np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:    np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :return:           int                     the index of `indices`
    """
    n = len(indices)
    for ia in range(n):
        ia_prev = ia - 1 if ia - 1 >= 0 else n - 1
        ia_next = ia + 1 if ia + 1 < n else 0

        if not left_on(verts[indices[ia_prev]], verts[indices[ia]], verts[indices[ia_next]]):
            return ia
    return -1


def convexify(verts: np.ndarray, indices: np.ndarray) -> [[np.ndarray], [(int, int)]]:
    """
    Turn a simple polygon into a list of convex polygons that shares the same area.
    This divide-and-conquer methods base on Arkin, Ronald C.'s report (1987).
    "Path planning for a vision-based autonomous robot"

    :param verts:       np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:     np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :return:  ([np.ndarray], [(int, int)])      a list of indices of `verts` that constructs convex areas
                                                e.g: [np.array(p1_i1, p1_i2, p1_i3, ..), np.array(p2_i1, ...), ..]

                                                list of diagonals that splits the input polygon.
                                                e.g: [(diag1_a_index, diag1_b_index), ...]
    """
    n = len(indices)
    i_concave = find_concave_vertex(verts, indices)

    # if there is no concave vertex, which means current polygon is convex. Return itself directly
    if i_concave == -1:
        return [indices], []

    # Find vertex i_break that `<i_concave, i_break>` is an internal edge
    i_break = -1
    for i in range(n):
        if i != i_concave:
            if Diag.diagonal(verts, indices, i_concave, i):
                i_break = i
                break

    # Not find (should not happen!)
    if i_break == -1:
        # Just keep that weird region for now
        # TBD: raise a warning
        return [indices], []

    # Split the simple polygon by <i_concave, i_break>
    indices1 = []
    indices2 = []
    i_now = i_concave

    while i_now != i_break:
        indices1.append(indices[i_now])
        i_now = (i_now + 1) % n
    indices1.append(indices[i_break])

    while i_now != i_concave:
        indices2.append(indices[i_now])
        i_now = (i_now + 1) % n
    indices2.append(indices[i_concave])

    # keep convexifying new-ly generated two areas in a recursive manner
    i1, diag1 = convexify(verts, indices1)
    i2, diag2 = convexify(verts, indices2)

    # merge results from recursively convexify
    ret_diag = [[i_concave, i_break]]
    for diag in diag1:
        ret_diag.append(
            (
                (diag[0] + i_concave) % n,
                (diag[1] + i_concave) % n
            )
        )
    for diag in diag2:
        ret_diag.append(
            (
                (diag[0] + i_break) % n,
                (diag[1] + i_break) % n
            )
        )

    return i1 + i2, ret_diag


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Sample test
    verts_poly = np.array(
        [
            [0., 0.], [0., 4.], [2., 4.],
            [1., 3.], [2., 1.], [3., 3.], [4., 1.],
            [1., 0.]
        ]
    )

    indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

    def plot_poly(verts, indices):
        x = []
        y = []
        for i in indices:
            x.append(verts[i][0])
            y.append(verts[i][1])

        x.append(verts[indices[0]][0])
        y.append(verts[indices[0]][1])

        plt.plot(x, y, c="blue")

    # draw the polygon
    polys, diags = convexify(verts_poly, indices_poly)
    plot_poly(verts_poly, indices_poly)

    # Plot diagonals that split original region in dotted line
    for d in diags:
        posA = verts_poly[indices_poly[d[0]]]
        posB = verts_poly[indices_poly[d[1]]]
        plt.plot([posA[0], posB[0]], [posA[1], posB[1]], "--", c="blue")

    itest = find_concave_vertex(verts_poly, indices_poly)

    plt.show()
