import unittest
from statistics import Statistics


class TestStatistics(unittest.TestCase):
    def test_statistics(self):
        self.assertRaises(ValueError, Statistics, "Hello")
        self.assertRaises(TypeError, Statistics, [])
        self.assertRaises(TypeError, Statistics, [1])
        
    def test_mean(self):
        # Test that method calculates mean correctly
        stats = Statistics([1, 2, 3, 4, 5, 6])
        self.assertAlmostEqual(stats.mean(), 3.5)

        stats.data = [3, 4, 6, 6, 8, 9]
        self.assertAlmostEqual(stats.mean(), 6)

    def test_median(self):
        stats = Statistics([1, 2, 3, 3, 3, 4, 5, 6])
        self.assertAlmostEqual(stats.median(), 3)

        stats.data = [1, 2, 3, 4, 4, 4, 5, 6, 7]
        self.assertAlmostEqual(stats.median(), 4)

        stats.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertAlmostEqual(stats.median(), 5.5)

    def test_mode(self):
        stats = Statistics([1, 2, 3, 3, 3, 4, 5, 6])
        self.assertAlmostEqual(stats.mode(), 3)

        stats.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(stats.mode(), "This Data set does not have mode")

        stats.data = [1, 1, 2, 3, 3, 3, 4, 4, 4]
        self.assertEqual(stats.mode(), [3, 4])

    def test_hildebrand_rule(self):
        stats = Statistics([1, 2, 3, 3, 3, 4, 5])
        self.assertEqual(stats.hildebrand_rule(), True)

    def test_variance(self):
        stats = Statistics([1, 2, 3, 4])
        self.assertAlmostEqual(stats.variance(), 1.25)
        self.assertAlmostEqual(stats.variance(sample=True), 1.666666666)

        stats.data = [1, 2, 3, 4, 5, 6]
        self.assertAlmostEqual(stats.variance(), 2.9166667)
        self.assertAlmostEqual(stats.variance(sample=True), 3.5)

    def test_standard_deviation(self):
        stats = Statistics([600, 470, 170, 430, 300])
        self.assertAlmostEqual(stats.standard_deviation(), 147.322774886)

        stats.data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertAlmostEqual(stats.standard_deviation(), 2.5819889)
        self.assertAlmostEqual(stats.standard_deviation(sample=True), 2.7386128)

    def test_coeffiecient_of_variation(self):
        stats = Statistics([10, 10, 10])
        self.assertEqual(stats.coeffiecient_of_variation(), 0)

        stats.data = [90, 100, 110]
        self.assertAlmostEqual(stats.coeffiecient_of_variation(), 0.081649658)

        stats.data = [10, 12, 23, 23, 16, 23, 21, 16]
        self.assertAlmostEqual(stats.coeffiecient_of_variation(sample=True), 0.29095718698)

    def test_chebyshevs_theorem(self):
        self.assertEqual(Statistics.chebyshevs_theorem(2), "75.0%")
        self.assertEqual(Statistics.chebyshevs_theorem(3), "88.89%")
        self.assertEqual(Statistics.chebyshevs_theorem(4), "93.75%")

    def test_five_number_summary(self):
        stats = Statistics([10, 12, 16, 16, 21, 23, 23, 23])
        self.assertEqual(stats.five_number_summary(), [10, 14, 18.5, 23, 23])

    def test_z_score(self):
        stats = Statistics([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(stats.z_score(stats.mean()), 0)

        stats.data = [10, 12, 16, 16, 21, 23, 23, 23]
        self.assertAlmostEqual(stats.z_score(10), -1.6329932)
        
        stats.data = [10, 12, 16, 16, 21, 23, 23, 23]
        self.assertAlmostEqual(stats.z_score(10, sample=True), -1.5275252)
