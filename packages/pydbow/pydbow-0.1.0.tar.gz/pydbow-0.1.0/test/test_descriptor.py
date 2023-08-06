#!/usr/bin/env python3

import unittest
import orb_descriptor
import numpy as np


class TestORB(unittest.TestCase):
    def test_mean(self):
        descriptors = [orb_descriptor.ORB([0, 1, 0, 0, 1]),
                       orb_descriptor.ORB([1, 1, 1, 1, 1]),
                       orb_descriptor.ORB([0, 0, 0, 1, 0]),
                       orb_descriptor.ORB([0, 1, 0, 0, 1])]

        self.assertEqual(
                orb_descriptor.mean_value(descriptors),
                orb_descriptor.ORB([0, 1, 0, 1, 1]))

    def test_distance(self):
        desc1 = orb_descriptor.ORB([0, 1, 0, 0, 1])
        desc2 = orb_descriptor.ORB([1, 1, 1, 1, 1])
        self.assertEqual(desc1.distance(desc2), 3)

    def test_sum(self):
        descriptors = [orb_descriptor.ORB([0, 1, 0, 0, 1]),
                       orb_descriptor.ORB([1, 1, 1, 1, 1]),
                       orb_descriptor.ORB([0, 0, 0, 1, 0]),
                       orb_descriptor.ORB([0, 1, 0, 0, 1])]
        np.allclose(np.sum(descriptors).features,
                    np.array([1, 3, 1, 2, 3]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
