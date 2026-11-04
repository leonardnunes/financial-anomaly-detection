"""Reproducible repeated evaluation on synthetic financial data."""

from collections import Counter
from decimal import Decimal
from random import Random

from financial_anomaly_detection.detector import analyze_amounts


TRIALS = 100
BASELINE_SIZE = 50
SEED = 20261103


def generate_sample(scenario, rng):
    if scenario == "normal_with_anomalies":
        records = [
            (Decimal(f"{max(1.0, rng.gauss(110, 15)):.2f}"), False)
            for _ in range(BASELINE_SIZE)
        ]
        records.extend([
            (Decimal("500"), True),
            (Decimal("600"), True),
        ])

    elif scenario == "skewed_without_anomalies":
        records = [
            (Decimal(f"{rng.lognormvariate(4.7, 0.85):.2f}"), False)
            for _ in range(BASELINE_SIZE)
        ]

    elif scenario == "zero_mad_with_anomaly":
        records = [
            (Decimal("100"), False)
            for _ in range(BASELINE_SIZE)
        ]
        records.append((Decimal("500"), True))

    else:
        raise ValueError(f"Unknown scenario: {scenario}")

    rng.shuffle(records)

    amounts = [amount for amount, _ in records]
    labels = {
        index
        for index, (_, is_anomaly) in enumerate(records)
        if is_anomaly
    }

    return amounts, labels


def evaluate(scenario, seed):
    rng = Random(seed)
    totals = Counter()
    statuses = Counter()

    for _ in range(TRIALS):
        amounts, labels = generate_sample(scenario, rng)
        result = analyze_amounts(amounts)

        predicted = {item.index for item in result.anomalies}
        review = {item.index for item in result.review_candidates}

        totals["tp"] += len(predicted & labels)
        totals["fp"] += len(predicted - labels)
        totals["fn"] += len(labels - predicted)
        totals["tn"] += len(amounts) - len(predicted | labels)

        totals["review_candidates"] += len(review)
        totals["labeled_anomalies_in_review"] += len(review & labels)
        statuses[result.status] += 1

    tp = totals["tp"]
    fp = totals["fp"]
    fn = totals["fn"]
    tn = totals["tn"]

    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    fpr = fp / (fp + tn) if fp + tn else None

    def show(value):
        return "undefined" if value is None else f"{value:.3f}"

    print(f"Scenario: {scenario}")
    print(f"Seed: {seed}")
    print(f"Trials: {TRIALS}")
    print(f"Statuses: {dict(statuses)}")
    print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"Precision: {show(precision)}")
    print(f"Recall: {show(recall)}")
    print(f"False positive rate: {show(fpr)}")
    print(f"Review candidates: {totals['review_candidates']}")
    print(
        "Labeled anomalies in review:",
        totals["labeled_anomalies_in_review"],
    )
    print()


def main():
    scenarios = [
        "normal_with_anomalies",
        "skewed_without_anomalies",
        "zero_mad_with_anomaly",
    ]

    for index, scenario in enumerate(scenarios):
        evaluate(scenario, SEED + index)


if __name__ == "__main__":
    main()
