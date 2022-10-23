"""
Turn a simple (concave) polygon with holes(obstacles) into convex polys based on a divide-and-conquer method.
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

from .DiagIntersect import *
from .ConvexifyNoHole import *
from .utils import *

__all__ = ["merge_hole"]

def merge_hole(verts_poly: np.ndarray, indices_poly: np.ndarray,
               verts_hole: np.ndarray, indices_hole: np.ndarray) -> (np.ndarray, np.ndarray, (int,)):
    """
    Merge hole into polygon. Connect arbitrary vertex on hole to some vertex in polygon in sight.

    This method refer to Recast Navigation's implementation.

    Remark: `indices_poly` should be in counter-clock wise.
    Remark: `indices_hole` should be in counter-clock wise.
    :param verts_poly:     np.ndarray (#verts, 2)  a list of 2D-vertices position of simple polygon
    :param indices_poly:   np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`) of simple polygon
    :param verts_hole:     np.ndarray (#verts, 2)  a list of 2D-vertices position of hole
    :param indices_hole:   np.ndarray (#verts, 2)  a list of polygon vertex index (to array `verts`) of hole

    :return: (verts_out: np.ndarray (#verts, 2), indices_out: np.ndarray (#vert, ), diag: (0, 1)):
            (1) output a polygon in (verts_out, indices_out) that merges the hole.
            (2) `diag` is index of edge that merges poly and hole.
    """
    n_poly = len(indices_poly)
    n_hole = len(indices_hole)

    hole_i = indices_hole[0]

    # traverse all vertex in poly to check whether it is in `hole_i`'s line of sight
    for poly_i in indices_poly:
        okay = True
        # check whether `hole_i, poly_i` intersects with each poly edge
        for polyEdge in range(n_poly):
            polyAi = indices_poly[polyEdge]
            polyBi = indices_poly[(polyEdge + 1) % n_poly]
            # skip check with shared vertex `poly_i`
            if polyAi == poly_i or polyBi == poly_i:
                continue
            if intersect(verts_poly[poly_i], verts_hole[hole_i], verts_poly[polyAi], verts_poly[polyBi]):
                okay = False
                break
        # check whether `hole_i, poly_i` intersects with each hole edge
        if not okay:
            continue
        for holeEdge in range(n_hole):
            hole_ai = indices_hole[holeEdge]
            hole_bi = indices_hole[(holeEdge + 1) % n_hole]
            # skip check with shared vertex `hole_i`
            if hole_ai == hole_i or hole_bi == hole_i:
                continue
            if intersect(verts_poly[poly_i], verts_hole[hole_i], verts_hole[hole_ai], verts_hole[hole_bi]):
                okay = False
                break

        if okay:
            verts_out = np.concatenate((verts_poly, verts_hole), axis=0)
            indices_out = [indices_poly[poly_i], indices_hole[hole_i] + n_poly]
            # all hole index applied an offset of nPoly

            now_holei = (hole_i + 1) % n_hole
            while now_holei != hole_i:
                indices_out.append(indices_hole[now_holei] + n_poly)
                now_holei = (now_holei + 1) % n_hole

            indices_out.append(indices_hole[hole_i] + n_poly)
            indices_out.append(indices_poly[poly_i])

            now_polyi = (poly_i + 1) % n_poly
            while now_polyi != poly_i:
                indices_out.append(indices_poly[now_polyi])
                now_polyi = (now_polyi + 1) % n_poly

            return verts_out, indices_out, (indices_hole[hole_i] + n_poly, indices_poly[poly_i])


if __name__ == "__main__":
    verts_mypoly = np.array(
        [
            [0., 0.], [0., 4.], [2., 4.],
            [1., 3.], [2., 1.], [3., 3.], [4., 1.],
            [1., 0.]
        ]
    )
    indices_mypoly = [verts_mypoly.shape[0] - i - 1 for i in range(verts_mypoly.shape[0])]  # CCW

    vertsHole = np.array(
        [
            [0.5, 0.5], [0.2, 1.5], [0.4, 2.],
            [1.8, 0.5]
        ]
    )
    indicesHole = [i for i in range(vertsHole.shape[0])]  # CW

    verts, indices, mergeLineSeg = merge_hole(verts_mypoly, indices_mypoly, vertsHole, indicesHole)
    polys, diags = convexify(verts, indices)

    # plot the result
    plot_poly(verts_mypoly, indices_mypoly, [0, 0, 1.0])
    plot_poly(vertsHole, indicesHole, [0.0, 0.0, 0.0])
    # plot all diags. with dotted line
    for d in diags:
        posA = verts[indices[d[0]]]
        posB = verts[indices[d[1]]]
        plt.plot([posA[0], posB[0]], [posA[1], posB[1]], "--", c=[0.4, 0.4, 0.8])
    # plot the line segment that merge the hole
    plt.plot(
        [verts[mergeLineSeg[0]][0], verts[mergeLineSeg[1]][0]],
        [verts[mergeLineSeg[0]][1], verts[mergeLineSeg[1]][1]],
        "--", c=[0.4, 0.4, 0.8]
    )
    plt.title("Convexify with holes")
    plt.show()
