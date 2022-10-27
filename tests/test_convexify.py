import unittest
import numpy as np
from meadow_map.convex_no_hole import convexify
from shapely.geometry import Polygon


def is_convex(verts: np.ndarray, indices: np.ndarray) -> int:
    """
    Is polygon convex
    :param verts:      np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:    np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :return:           int                     the index of `indices`
    """
    n = len(indices)
    for ia in range(n):
        ia_prev = ia - 1 if ia - 1 >= 0 else n - 1
        ia_next = ia + 1 if ia + 1 < n else 0

        k1 = verts[indices[ia_prev]]
        k2 = verts[indices[ia]]
        k3 = verts[indices[ia_next]]

        dx1 = k2[0] - k1[0]
        dy1 = k2[1] - k1[1]
        dx2 = k3[0] - k2[0]
        dy2 = k3[1] - k2[1]

        if dx1 * dy2 - dy1 * dx2 < 0:
            return False
    return True


class TestConvexify(unittest.TestCase):

    def test_convexify(self):
        # Sample test
        verts_poly = np.array(
            [
                [0., 0.], [0., 4.], [2., 4.],
                [1., 3.], [2., 1.], [3., 3.], [4., 1.],
                [1., 0.]
            ]
        )

        indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

        polys, diags = convexify(verts_poly, indices_poly)

        # Area of the whole polygon
        area_original = Polygon(verts_poly).area
        # Compute sum of area of split polygons
        area_sum = 0
        for p in polys:
            # Assume find_concave_vertex work here
            self.assertEqual(is_convex(verts_poly, p), True)

            x = []
            y = []

            for i in p:
                x.append(verts_poly[i][0])
                y.append(verts_poly[i][1])

            pgon = Polygon(zip(x, y))
            area_sum += pgon.area

        self.assertAlmostEqual(area_sum, area_original)
