"""Independent calibration and holdout evaluation of statistical detectors."""

from collections import Counter
from decimal import Decimal
from math import ceil
from random import Random
from statistics import median, quantiles


CALIBRATION_SEED = 20261107
TEST_SEED = 20261108
CALIBRATION_TRIALS = 200
TEST_TRIALS = 100
BASELINE_SIZE = 50
TARGET_FPR = 0.05

METHODS = ("raw_mad", "scaled_mad", "iqr")


def generate_baseline(rng):
    return [
        Decimal(f"{rng.lognormvariate(4.7, 0.85):.2f}")
        for _ in range(BASELINE_SIZE)
    ]


def calculate_scores(values):
    center = median(values)
    mad = median(abs(value - center) for value in values)

    scores = {method: [None] * len(values) for method in METHODS}

    if mad > 0:
        for index, value in enumerate(values):
            raw_score = (value - center) / mad
            scores["raw_mad"][index] = raw_score
            scores["scaled_mad"][index] = (
                raw_score / Decimal("1.4826")
            )

    q1, _, q3 = quantiles(
        values,
        n=4,
        method="inclusive",
    )
    iqr = q3 - q1

    if iqr > 0:
        for index, value in enumerate(values):
            scores["iqr"][index] = (value - q3) / iqr

    return scores


def calibrate():
    rng = Random(CALIBRATION_SEED)
    collected = {method: [] for method in METHODS}

    for _ in range(CALIBRATION_TRIALS):
        values = generate_baseline(rng)
        scores = calculate_scores(values)

        for method in METHODS:
            collected[method].extend(
                score
                for score in scores[method]
                if score is not None
            )

    thresholds = {}

    for method in METHODS:
        ordered = sorted(collected[method])

        if not ordered:
            raise RuntimeError(
                f"No calibration scores for {method}"
            )

        position = ceil((1 - TARGET_FPR) * len(ordered)) - 1
        thresholds[method] = max(
            Decimal("0"),
            ordered[position],
        )

    return thresholds


def evaluate(thresholds):
    rng = Random(TEST_SEED)

    totals = {
        condition: {
            method: Counter()
            for method in METHODS
        }
        for condition in ("normal_only", "with_injections")
    }

    for _ in range(TEST_TRIALS):
        baseline = generate_baseline(rng)

        datasets = {
            "normal_only": (
                baseline,
                set(),
            ),
            "with_injections": (
                baseline + [Decimal("500"), Decimal("600")],
                {BASELINE_SIZE, BASELINE_SIZE + 1},
            ),
        }

        for condition, (values, truth) in datasets.items():
            scores = calculate_scores(values)

            for method in METHODS:
                predicted = {
                    index
                    for index, score in enumerate(scores[method])
                    if score is not None
                    and score > thresholds[method]
                }

                counts = totals[condition][method]
                counts["tp"] += len(predicted & truth)
                counts["fp"] += len(predicted - truth)
                counts["fn"] += len(truth - predicted)
                counts["tn"] += len(values) - len(predicted | truth)

    return totals


def display_ratio(numerator, denominator):
    if denominator == 0:
        return "undefined"
    return f"{numerator / denominator:.4f}"


def main():
    thresholds = calibrate()

    print("INDEPENDENT CALIBRATION")
    print(f"Calibration seed: {CALIBRATION_SEED}")
    print(f"Calibration trials: {CALIBRATION_TRIALS}")
    print(f"Target FPR: {TARGET_FPR:.2%}")
    print()

    for method in METHODS:
        print(f"{method} calibrated cutoff: {thresholds[method]:.6f}")

    print()
    print("HELD-OUT EVALUATION")
    print(f"Test seed: {TEST_SEED}")
    print(f"Test trials: {TEST_TRIALS}")

    totals = evaluate(thresholds)

    for condition, methods in totals.items():
        print()
        print(f"Condition: {condition}")

        for method, counts in methods.items():
            tp = counts["tp"]
            fp = counts["fp"]
            fn = counts["fn"]
            tn = counts["tn"]

            print(f"  Method: {method}")
            print(f"    TP={tp} FP={fp} FN={fn} TN={tn}")
            print(
                "    Precision:",
                display_ratio(tp, tp + fp),
            )
            print(
                "    Recall:",
                display_ratio(tp, tp + fn),
            )
            print(
                "    FPR:",
                display_ratio(fp, fp + tn),
            )

    print()
    print("HOLDOUT EVALUATION COMPLETED")


if __name__ == "__main__":
    main()
