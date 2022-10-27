import unittest
import numpy as np
from meadow_map.diag import diagonal, diagonalie, in_cone


class TestDiag(unittest.TestCase):

    def test_diagonalie(self):
        verts_poly = np.array(
            [
                [0., 0.], [0., 4.], [2., 4.],
                [1., 3.], [2., 1.], [3., 3.], [4., 1.],
                [1., 0.]
            ][::-1]
        )
        indices_poly = [i for i in range(verts_poly.shape[0])] # CCW

        dias = [0, 2, 4, 6]
        dibs = [2, 4, 6, 2]
        result = []

        for dia, dib in zip(dias, dibs):
            result.append(diagonalie(verts_poly, indices_poly, dia, dib))

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], True)
        self.assertEqual(result[3], False)

    def test_in_cone(self):
        verts_poly = np.array(
            [
                [0., 0.], [0., 4.], [2., 4.],
                [1., 3.], [2., 1.], [3., 3.], [4., 1.],
                [1., 0.]
            ][::-1]
        )
        indices_poly = [i for i in range(verts_poly.shape[0])]  # CCW

        dias = [0, 2, 4, 6]
        dibs = [2, 4, 6, 2]
        result = []

        for dia, dib in zip(dias, dibs):
            result.append(in_cone(verts_poly, indices_poly, dia, dib))

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        self.assertEqual(result[3], True)

    def test_diagonal(self):
        verts_poly = np.array(
            [
                [0., 0.], [0., 4.], [2., 4.],
                [1., 3.], [2., 1.], [3., 3.], [4., 1.],
                [1., 0.]
            ][::-1]
        )
        indices_poly = [i for i in range(verts_poly.shape[0])]  # CCW

        dias = [0, 2, 4, 6]
        dibs = [2, 4, 6, 2]
        result = []

        for dia, dib in zip(dias, dibs):
            result.append(diagonal(verts_poly, indices_poly, dia, dib))

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        self.assertEqual(result[3], False)
