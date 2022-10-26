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
import numpy as np
from .diag import diagonal
from .basic_ops import left_on

__all__ = ["find_concave_vertex", "convexify"]


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
    :return:  ([np.ndarray], [(int, int)])
        a list of indices of `verts` that constructs convex areas
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
            if diagonal(verts, indices, i_concave, i):
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
