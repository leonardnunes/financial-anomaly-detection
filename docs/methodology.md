# Statistical Methodology

## Project
Financial Anomaly Detection

## Objective
Identify unusually high financial expenses using robust statistics and reproducible synthetic datasets.

## Mathematical Definitions

Let X = {x_1, ..., x_n} represent a sample of expenses.

Median:
m = median(X)

Median Absolute Deviation:
MAD = median(|x_i - m|)

Initial reference threshold:
T = m + 3 * MAD

Candidate anomaly:
x_i > T

## Important Distinction

The initial threshold is a heuristic, not a statistically calibrated significance test.

Raw MAD and scaled MAD are different quantities.

## Pending Methodological Decisions

- Handling of MAD equal to zero
- Minimum acceptable sample size
- Treatment of repeated values
- Treatment of missing and invalid observations
- Behavior under skewed distributions
- Comparison with reference statistical methods
- Evaluation using labeled synthetic anomalies

## Validation Status

Mathematical implementation: pending
Automated tests: pending
Experimental evaluation: pending

## Small-Sample Limitations

For a sample containing exactly two observations a <= b:

median = (a + b) / 2
MAD = (b - a) / 2

Under the initial threshold rule:

T = median + 3 * MAD
T = 2*b - a

Because T >= b, neither observation can exceed the threshold.

This demonstrates a mathematical limitation of the initial detector for samples of size two.

Observed synthetic examples:

Sample [100, 500]:
Median = 300
MAD = 200
Threshold = 900
Detected anomalies = none

Sample [100, 110, 500]:
Median = 110
MAD = 10
Threshold = 140
Detected anomalies = [500]

A sample size of three does not guarantee reliable detection.

Minimum sample-size policy: pending experimental validation.

No universal statistical minimum is assumed.

Additional validation must consider sample size, contamination, distribution shape, and detection stability.

## Contamination Sensitivity

A controlled exploratory experiment used 20 synthetic expenses.

Ordinary expenses were generated from repeated values:
90, 100, 110, 120, 130.

Extraordinary expenses were assigned a value of 500.

Detection rule:
T = median + 3 * raw MAD

Observed results:

45% contamination:
Median = 130
MAD = 40
Threshold = 250
Detected = 9 of 9

50% contamination:
Median = 315
MAD = 185
Threshold = 870
Detected = 0 of 10

55% contamination:
Median = 500
MAD = 0
Threshold = 500
Detected = 0 of 11

## Interpretation

The detector failed to identify the inserted extraordinary expenses at contamination levels of 50% and 55%.

At 50%, the threshold exceeded all observed expenses.

At 55%, the median equaled the extraordinary expense value and MAD became zero.

These results are specific to the constructed synthetic samples.

They do not establish a universal contamination tolerance or a general detection-performance guarantee.

The breakdown properties of robust estimators must not be confused with the detection performance of a threshold-based anomaly classifier.

Further experiments must evaluate alternative distributions, sample sizes, contamination patterns, and threshold policies.

Experimental conclusions remain provisional.

## Comparison of Statistical Detection Methods

Dataset:
21 synthetic financial expenses with right-skewed values.

Sample median = 128
Raw MAD = 23

### Method 1: Raw MAD

Threshold = median + 3 * raw MAD
Threshold = 197

Candidate anomalies:
225, 280, 370, 500

### Method 2: Scaled MAD

Scaling factor = 1.4826

Threshold = median + 3 * 1.4826 * raw MAD
Threshold = 230.2994

Candidate anomalies:
280, 370, 500

The scaling factor is motivated by consistency with the standard deviation under a normal distribution.

It does not guarantee superior anomaly detection performance under skewed distributions.

### Method 3: Interquartile Range

Quartile calculation: inclusive method

Q1 = 115
Q3 = 170
IQR = 55

Threshold = Q3 + 1.5 * IQR
Threshold = 252.5

Candidate anomalies:
280, 370, 500

### Experimental Interpretation

All three methods identified expenses of 280, 370, and 500.

Only the raw MAD method identified the expense of 225.

This disagreement does not establish which method is more accurate.

The dataset has no ground-truth anomaly labels.

Therefore, true positives, false positives, precision, recall, and F1-score cannot yet be established.

