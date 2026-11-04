# Synthetic Anomaly Detection Evaluation

## Objective

Evaluate the initial financial anomaly detector on
small, explicitly labeled synthetic scenarios.

This evaluation investigates statistical behavior
and known limitations. It does not estimate
performance on real financial transactions.

## Experimental Setup

Detector: median + 3 * raw MAD

Automatic statistical flags are counted as
positive predictions.

Descriptive review candidates are not counted
as automatic positive predictions.

All observations use synthetic financial amounts.

Reference labels are assigned by experimental
design, not established through independent
financial investigation.

## Scenario 1: Injected High-Value Anomalies

Dataset:
- 20 baseline observations repeating 90, 100,
  110, 120, and 130.
- Two additional observations: 500 and 600.
- Both additional observations labeled anomalous.

Detector status: success

True positives: 2
False positives: 0
False negatives: 0
True negatives: 20

Precision: 1.000
Recall: 1.000

Interpretation:

The detector identified both injected anomalies
in this favorable synthetic scenario.

These results must not be generalized into a
claim of real-world detection accuracy.

## Scenario 2: Right-Skewed Normal Distribution

Dataset:
21 positive observations with a long upper tail.

All observations were assigned normal labels
for this experimental stress test.

Detector status: success

True positives: 0
False positives: 4
False negatives: 0
True negatives: 17

Precision: 0.000
Recall: undefined

Interpretation:

Four observations were flagged despite being
labeled normal by the experimental design.

This illustrates sensitivity to legitimate
high-value observations in skewed samples.

The assigned normal labels are experimental
assumptions, not independently verified
financial ground truth.

Recall is undefined because the dataset
contains no labeled positive observations.

## Scenario 3: Zero MAD With Injected Anomaly

Dataset:
[100, 100, 100, 100, 500]

The observation at index 4 is labeled anomalous.

Detector status: zero_mad_with_variation

True positives: 0
False positives: 0
False negatives: 1
True negatives: 4

Precision: undefined
Recall: 0.000

One descriptive review candidate was returned.

Interpretation:

The conservative zero-MAD policy produced
no automatic statistical anomaly flag.

The injected anomaly was retained as a
descriptive review candidate.

Review recommendations are excluded from
automatic detection metrics.

Precision is undefined because the detector
made no positive predictions.

## Limitations

- Only three small synthetic scenarios were tested.
- Experimental labels are defined by construction.
- No independent financial ground truth exists.
- No real financial dataset was evaluated.
- No confidence intervals were calculated.
- Performance across repeated random samples
  has not been investigated.
- Threshold calibration remains incomplete.
- Financial materiality is not modeled.

## Preliminary Findings

The detector can identify clear injected
high-value observations in favorable samples.

It may flag values from skewed distributions
even when the experimental labels are normal.

Its conservative zero-MAD policy avoids
unsupported automatic classifications, but
can miss labeled anomalies in binary evaluation.

These findings motivate additional experiments
rather than an immediate claim of model accuracy.

## Reproducibility

Experiment script: examples/evaluate_synthetic.py

All amounts and reference labels are explicitly
defined in that script.

Results reported here correspond to the initial
local execution of the experiment.

## Repeated Synthetic Evaluation

### Experimental Design

A reproducible experiment was performed using
100 trials for each of three synthetic scenarios.

Total trials: 300

Random seeds:
- Normal with anomalies: 20261103
- Skewed without anomalies: 20261104
- Zero MAD with anomaly: 20261105

Experiment script: examples/evaluate_repeated.py

Metrics were aggregated across observations
within each scenario.

These are synthetic experimental labels,
not independently established financial truth.

### Scenario 1: Approximately Normal With Anomalies

Baseline observations per trial: 50
Injected anomalies per trial: 2
Injected values: 500 and 600

Trials: 100
Status success: 100

True positives: 200
False positives: 106
False negatives: 0
True negatives: 4894

Precision: 0.654
Recall: 1.000
False positive rate: 0.0212

All injected anomalies were detected, but
106 normal observations were also flagged.

### Scenario 2: Right-Skewed Without Labeled Anomalies

Observations per trial: 50
Distribution: lognormal
Parameters: mu = 4.7, sigma = 0.85

Trials: 100
Status success: 100

True positives: 0
False positives: 662
False negatives: 0
True negatives: 4338

Precision: 0.000
Recall: undefined
False positive rate: 0.1324

The detector flagged 13.24% of observations
labeled normal by experimental design.

These labels represent modeling assumptions,
not verified real-world financial behavior.

### Scenario 3: Zero MAD With Injected Anomaly

Normal observations per trial: 50
Injected anomaly per trial: 1
Injected value: 500

Trials: 100
Status zero_mad_with_variation: 100

True positives: 0
False positives: 0
False negatives: 100
True negatives: 5000

Precision: undefined
Recall: 0.000
False positive rate: 0.000

Review candidates: 100
Labeled anomalies in review: 100

The conservative zero-MAD policy prevented
automatic flags but retained every injected
anomaly as a descriptive review candidate.

### Interpretation

The raw-MAD heuristic performed favorably
for the injected high-value anomalies.

It produced substantially more false positives
in the right-skewed synthetic scenario.

The zero-MAD policy separates review
recommendations from automatic detections.

A low false positive rate alone does not
establish effective anomaly detection.

### Limitations and Next Steps

