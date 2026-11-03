"""Regression tests for numerical boundary conditions."""

import unittest
from decimal import Decimal, ROUND_DOWN, localcontext

from financial_anomaly_detection.detector import analyze_amounts


class NumericalBoundaryTests(unittest.TestCase):

    def check_scenario(
        self,
        values,
        expected_median,
        expected_mad,
        expected_threshold,
    ):
        with localcontext() as context:
            context.prec = 6
            context.Emax = 5
            context.Emin = -5
            context.rounding = ROUND_DOWN

            result = analyze_amounts(values)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.median, expected_median)
        self.assertEqual(result.mad, expected_mad)
        self.assertEqual(result.threshold, expected_threshold)
        self.assertEqual(
            [item.index for item in result.anomalies],
            [4],
        )

    def test_large_monetary_values(self):
        values = [
            Decimal("1000000000000000000.01"),
            Decimal("1000000000000000000.02"),
            Decimal("1000000000000000000.03"),
            Decimal("1000000000000000000.04"),
            Decimal("1000000000000000000.20"),
        ]

        self.check_scenario(
            values,
            Decimal("1000000000000000000.03"),
            Decimal("0.01"),
            Decimal("1000000000000000000.06"),
        )

    def test_very_small_values(self):
        values = [
            Decimal("1E-26"),
            Decimal("2E-26"),
            Decimal("3E-26"),
            Decimal("4E-26"),
            Decimal("20E-26"),
        ]

        self.check_scenario(
            values,
            Decimal("3E-26"),
            Decimal("1E-26"),
            Decimal("6E-26"),
        )

    def test_mixed_magnitudes(self):
        values = [
            Decimal("0.01"),
            Decimal("0.02"),
            Decimal("0.03"),
            Decimal("0.04"),
            Decimal("1000000000000000000000000.00"),
        ]

        self.check_scenario(
            values,
            Decimal("0.03"),
            Decimal("0.01"),
            Decimal("0.06"),
        )


if __name__ == "__main__":
    unittest.main()
