import unittest
import numpy as np
from meadow_map.intersect import intersect


class TestBasicOps(unittest.TestCase):

    def test_intersect(self):
        a1 = np.array([0.5, 0.5])
        a2 = np.array([5.0, 5.0])

        b1 = np.array([0.5, 4.0])
        b2 = np.array([5.5, 2.0])

        c1 = np.array([1.0, 0.5])
        c2 = np.array([8.0, 5.0])

        self.assertEqual(intersect(a1, a2, b1, b2), True)
        self.assertEqual(intersect(c1, c2, b1, b2), True)
        self.assertEqual(intersect(c1, c2, a1, a2), False)

    def test_intersect2(self):
        a1 = np.array([0.0, 5.0])
        a2 = np.array([5.0, 5.0])

        b1 = np.array([2.0, 0.0])
        b2 = np.array([2.0, 8.0])

        c1 = np.array([3.0, 6.0])
        c2 = np.array([3.0, 7.0])

        self.assertEqual(intersect(a1, a2, b1, b2), True)
        self.assertEqual(intersect(c1, c2, a1, a2), False)

    def test_intersect3(self):
        a1 = np.array([0.0, 0.0])
        a2 = np.array([3.0, 3.0])

        b1 = np.array([2.0, 2.0])
        b2 = np.array([4.4, 4.4])

        c1 = np.array([4.0, 4.0])
        c2 = np.array([5.0, 7.0])

        d1 = np.array([2.0, 2.0])
        d2 = np.array([3.0, 8.5])

        self.assertEqual(intersect(a1, a2, b1, b2), True)
        self.assertEqual(intersect(c1, c2, a1, a2), False)
        self.assertEqual(intersect(c1, c2, a2, a1), False)
        self.assertEqual(intersect(d1, d2, a2, a1), True)
        self.assertEqual(intersect(a1, a2, d2, d1), True)
