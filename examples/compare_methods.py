"""Compare statistical thresholds on identical synthetic datasets."""

from collections import Counter
from decimal import Decimal
from random import Random
from statistics import quantiles

from evaluate_repeated import (
    BASELINE_SIZE,
    SEED,
    TRIALS,
    generate_sample,
)
from financial_anomaly_detection.detector import analyze_amounts


SCENARIOS = (
    "normal_with_anomalies",
    "skewed_without_anomalies",
    "zero_mad_with_anomaly",
)

METHODS = ("raw_mad", "scaled_mad", "iqr")


def predictions(amounts):
    result = analyze_amounts(amounts)

    raw = {item.index for item in result.anomalies}
    scaled = set()
    iqr_flags = set()

    if result.status == "success":
        scaled_threshold = (
            result.median
            + Decimal("3") * Decimal("1.4826") * result.mad
        )
        scaled = {
            index
            for index, value in enumerate(amounts)
            if value > scaled_threshold
        }

    if len(amounts) >= 3:
        q1, _, q3 = quantiles(
            amounts, n=4, method="inclusive"
        )
        iqr = q3 - q1

        if iqr > 0:
            iqr_threshold = q3 + Decimal("1.5") * iqr
            iqr_flags = {
                index
                for index, value in enumerate(amounts)
                if value > iqr_threshold
            }

    return {
        "raw_mad": raw,
        "scaled_mad": scaled,
        "iqr": iqr_flags,
    }


def metric(numerator, denominator):
    if denominator == 0:
        return "undefined"
    return f"{numerator / denominator:.4f}"


def evaluate_scenario(scenario, seed):
    rng = Random(seed)
    totals = {method: Counter() for method in METHODS}

    for _ in range(TRIALS):
        amounts, truth = generate_sample(scenario, rng)
        results = predictions(amounts)

        for method, predicted in results.items():
            counts = totals[method]
            counts["tp"] += len(predicted & truth)
            counts["fp"] += len(predicted - truth)
            counts["fn"] += len(truth - predicted)
            counts["tn"] += len(amounts) - len(predicted | truth)

    print(f"Scenario: {scenario}")
    print(f"Seed: {seed} | Trials: {TRIALS}")

    for method in METHODS:
        counts = totals[method]
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        tn = counts["tn"]

        print(f"  Method: {method}")
        print(f"    TP={tp} FP={fp} FN={fn} TN={tn}")
        print(f"    Precision: {metric(tp, tp + fp)}")
        print(f"    Recall: {metric(tp, tp + fn)}")
        print(f"    FPR: {metric(fp, fp + tn)}")

    print()


def main():
    print(f"Baseline size: {BASELINE_SIZE}")
    print("Exploratory comparison; thresholds are not calibrated.")
    print()

    for index, scenario in enumerate(SCENARIOS):
        evaluate_scenario(scenario, SEED + index)


if __name__ == "__main__":
    main()
