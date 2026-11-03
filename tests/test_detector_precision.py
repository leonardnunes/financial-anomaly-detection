"""Regression tests for Decimal context independence."""

import unittest
from decimal import Decimal, localcontext

from financial_anomaly_detection.detector import analyze_amounts


class DecimalPrecisionTests(unittest.TestCase):

    def test_results_are_independent_of_external_precision(self):
        values = [
            Decimal("100000.01"),
            Decimal("100000.02"),
            Decimal("100000.03"),
            Decimal("100000.04"),
        ]

        for precision in (28, 6):
            with self.subTest(precision=precision):
                with localcontext() as context:
                    context.prec = precision
                    result = analyze_amounts(values)

                self.assertEqual(result.status, "success")
                self.assertEqual(
                    result.median,
                    Decimal("100000.025"),
                )
                self.assertEqual(
                    result.mad,
                    Decimal("0.010"),
                )
                self.assertEqual(
                    result.threshold,
                    Decimal("100000.055"),
                )
                self.assertEqual(result.anomalies, ())


if __name__ == "__main__":
    unittest.main()
