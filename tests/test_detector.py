"""Automated tests for the financial anomaly detector."""

import unittest
from decimal import Decimal

from financial_anomaly_detection.detector import analyze_amounts


class DetectorTests(unittest.TestCase):

    def test_positive_mad_detects_candidate(self):
        values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.median, Decimal("110"))
        self.assertEqual(result.mad, Decimal("10"))
        self.assertEqual(result.threshold, Decimal("140"))
        self.assertEqual(
            [(item.index, item.amount) for item in result.anomalies],
            [(4, Decimal("500"))],
        )

    def test_threshold_uses_strict_comparison(self):
        values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("140"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.threshold, Decimal("140"))
        self.assertEqual(result.anomalies, ())

    def test_insufficient_samples(self):
        for size in (0, 1, 2):
            with self.subTest(size=size):
                values = [Decimal("100")] * size
                result = analyze_amounts(values)

                self.assertEqual(result.status, "insufficient_data")
                self.assertIsNone(result.median)
                self.assertIsNone(result.mad)
                self.assertIsNone(result.threshold)
                self.assertEqual(result.anomalies, ())

    def test_zero_dispersion(self):
        values = [Decimal("100")] * 5

        result = analyze_amounts(values)

        self.assertEqual(result.status, "zero_dispersion")
        self.assertEqual(result.mad, Decimal("0"))
        self.assertIsNone(result.threshold)
        self.assertEqual(result.anomalies, ())
        self.assertEqual(result.review_candidates, ())

    def test_zero_mad_with_variation(self):
        values = [
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("500"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "zero_mad_with_variation")
        self.assertEqual(result.mad, Decimal("0"))
        self.assertIsNone(result.threshold)
        self.assertEqual(result.anomalies, ())
        self.assertEqual(
            [(item.index, item.amount) for item in result.review_candidates],
            [(4, Decimal("500"))],
        )

    def test_decimal_precision(self):
        values = [
            Decimal("100.10"),
            Decimal("100.20"),
            Decimal("100.30"),
            Decimal("100.40"),
            Decimal("500.00"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.median, Decimal("100.30"))
        self.assertEqual(result.mad, Decimal("0.10"))
        self.assertEqual(result.threshold, Decimal("100.60"))
        self.assertEqual(
            [item.amount for item in result.anomalies],
            [Decimal("500.00")],
        )

    def test_invalid_inputs_are_recorded(self):
        values = [
            None,
            True,
            "100",
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("0"),
            Decimal("-5"),
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.total_count, 12)
        self.assertEqual(result.valid_count, 5)
        self.assertEqual(
            [(issue.index, issue.code) for issue in result.issues],
            [
                (0, "missing_value"),
                (1, "invalid_type"),
                (2, "invalid_type"),
                (3, "non_finite"),
                (4, "non_finite"),
                (5, "zero_amount_review"),
                (6, "negative_amount_review"),
            ],
        )
        self.assertEqual(result.status, "success")
        self.assertEqual(
            [item.index for item in result.anomalies],
            [11],
        )

    def test_all_invalid_inputs(self):
        result = analyze_amounts([None, "100", Decimal("-1")])

        self.assertEqual(result.status, "insufficient_data")
        self.assertEqual(result.total_count, 3)
        self.assertEqual(result.valid_count, 0)
        self.assertEqual(len(result.issues), 3)

    def test_original_input_is_not_modified(self):
        values = [
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ]
        original = values.copy()

        analyze_amounts(values)

        self.assertEqual(values, original)


if __name__ == "__main__":
    unittest.main()