- Results are limited to synthetic distributions.
- No real financial transactions were used.
- No independent ground-truth labels exist.
- No confidence intervals were calculated.
- No held-out threshold calibration was performed.
- Real-world precision and recall remain unknown.
- Alternative detection rules require comparison
  under the same experimental conditions.
- Model selection should avoid tuning directly
  to the evaluation scenarios.

These results describe the current experimental
baseline and do not establish production readiness.

## Method Comparison Under Skewed Contamination

### Experimental Design

Scenario: skewed_with_injected_anomalies

Random seed: 20261106
Trials: 100
Baseline observations per trial: 50
Injected observations per trial: 2
Injected values: 500 and 600

The baseline follows a lognormal distribution
with mu = 4.7 and sigma = 0.85.

Methods compared:
- Raw MAD: median + 3 * MAD
- Scaled MAD: median + 3 * 1.4826 * MAD
- Inclusive IQR: Q3 + 1.5 * IQR

All methods were evaluated on identical
synthetic observations and reference labels.

Thresholds were not calibrated to produce
equivalent alert rates.

### Raw MAD

TP = 200
FP = 600
FN = 0
TN = 4400

Precision = 0.2500
Recall = 1.0000
FPR = 0.1200

### Scaled MAD

TP = 193
FP = 367
FN = 7
TN = 4633

Precision = 0.3446
Recall = 0.9650
FPR = 0.0734

### Inclusive IQR

TP = 181
FP = 292
FN = 19
TN = 4708

Precision = 0.3827
Recall = 0.9050
FPR = 0.0584

### Interpretation

Raw MAD achieved the highest recall but
produced the most false positives.

Scaled MAD reduced false positives while
missing seven injected anomalies.

IQR produced the fewest false positives
but missed nineteen injected anomalies.

This illustrates a detection tradeoff,
not proof of universal method superiority.

### Methodological Limitations

Injected values were labeled anomalous by
experimental design.

The lognormal baseline can also generate
large observations that remain labeled normal.

Consequently, labels represent synthetic
assumptions rather than independently
verified financial anomalies.

Method thresholds were not calibrated on
a separate development dataset.

The evaluated scenarios should not be used
both to optimize a method and to claim
unbiased final performance.

### Next Steps

- Define an independent calibration protocol.
- Compare methods under controlled alert rates.
- Separate calibration and evaluation datasets.
- Preserve zero-MAD diagnostic behavior.
- Avoid claims of real-world accuracy.

No change to the production-facing detector
interface has been authorized or implemented.

## Independent Calibration and Holdout Evaluation

### Experimental Design

Calibration trials: 200
Calibration seed: 20261107

Holdout trials: 100
Holdout seed: 20261108

Baseline observations per trial: 50

Synthetic baseline:
Lognormal distribution, mu = 4.7, sigma = 0.85.

Experimental target false positive rate: 5%.

Calibration and holdout datasets were generated
using separate random seeds.

Calibration scores were calculated using each
observation within its own sample statistics.

This design is not equivalent to scoring each
observation against an independent historical
reference window.

### Calibrated Score Thresholds

Raw MAD: 5.801509
Scaled MAD: 3.913065
Inclusive IQR: 1.969308

These are experimental score cutoffs rather
than financial transaction amount thresholds.

### Holdout: Normal-Only Condition

Raw MAD:
TP = 0, FP = 251, FN = 0, TN = 4749
Precision = 0.0000
Recall = undefined
FPR = 0.0502

Scaled MAD:
TP = 0, FP = 251, FN = 0, TN = 4749
Precision = 0.0000
Recall = undefined
FPR = 0.0502

Inclusive IQR:
TP = 0, FP = 220, FN = 0, TN = 4780
Precision = 0.0000
Recall = undefined
FPR = 0.0440

### Holdout: Injected-Anomaly Condition

Two observations, 500 and 600, were injected
per trial and labeled anomalous by design.

Raw MAD:
TP = 154, FP = 210, FN = 46, TN = 4790
Precision = 0.4231
Recall = 0.7700
FPR = 0.0420

Scaled MAD:
TP = 154, FP = 210, FN = 46, TN = 4790
Precision = 0.4231
Recall = 0.7700
FPR = 0.0420

Inclusive IQR:
TP = 142, FP = 172, FN = 58, TN = 4828
Precision = 0.4522
Recall = 0.7100
FPR = 0.0344

### Interpretation

Raw and scaled MAD generated identical
predictions after corresponding calibration.

This is consistent with the positive linear
relationship between their anomaly scores.

IQR reduced false positives but missed more
injected anomalies in this evaluation.

Introducing anomalies changes the sample
statistics and can alter normal-observation
false positive rates.

The experimental five-percent target was
approximately achieved in the normal-only
holdout condition.

### Limitations

- Synthetic data and constructed labels only.
- No independent financial ground truth.
- Individual scores use in-sample statistics.
- No uncertainty intervals were calculated.
- No validation under distribution shift.
- No real-world threshold calibration.
- Limited range of synthetic distributions.
- No production performance claims.

### Decision

Retain raw MAD as the initial experimental
implementation.

Keep scaled MAD and IQR as documented
comparison methods.

No method is declared universally superior.

Further evaluation should focus on uncertainty,
distribution shift, and leakage-safe reference
window design before production claims.

Reproducible script: examples/calibrate_holdout.py
