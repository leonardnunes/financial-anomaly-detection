"""Regression tests for mathematical invariance properties."""

import unittest
from decimal import Decimal

from financial_anomaly_detection.detector import analyze_amounts


class MathematicalInvarianceTests(unittest.TestCase):

    def setUp(self):
        self.values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ]

    def test_positive_scaling(self):
        factor = Decimal("100")

        original = analyze_amounts(self.values)
        scaled = analyze_amounts(
            [value * factor for value in self.values]
        )

        self.assertEqual(original.status, "success")
        self.assertEqual(scaled.status, "success")
        self.assertEqual(
            scaled.median,
            original.median * factor,
        )
        self.assertEqual(
            scaled.mad,
            original.mad * factor,
        )
        self.assertEqual(
            scaled.threshold,
            original.threshold * factor,
        )
        self.assertEqual(
            [item.index for item in scaled.anomalies],
            [item.index for item in original.anomalies],
        )
        self.assertEqual(
            [item.index for item in scaled.anomalies],
            [4],
        )

    def test_positive_translation(self):
        offset = Decimal("1000")

        original = analyze_amounts(self.values)
        shifted = analyze_amounts(
            [value + offset for value in self.values]
        )

        self.assertEqual(original.status, "success")
        self.assertEqual(shifted.status, "success")
        self.assertEqual(
            shifted.median,
            original.median + offset,
        )
        self.assertEqual(
            shifted.mad,
            original.mad,
        )
        self.assertEqual(
            shifted.threshold,
            original.threshold + offset,
        )
        self.assertEqual(
            [item.index for item in shifted.anomalies],
            [item.index for item in original.anomalies],
        )
        self.assertEqual(
            [item.index for item in shifted.anomalies],
            [4],
        )


if __name__ == "__main__":
    unittest.main()
