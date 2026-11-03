# Financial Anomaly Detection

A reproducible Python project for exploring financial anomaly detection through robust statistics, explicit input validation, and explainable results.

## Overview

This project identifies unusually high financial amounts using the median and median absolute deviation (MAD).

Its purpose is to demonstrate statistical reasoning, Python software engineering, automated testing, and reproducible experimentation.

This is an experimental data science project, not a production fraud detection system.

## Features

- Robust statistics using the median and raw MAD.
- Decimal arithmetic for financial precision.
- Explicit diagnostic statuses.
- Validation of individual observations.
- Preservation of original observation indices.
- Separation of anomaly flags and review suggestions.
- Automated unit tests.
- No third-party runtime dependencies.

## Statistical Method

For valid positive amounts:

    center = median(values)
    mad = median(abs(x - center) for x in values)
    threshold = center + 3 * mad

When MAD is positive, values strictly greater than the threshold are flagged as statistical anomaly candidates.

The multiplier of three is an experimental heuristic, not a calibrated significance level.

See docs/methodology.md for mathematical assumptions, experiments, and limitations.

## Diagnostic Statuses

| Status | Description |
| --- | --- |
| insufficient_data | Fewer than three valid observations |
| zero_dispersion | All valid observations are identical |
| zero_mad_with_variation | Distinct values exist, but MAD is zero |
| success | Positive MAD and a calculated threshold |

When MAD is zero, the detector does not automatically apply an alternative threshold.

Review suggestions are not equivalent to statistically detected anomalies.

## Requirements

- Python 3.13 or newer
- pip

No external runtime libraries are required.

## Installation

From the project directory, create a virtual environment:

    python -m venv .venv

On Windows, install the package using:

    .\.venv\Scripts\python.exe -m pip install -e .

## Usage

    from decimal import Decimal
    from financial_anomaly_detection.detector import analyze_amounts

    amounts = [
        Decimal("90"),
        Decimal("100"),
        Decimal("110"),
        Decimal("120"),
        Decimal("500"),
    ]

    result = analyze_amounts(amounts)

    print(result.status)
    print(result.median)
    print(result.mad)
    print(result.threshold)

    for observation in result.anomalies:
        print(observation.index, observation.amount)

Expected output:

    success
    110
    10
    140
    4 500

Only positive, finite Decimal observations contribute to the statistics.

Invalid, missing, zero, negative, and non-finite values are recorded as input issues.

## Reproducible Demonstration

A runnable example with synthetic financial data
is available at examples/basic_usage.py.

After installing the package, run:

    .\.venv\Scripts\python.exe -B .\examples\basic_usage.py

The demonstration covers three scenarios:

- Positive MAD with a statistical anomaly candidate.
- Zero MAD with a descriptive review candidate.
- Input validation with preserved observation indices.

The example uses no confidential financial data.

## Automated Tests

Run all tests from the repository root:

    python -m unittest discover -s tests -p "test_*.py" -v

The current suite contains 25 tests, all passing in the local development environment.

The tests cover basic calculations, monetary precision, input validation, insufficient samples, zero-MAD cases, generators, and multiple candidates.

## Project Structure

    financial-anomaly-detection/
      docs/
        methodology.md
      src/
        financial_anomaly_detection/
          __init__.py
          detector.py
      examples/
        basic_usage.py
      tests/
        test_detector.py
        test_detector_edge_cases.py
        test_detector_precision.py
        test_detector_exponent.py
        test_detector_context_isolation.py
        test_detector_invariance.py
        test_detector_numeric_boundaries.py
      .gitignore
      pyproject.toml
      README.md

## Known Limitations

- The threshold is heuristic and not calibrated against labeled financial data.
- Flagged values are not necessarily fraud or financial errors.
- Financial materiality is not assessed.
- Only unusually high amounts are considered.
- Temporal dependencies, categories, and seasonality are not modeled.
- Results depend on sample composition and distribution.
- Zero-MAD samples are not automatically classified.
- Precision, recall, and false-positive rates have not been established.
- Passing unit tests does not establish production readiness.

## Development Principles

The project emphasizes transparency, reproducibility, mathematical rigor, and safe handling of financial information.

Experiments should use synthetic or appropriately authorized datasets.

## Current Status

Initial detector implemented.

25 automated tests passed locally.

Additional statistical validation and publication checks are pending.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
