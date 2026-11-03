"""Reproducible examples using synthetic financial amounts."""

from decimal import Decimal

from financial_anomaly_detection.detector import analyze_amounts


def show_result(name, amounts):
    """Print diagnostic information for one synthetic sample."""
    result = analyze_amounts(amounts)

    print(f"\nScenario: {name}")
    print(f"Status: {result.status}")
    print(f"Valid observations: {result.valid_count}/{result.total_count}")
    print(f"Median: {result.median}")
    print(f"MAD: {result.mad}")
    print(f"Threshold: {result.threshold}")

    print("Statistical candidates:")
    for item in result.anomalies:
        print(f"  Index {item.index}: {item.amount}")

    print("Descriptive review candidates:")
    for item in result.review_candidates:
        print(f"  Index {item.index}: {item.amount}")

    print("Input issues:")
    for issue in result.issues:
        print(f"  Index {issue.index}: {issue.code}")


def main():
    show_result(
        "Positive MAD",
        [
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ],
    )

    show_result(
        "Zero MAD with variation",
        [
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("100"),
            Decimal("500"),
        ],
    )

    show_result(
        "Input validation",
        [
            None,
            Decimal("0"),
            Decimal("-10"),
            Decimal("90"),
            Decimal("100"),
            Decimal("110"),
            Decimal("120"),
            Decimal("500"),
        ],
    )


if __name__ == "__main__":
    main()
