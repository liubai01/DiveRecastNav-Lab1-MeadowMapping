"""
Turn a simple (concave) polygon with holes(obstacles) into convex
polys based on a divide-and-conquer method. The method bases on Arkin,
Ronald C.'s report "Path planning for a vision-based autonomous robot".

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
from .intersect import intersect


__all__ = ["merge_hole"]


def merge_hole(verts_poly: np.ndarray, indices_poly: np.ndarray,
               verts_hole: np.ndarray, indices_hole: np.ndarray
               ) -> (np.ndarray, np.ndarray, (int,)):
    """
    Merge hole into polygon. Connect arbitrary vertex on hole to some vertex in polygon in sight.

    This method refer to Recast Navigation's implementation.

    Remark: `indices_poly` should be in counter-clock wise.
    Remark: `indices_hole` should be in counter-clock wise.
    :param verts_poly:     np.ndarray (#verts, 2)
                           a list of 2D-vertices position of simple polygon

    :param indices_poly:   np.ndarray (#vert, )
                           a list of polygon vertex index (to array `verts`)
                           of simple polygon

    :param verts_hole:     np.ndarray (#verts, 2)
                           a list of 2D-vertices position of hole

    :param indices_hole:   np.ndarray (#verts, 2)
                           a list of polygon vertex index (to array `verts`) of hole

    :return: (verts_out: np.ndarray (#verts, 2), indices_out: np.ndarray (#vert, ), diag: (0, 1)):
            (1) output a polygon in (verts_out, indices_out) that merges the hole.
            (2) `diag` is index of edge that merges poly and hole.
    """
    n_poly = len(indices_poly)
    n_poly_verts = verts_poly.shape[0]
    n_hole = len(indices_hole)
    n_hole_verts = verts_hole.shape[0]

    hole_i = indices_hole[0]

    # traverse all vertex in poly to check whether it is in `hole_i`'s line of sight
    for poly_idx, poly_i in enumerate(indices_poly):
        okay = True
        # check whether `hole_i, poly_i` intersects with each poly edge
        for poly_edge in range(n_poly):
            poly_ai = indices_poly[poly_edge]
            poly_bi = indices_poly[(poly_edge + 1) % n_poly]
            # skip check with shared vertex `poly_i`
            if poly_i in (poly_ai, poly_bi):
                continue
            if intersect(
                    verts_poly[poly_i], verts_hole[hole_i], verts_poly[poly_ai], verts_poly[poly_bi]
            ):
                okay = False
                break
        # check whether `hole_i, poly_i` intersects with each hole edge
        if not okay:
            continue
        for hole_edge in range(n_hole):
            hole_ai = indices_hole[hole_edge]
            hole_bi = indices_hole[(hole_edge + 1) % n_hole]
            # skip check with shared vertex `hole_i`
            if hole_i in (hole_ai, hole_bi):
                continue
            if intersect(verts_poly[poly_i], verts_hole[hole_i],
                         verts_hole[hole_ai], verts_hole[hole_bi]):
                okay = False
                break

        if okay:
            verts_out = np.concatenate((verts_poly, verts_hole), axis=0)
            indices_out = [poly_i, hole_i + n_poly_verts]
            # all hole index applied an offset of nPoly

            # add hole verts to out
            now_holei = 1 % n_hole
            while indices_hole[now_holei] != hole_i:
                indices_out.append(indices_hole[now_holei] + n_poly_verts)
                now_holei = (now_holei + 1) % n_hole

            indices_out.append(hole_i + n_poly_verts)
            indices_out.append(poly_i)

            # add poly verts to out
            now_polyi = (poly_idx + 1) % n_poly
            while indices_poly[now_polyi] != poly_i:
                indices_out.append(indices_poly[now_polyi])
                now_polyi = (now_polyi + 1) % n_poly

            return verts_out, indices_out, (hole_i + n_poly_verts, poly_i)

    # Fail fallback: discard the hole
    return verts_poly, indices_poly, None
