"""Regression tests for Decimal context isolation."""

import unittest
from decimal import (
    Decimal,
    Inexact,
    Rounded,
    ROUND_DOWN,
    localcontext,
)

from financial_anomaly_detection.detector import analyze_amounts


class DecimalContextIsolationTests(unittest.TestCase):

    def test_external_context_is_preserved(self):
        values = [
            Decimal("1000000.01"),
            Decimal("1000000.02"),
            Decimal("1000000.03"),
            Decimal("1000000.04"),
        ]

        with localcontext() as context:
            context.prec = 6
            context.Emax = 5
            context.Emin = -5
            context.rounding = ROUND_DOWN
            context.traps[Inexact] = True
            context.traps[Rounded] = True

            result = analyze_amounts(values)

            self.assertEqual(context.prec, 6)
            self.assertEqual(context.Emax, 5)
            self.assertEqual(context.Emin, -5)
            self.assertEqual(context.rounding, ROUND_DOWN)
            self.assertTrue(context.traps[Inexact])
            self.assertTrue(context.traps[Rounded])

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
