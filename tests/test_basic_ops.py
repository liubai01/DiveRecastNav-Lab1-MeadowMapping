import unittest
import numpy as np
import meadow_map.basic_ops as op


class TestBasicOps(unittest.TestCase):

    def test_left(self):
        a = np.array([0, 0], dtype=np.float64)
        b = np.array([8, 4], dtype=np.float64)
        c = np.array([0, 1], dtype=np.float64)
        d = np.array([4, 1.5], dtype=np.float64)
        e = np.array([8, 4], dtype=np.float64)

        self.assertEqual(op.left(a, b, c), True)
        self.assertEqual(op.left(a, b, d), False)
        self.assertEqual(op.left(a, b, e), False) # on should be False!

    def test_lefton(self):
        a = np.array([0, 0], dtype=np.float64)
        b = np.array([8, 4], dtype=np.float64)
        c = np.array([0, 2], dtype=np.float64)
        d = np.array([4, 1.5], dtype=np.float64)
        e = np.array([8, 4], dtype=np.float64)

        self.assertEqual(op.left_on(a, b, c), True)
        self.assertEqual(op.left_on(a, b, d), False)
        self.assertEqual(op.left_on(a, b, e), True) # on should be True

    def test_collinear(self):
        a = np.array([0, 0], dtype=np.float64)
        b = np.array([8, 4], dtype=np.float64)
        c = np.array([1, 2], dtype=np.float64)
        d = np.array([4, 2], dtype=np.float64)
        e = np.array([2.2, 4.4], dtype=np.float64)

        self.assertEqual(op.collinear(a, b, c), False)
        self.assertEqual(op.collinear(c, b, a), False)
        self.assertEqual(op.collinear(a, b, d), True)
        self.assertEqual(op.collinear(b, a, d), True)
        self.assertEqual(op.collinear(c, a, e), True)

    def test_between(self):
        a = np.array([0, 0], dtype=np.float64)
        b = np.array([8, 4], dtype=np.float64)
        c = np.array([4, 2], dtype=np.float64)
        d = np.array([0, 8], dtype=np.float64)
        e = np.array([0, 4], dtype=np.float64)

        self.assertEqual(op.collinear(a, b, c) and op.between(a, b, c), True)
        self.assertEqual(op.collinear(a, b, c) and op.between(b, a, c), True)
        self.assertEqual(op.collinear(a, b, c) and op.between(a, c, b), False)

        self.assertEqual(op.collinear(a, d, e) and op.between(a, d, e), True)
        self.assertEqual(op.collinear(a, d, e) and op.between(d, a, e), True)
        self.assertEqual(op.collinear(a, d, e) and op.between(a, e, d), False)
