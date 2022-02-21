import unittest
from statistics import Statistics


class TestStatistics(unittest.TestCase):
    def test_mean(self):
        # Test that method calculates mean correctly
        stats = Statistics([1, 2, 3, 4, 5, 6])
        self.assertAlmostEqual(stats.mean(), 3.5)

    def test_median(self):
        stats = Statistics([1, 2, 3, 3, 3, 4, 5, 6])
        self.assertAlmostEqual(stats.median(), 3)

    def test_hildebrand_rule(self):
        stats = Statistics([1, 2, 3, 3, 3, 4, 5])
        self.assertTrue(stats.hildebrand_rule(), True)
