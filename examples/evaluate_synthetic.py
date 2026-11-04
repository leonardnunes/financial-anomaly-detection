"""Evaluate the detector on explicitly labeled synthetic scenarios."""

from decimal import Decimal

from financial_anomaly_detection.detector import analyze_amounts


def evaluate(name, amounts, labeled_anomalies):
    """Compare statistical flags against synthetic reference labels."""
    values = [Decimal(str(value)) for value in amounts]
    truth = set(labeled_anomalies)

    result = analyze_amounts(values)

    predicted = {
        observation.index for observation in result.anomalies
    }

    tp = len(predicted & truth)
    fp = len(predicted - truth)
    fn = len(truth - predicted)
    tn = len(values) - tp - fp - fn

    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None

    def display(metric):
        return f"{metric:.3f}" if metric is not None else "undefined"

    print(f"Scenario: {name}")
    print(f"Status: {result.status}")
    print(f"Observations: {len(values)}")
    print(f"Labeled anomalies: {len(truth)}")
    print(f"Flagged anomalies: {len(predicted)}")
    print(f"Review candidates: {len(result.review_candidates)}")
    print(f"TP: {tp} | FP: {fp} | FN: {fn} | TN: {tn}")
    print(f"Precision: {display(precision)}")
    print(f"Recall: {display(recall)}")
    print()


def main():
    baseline = [90, 100, 110, 120, 130] * 4

    evaluate(
        "Injected high-value anomalies",
        baseline + [500, 600],
        {20, 21},
    )

    evaluate(
        "Right-skewed amounts labeled as normal",
        [
            90, 95, 100, 105, 110, 115, 118,
            120, 122, 125, 128, 133, 139, 147,
            157, 170, 190, 225, 280, 370, 500,
        ],
        set(),
    )

    evaluate(
        "Zero MAD with injected anomaly",
        [100, 100, 100, 100, 500],
        {4},
    )


if __name__ == "__main__":
    main()