The detection thresholds use different heuristic conventions and are not calibrated to equivalent false-positive rates.

Further experiments with labeled synthetic datasets and different distribution shapes are required.

No method has been selected as universally superior.


## Monetary Precision Policy

Financial values must preserve their intended decimal precision.

Accepted internal representations under evaluation:
- Python Decimal
- Integer minor currency units (cents)

Statistical calculations:
- Preserve fractional cents when mathematically necessary.
- Do not round medians, MAD values, or thresholds prematurely.
- Apply anomaly comparisons using unrounded thresholds.
- Use a strict greater-than comparison for upper-tail detection.

Example:
Median = 10001.5 cents
MAD = 1.0 cent
Threshold = 10004.5 cents
Threshold in BRL = 100.045

Rounding policy:
- Rounding for display must be separated from statistical calculations.
- The rounding mode must be explicitly documented.
- Display formatting must not change anomaly classifications.

Scientific library compatibility:
- Float conversions must be explicit.
- Potential numerical precision loss must be evaluated.
- Monetary source values must remain available without unintended conversion.

Final numeric representation: pending implementation validation.

## Financial Input Validation Policy

This policy defines the preliminary input contract.

### Statistical Input

The anomaly detector will operate on finite,
strictly positive Decimal expense amounts.

Input normalization and statistical detection
must remain separate responsibilities.

### Validation Categories

missing_value:
- None or an explicitly missing amount.

invalid_type:
- Unsupported types, including boolean values.
- Text values require explicit upstream parsing.

non_finite:
- Decimal NaN or Infinity.

zero_amount_review:
- Zero-valued financial records.

negative_amount_review:
- Negative financial records requiring
  contextual interpretation.

valid_positive_expense:
- Finite Decimal values greater than zero.

### Processing Rules

- Never silently discard financial records.
- Preserve the original financial dataset.
- Record validation failures and their reasons.
- Track accepted, rejected, and review-required records.
- Exclude unresolved records from the positive-expense
  statistical baseline.
- Do not automatically reinterpret negative amounts
  as expenses, refunds, or reversals.
- Perform explicit conversion before statistical analysis.
- Do not calculate thresholds using non-finite values.

### Pending Decisions

- Exception types and error reporting format.
- Batch rejection versus partial acceptance.
- Minimum number of valid observations.
- Treatment of empty and degenerate samples.
- Final public API for validation results.

Implementation and automated validation tests: pending.

## Empty and Invalid Samples

### Empty Input

When the input dataset contains zero observations:

Status = insufficient_data

Median = not calculated
MAD = not calculated
Threshold = not calculated

### No Valid Expenses

When records exist but none satisfy the
positive-expense validation requirements:

Status = insufficient_data

The detector must not calculate statistics
using an empty collection of valid expenses.

### Important Distinction

insufficient_data:
The statistical analysis could not be performed.

success with zero anomalies:
The analysis was performed and no observations
exceeded the defined detection threshold.

These outcomes must never be treated as equivalent.

### Audit Requirements

- Preserve original records.
- Count received and accepted observations.
- Report rejected and review-required records.
- Record individual validation reasons.
- Do not silently discard invalid observations.
- Do not replace missing statistics with zero.

### Pending Decisions

- Structured result and error-reporting format.
- Minimum number of valid observations.
- Behavior for one valid observation.
- Final handling of MAD equal to zero.

Implementation and automated tests remain pending.

## Single-Observation Samples

A sample with one valid expense permits mathematical
calculation of the median and raw MAD.

Example:
X = [150.00]

Median = 150.00
MAD = 0.00
Threshold = 150.00
Detected candidates = none

However, a single observation does not establish
a historical reference for anomaly detection.

### Preliminary Policy

Samples with zero or one valid observation
must return:

Status = insufficient_data

No operational anomaly classification
should be produced.

A mathematical result must not be confused
with a statistically reliable assessment.

This preliminary policy does not establish
that two or more observations are sufficient.

The definitive minimum sample size remains
subject to experimental validation.

Automated tests: pending.

## Zero MAD Diagnostic Cases

A zero MAD does not necessarily imply that all
observations are identical.

### Case 1: Zero Dispersion

Sample:
[100, 100, 100, 100, 100]

