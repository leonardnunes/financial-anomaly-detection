"""Regression tests for external Decimal exponent limits."""

import unittest
from decimal import Decimal, localcontext

from financial_anomaly_detection.detector import analyze_amounts


class DecimalExponentTests(unittest.TestCase):

    def test_external_emax_does_not_change_results(self):
        values = [
            Decimal("1000000.01"),
            Decimal("1000000.02"),
            Decimal("1000000.03"),
            Decimal("1000000.04"),
        ]

        for maximum_exponent in (999999, 5):
            with self.subTest(emax=maximum_exponent):
                with localcontext() as context:
                    context.prec = 6
                    context.Emax = maximum_exponent

                    result = analyze_amounts(values)

                self.assertEqual(result.status, "success")
                self.assertEqual(
                    result.median,
                    Decimal("1000000.025"),
                )
                self.assertEqual(
                    result.mad,
                    Decimal("0.010"),
                )
                self.assertEqual(
                    result.threshold,
                    Decimal("1000000.055"),
                )
                self.assertEqual(result.anomalies, ())


if __name__ == "__main__":
    unittest.main()
