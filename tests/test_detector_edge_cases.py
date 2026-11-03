"""Additional edge-case tests for financial anomaly detection."""

import unittest
from decimal import Decimal

from financial_anomaly_detection.detector import analyze_amounts


class DetectorEdgeCaseTests(unittest.TestCase):

    def test_generator_preserves_original_indices(self):
        values = iter([
            None,
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ])

        result = analyze_amounts(values)

        self.assertEqual(result.total_count, 6)
        self.assertEqual(result.valid_count, 5)
        self.assertEqual(
            [item.index for item in result.anomalies],
            [5],
        )

    def test_invalid_inputs_leave_insufficient_sample(self):
        values = [
            None,
            Decimal("100"),
            Decimal("100"),
            "invalid",
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "insufficient_data")
        self.assertEqual(result.valid_count, 2)
        self.assertEqual(
            [issue.index for issue in result.issues],
            [0, 3],
        )

    def test_multiple_zero_mad_review_candidates(self):
        values = [
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("101"),
            Decimal("500"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "zero_mad_with_variation")
        self.assertEqual(result.anomalies, ())
        self.assertEqual(
            [item.index for item in result.review_candidates],
            [4, 5],
        )

    def test_below_median_is_not_review_candidate(self):
        values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "zero_mad_with_variation")
        self.assertEqual(result.review_candidates, ())

    def test_positive_mad_without_anomalies(self):
        values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("130"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.threshold, Decimal("140"))
        self.assertEqual(result.anomalies, ())

    def test_multiple_anomaly_candidates(self):
        values = [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("130"),
            Decimal("500"),
            Decimal("600"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.status, "success")
        self.assertEqual(
            [item.index for item in result.anomalies],
            [5, 6],
        )

    def test_float_and_boolean_are_rejected(self):
        values = [
            Decimal("90"),
            False,
            100.0,
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.valid_count, 5)
        self.assertEqual(
            [(issue.index, issue.code) for issue in result.issues],
            [
                (1, "invalid_type"),
                (2, "invalid_type"),
            ],
        )
        self.assertEqual(
            [item.index for item in result.anomalies],
            [6],
        )

    def test_small_decimal_amounts(self):
        values = [
            Decimal("0.01"),
            Decimal("0.02"),
            Decimal("0.03"),
            Decimal("0.04"),
            Decimal("0.20"),
        ]

        result = analyze_amounts(values)

        self.assertEqual(result.median, Decimal("0.03"))
        self.assertEqual(result.mad, Decimal("0.01"))
        self.assertEqual(result.threshold, Decimal("0.06"))
        self.assertEqual(
            [item.amount for item in result.anomalies],
            [Decimal("0.20")],
        )


if __name__ == "__main__":
    unittest.main()