Unique values = 1
Median = 100
MAD = 0

Diagnostic category:
zero_dispersion

All observed amounts are identical.

### Case 2: Zero MAD with Variation

Sample:
[100, 100, 100, 100, 500]

Unique values = 2
Median = 100
MAD = 0

Diagnostic category:
zero_mad_with_variation

The sample contains variation, but the raw MAD
cannot capture a positive dispersion scale.

The initial threshold flags 500 as a candidate.

This does not establish whether 500 is a
genuine financial anomaly.

### Preliminary Design Requirements

- Distinguish zero dispersion from zero MAD
  with non-identical observations.
- Do not automatically interpret MAD = 0
  as absence of anomalies.
- Do not introduce arbitrary fallback
  thresholds without explicit justification.
- Preserve diagnostic information in results.
- Evaluate fallback policies experimentally.

Final threshold policy: pending.
Automated tests: pending.

## Limitations of the Three-Times-Median Fallback

The fallback threshold T = 3 * median was evaluated
using synthetic samples with raw MAD equal to zero.

### Scenario A: Small Variation

Sample = [100, 100, 100, 100, 101]
Median = 100
MAD = 0
Fallback threshold = 300
Detected candidates = none

### Scenario B: Large Variation

Sample = [100, 100, 100, 100, 250]
Median = 100
MAD = 0
Fallback threshold = 300
Detected candidates = none

The additional expense is 150% above the median,
but the fallback does not flag it.

### Scenario C: Small Monetary Values

Sample = [0.01, 0.01, 0.01, 0.01, 0.04]
Median = 0.01
MAD = 0
Fallback threshold = 0.03
Detected candidates = [0.04]

The absolute difference from the median is 0.03.

### Interpretation

The fallback depends on relative magnitude rather
than financial materiality.

A mathematically unusual amount is not necessarily
a financially significant anomaly.

The strict comparison x > T excludes values
exactly equal to the threshold.

The multiplier of three is a heuristic and
requires empirical justification.

### Methodological Status

The three-times-median fallback remains an
experimental reference method.

No definitive zero-MAD threshold has been selected.

Final policy: pending further evaluation.
Automated tests: pending.

## Absolute and Relative Deviation

Absolute deviation from the median:

D_abs = x - median

Relative deviation, when median > 0:

D_rel = ((x - median) / median) * 100

### Experimental Results

Scenario A:
Median = 100
Candidate = 101
Absolute deviation = 1
Relative deviation = 1%

Scenario B:
Median = 100
Candidate = 250
Absolute deviation = 150
Relative deviation = 150%

Scenario C:
Median = 0.01
Candidate = 0.04
Absolute deviation = 0.03
Relative deviation = 300%

### Interpretation

Relative deviation measures proportional change.

Absolute deviation measures monetary difference.

A large percentage does not necessarily imply
a financially material difference.

Neither measure independently establishes
whether an expense is anomalous.

Relative deviation is undefined when the
reference median equals zero.

### Architectural Considerations

Statistical anomaly detection and financial
materiality assessment should be evaluated
as separate responsibilities.

No minimum monetary or percentage threshold
has been adopted.

Any operational materiality threshold must
have an explicit justification.

Final zero-MAD handling policy: pending.
Automated tests: pending.

## IQR as a Potential Zero-MAD Alternative

Two synthetic samples were evaluated using
the inclusive quartile calculation method.

### Scenario A

Sample = [100, 100, 100, 100, 500]

Median = 100
MAD = 0
Q1 = 100
Q3 = 100
IQR = 0
IQR threshold = 100

Candidate anomalies = [500]

Both MAD and IQR have zero dispersion.

The candidate is flagged because it exceeds
the threshold, not because a positive
dispersion scale was successfully estimated.

### Scenario B

Sample = [100, 100, 100, 200, 500]

Median = 100
MAD = 0
Q1 = 100
Q3 = 200
IQR = 100
IQR threshold = 350

Candidate anomalies = [500]

In this sample, IQR provides a positive
dispersion measure despite MAD being zero.

### Interpretation

IQR may provide additional information
when MAD equals zero.

However, IQR can also equal zero when
distinct observations are present.

Neither method guarantees reliable
anomaly classification in every sample.

