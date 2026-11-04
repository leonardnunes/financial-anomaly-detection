"""Evaluate anomaly detection in right-skewed synthetic samples."""

from collections import Counter
from decimal import Decimal
from random import Random

from compare_methods import METHODS, predictions, metric


SEED = 20261106
TRIALS = 100
BASELINE_SIZE = 50


def main():
    rng = Random(SEED)
    totals = {method: Counter() for method in METHODS}

    for _ in range(TRIALS):
        records = [
            (
                Decimal(f"{rng.lognormvariate(4.7, 0.85):.2f}"),
                False,
            )
            for _ in range(BASELINE_SIZE)
        ]

        records.extend([
            (Decimal("500"), True),
            (Decimal("600"), True),
        ])

        rng.shuffle(records)

        amounts = [amount for amount, _ in records]
        truth = {
            index
            for index, (_, is_anomaly) in enumerate(records)
            if is_anomaly
        }

        results = predictions(amounts)

        for method, predicted in results.items():
            counts = totals[method]
            counts["tp"] += len(predicted & truth)
            counts["fp"] += len(predicted - truth)
            counts["fn"] += len(truth - predicted)
            counts["tn"] += len(amounts) - len(predicted | truth)

    print("Scenario: skewed_with_injected_anomalies")
    print(f"Seed: {SEED}")
    print(f"Trials: {TRIALS}")
    print(f"Baseline observations per trial: {BASELINE_SIZE}")
    print("Injected anomaly values: 500, 600")
    print()

    for method in METHODS:
        counts = totals[method]
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        tn = counts["tn"]

        print(f"Method: {method}")
        print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
        print(f"Precision: {metric(tp, tp + fp)}")
        print(f"Recall: {metric(tp, tp + fn)}")
        print(f"FPR: {metric(fp, fp + tn)}")
        print()


if __name__ == "__main__":
    main()
