"""Robust, explainable financial anomaly detection."""

from dataclasses import dataclass
from decimal import (
    Context,
    Decimal,
    MAX_EMAX,
    MIN_EMIN,
    ROUND_HALF_EVEN,
    localcontext,
)
from statistics import median
from typing import Iterable, Literal


Status = Literal[
    "insufficient_data",
    "zero_dispersion",
    "zero_mad_with_variation",
    "success",
]

IssueCode = Literal[
    "missing_value",
    "invalid_type",
    "non_finite",
    "zero_amount_review",
    "negative_amount_review",
]


@dataclass(frozen=True)
class Observation:
    index: int
    amount: Decimal


@dataclass(frozen=True)
class InputIssue:
    index: int
    code: IssueCode


@dataclass(frozen=True)
class DetectionResult:
    status: Status
    total_count: int
    valid_count: int
    median: Decimal | None
    mad: Decimal | None
    threshold: Decimal | None
    anomalies: tuple[Observation, ...]
    review_candidates: tuple[Observation, ...]
    issues: tuple[InputIssue, ...]


def _working_precision(values: list[Decimal]) -> int:
    """Calculate precision with headroom for intermediate operations."""
    highest_position = max(
        value.adjusted() for value in values
    )
    lowest_position = min(
        value.as_tuple().exponent for value in values
    )

    return max(
        28,
        highest_position - lowest_position + 6,
    )


def _calculation_context(values: list[Decimal]) -> Context:
    """Create an independent decimal arithmetic context."""
    return Context(
        prec=_working_precision(values),
        rounding=ROUND_HALF_EVEN,
        Emin=MIN_EMIN,
        Emax=MAX_EMAX,
        clamp=0,
    )


def analyze_amounts(amounts: Iterable[object]) -> DetectionResult:
    """Analyze positive, finite Decimal amounts.

    Invalid or non-positive observations are excluded from
    statistical calculations and recorded as input issues.
    Original observation positions are preserved.
    """
    accepted: list[Observation] = []
    issues: list[InputIssue] = []
    total_count = 0

    for index, value in enumerate(amounts):
        total_count += 1

        if value is None:
            issues.append(InputIssue(index, "missing_value"))
        elif not isinstance(value, Decimal):
            issues.append(InputIssue(index, "invalid_type"))
        elif not value.is_finite():
            issues.append(InputIssue(index, "non_finite"))
        elif value == 0:
            issues.append(InputIssue(index, "zero_amount_review"))
        elif value < 0:
            issues.append(InputIssue(index, "negative_amount_review"))
        else:
            accepted.append(Observation(index, value))

    valid_count = len(accepted)
    recorded_issues = tuple(issues)

    if valid_count < 3:
        return DetectionResult(
            status="insufficient_data",
            total_count=total_count,
            valid_count=valid_count,
            median=None,
            mad=None,
            threshold=None,
            anomalies=(),
            review_candidates=(),
            issues=recorded_issues,
        )

    values = [observation.amount for observation in accepted]

    with localcontext(_calculation_context(values)):
        center = median(values)
        dispersion = median(
            abs(value - center) for value in values
        )

        if dispersion == 0:
            if all(value == center for value in values):
                status: Status = "zero_dispersion"
                review_candidates: tuple[Observation, ...] = ()
            else:
                status = "zero_mad_with_variation"
                review_candidates = tuple(
                    observation
                    for observation in accepted
                    if observation.amount > center
                )

            return DetectionResult(
                status=status,
                total_count=total_count,
                valid_count=valid_count,
                median=center,
                mad=dispersion,
                threshold=None,
                anomalies=(),
                review_candidates=review_candidates,
                issues=recorded_issues,
            )

        threshold = center + Decimal("3") * dispersion

        anomalies = tuple(
            observation
            for observation in accepted
            if observation.amount > threshold
        )

        return DetectionResult(
            status="success",
            total_count=total_count,
            valid_count=valid_count,
            median=center,
            mad=dispersion,
            threshold=threshold,
            anomalies=anomalies,
            review_candidates=(),
            issues=recorded_issues,
        )