### Preliminary Decision

IQR remains a candidate complementary method.

It will not automatically replace MAD
when MAD equals zero.

Further evaluation must include:
- Different sample sizes
- Repeated-value distributions
- Skewed distributions
- Extreme contamination
- Labeled synthetic anomalies

Final fallback policy: pending validation.
Automated tests: pending.

## Quartile Estimation Method Sensitivity

The IQR method was evaluated using two quartile
estimation conventions provided by Python statistics.

Sample = [100, 100, 100, 200, 500]

### Inclusive Method

Q1 = 100
Q3 = 200
IQR = 100
Upper threshold = 350
Candidates = [500]

### Exclusive Method

Q1 = 100
Q3 = 350
IQR = 250
Upper threshold = 725
Candidates = none

### Interpretation

Identical observations can produce different
quartiles and anomaly candidates depending
on the estimation convention.

The experiment does not establish which
convention is statistically superior.

No ground-truth anomaly labels were supplied.

Differences between candidate sets must not
be described as differences in accuracy
without labeled validation data.

### Reproducibility Policy

The inclusive quartile method is selected
as the initial experimental convention.

The convention must be explicitly documented
and consistently applied in experiments.

The suitability of this convention remains
subject to evaluation.

IQR fallback policy: not finalized.
Automated tests: pending.

## Initial Detector Decision Policy

The initial detector prioritizes transparent
diagnostics over unsupported fallback thresholds.

### Insufficient Sample

If fewer than three valid observations are
available, return:

status = insufficient_data

No statistical anomaly candidates are produced.

The minimum sample size is a preliminary
engineering rule, not a guarantee of reliability.

### Zero Dispersion

If MAD = 0 and all observations are identical:

status = zero_dispersion

No statistical anomaly candidates are produced.

### Zero MAD with Variation

If MAD = 0 and distinct values exist:

status = zero_mad_with_variation

No automatic statistical anomaly classification
is performed.

Values above the median may be reported as
descriptive review candidates, clearly separated
from statistically flagged anomalies.

No fallback threshold is applied by default.

### Positive MAD

When the sample is sufficient and MAD > 0:

status = success

Use the experimental raw-MAD threshold:

T = median + 3 * MAD

Flag values strictly greater than T as
statistical anomaly candidates.

These flags do not establish ground-truth
anomalies or financial materiality.

### Additional Requirements

- Preserve the input validation diagnostics.
- Preserve Decimal precision for monetary values.
- Expose median, MAD, threshold and status.
- Represent unavailable thresholds explicitly.
- Keep statistical flags separate from review
  suggestions and financial materiality.
- Keep the IQR method available for experiments,
  without automatic fallback behavior.

This policy is the initial implementation
contract and remains subject to labeled
experimental validation.

Automated implementation tests: pending.

## Decimal Arithmetic and Context Isolation

### Identified Precision Risk

Python Decimal arithmetic depends on the active
decimal context, including precision, exponent
limits, rounding mode, and exception traps.

An initial experiment showed that reducing the
external precision from 28 to 6 changed the
median, MAD, threshold, and anomaly candidates.

A separate experiment demonstrated that setting
the external Emax to 5 caused decimal.Overflow
when processing amounts near 1,000,000.

Both problems were reproduced through regression
tests before the implementation was corrected.

### Implemented Mitigation

The detector now creates an independent decimal
Context for its statistical calculations.

The internal context defines:

- Precision derived from input magnitudes and
  decimal exponents, with additional headroom.
- ROUND_HALF_EVEN rounding.
- Independent minimum and maximum exponent limits.
- Local isolation through localcontext().

The detector does not intentionally modify the
calling application's decimal context.

### Verified Behavior

Automated regression tests cover:

- External precision changes.
- Restricted external maximum exponents.
- External rounding configurations.
- External Inexact and Rounded exception traps.
- Preservation of the external decimal context.

The complete local suite passed 20 tests after
the context isolation changes.

### Remaining Limitations

The precision strategy has not been proven
correct for every possible Decimal magnitude,
exponent, or resource constraint.

Additional boundary and property-based testing
may be required before production deployment.

Passing unit tests does not establish statistical
accuracy, financial materiality, or production
readiness.
