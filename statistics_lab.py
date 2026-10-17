"""Introductory Statistics 1: National Debt Investigation.

A self-contained practice project covering:
- mean, median, variance, and standard deviation
- grouped data and histogram frequencies
- location, dispersion, and skewness
- linear interpolation
- standard normal probability
- correlation and simple linear regression

The data is illustrative. Replace the lists in main() with real observations.
"""

from __future__ import annotations

import math
from statistics import mean, median, multimode
from typing import Iterable, Sequence


YEAR = list(range(2010, 2025))
DEBT_RATIO = [52, 55, 57, 61, 64, 68, 71, 72, 73, 76, 79, 83, 87, 94, 101]
GROWTH_RATE = [5.2, 4.8, 4.2, 3.9, 3.5, 3.1, 2.8, 2.6, 2.4, 2.0, 1.5, 1.1, 0.8, 0.2, -0.7]


def population_variance(values: Sequence[float]) -> float:
    """Return population variance, sigma squared."""
    average = mean(values)
    return sum((value - average) ** 2 for value in values) / len(values)


def sample_variance(values: Sequence[float]) -> float:
    """Return sample variance, s squared."""
    if len(values) < 2:
        raise ValueError("At least two values are required for sample variance.")
    average = mean(values)
    return sum((value - average) ** 2 for value in values) / (len(values) - 1)


def standard_deviation(values: Sequence[float], sample: bool = False) -> float:
    """Return population or sample standard deviation."""
    variance = sample_variance(values) if sample else population_variance(values)
    return math.sqrt(variance)


def quartiles(values: Sequence[float]) -> tuple[float, float, float]:
    """Return first quartile, median, and third quartile."""
    ordered = sorted(values)
    middle = median(ordered)
    lower = ordered[: len(ordered) // 2]
    upper = ordered[(len(ordered) + 1) // 2 :]
    return median(lower), middle, median(upper)


def pearson_skewness(values: Sequence[float]) -> float:
    """Calculate Pearson's second coefficient of skewness."""
    spread = standard_deviation(values)
    if spread == 0:
        return 0.0
    return 3 * (mean(values) - median(values)) / spread


def grouped_frequency(
    values: Sequence[float], boundaries: Sequence[float]
) -> list[tuple[str, int, float]]:
    """Return interval labels, frequencies, and relative frequencies."""
    if len(boundaries) < 2 or any(a >= b for a, b in zip(boundaries, boundaries[1:])):
        raise ValueError("Boundaries must be in strictly increasing order.")

    rows = []
    total = len(values)
    for index, (lower, upper) in enumerate(zip(boundaries, boundaries[1:])):
        is_last_interval = index == len(boundaries) - 2
        if is_last_interval:
            frequency = sum(lower <= value <= upper for value in values)
        else:
            frequency = sum(lower <= value < upper for value in values)
        rows.append((f"{lower:g}–{upper:g}", frequency, frequency / total))
    return rows


def linear_interpolation(
    x1: float, y1: float, x2: float, y2: float, x: float
) -> float:
    """Estimate y at x between two known points."""
    if x1 == x2:
        raise ValueError("x1 and x2 must be different.")
    return y1 + ((x - x1) / (x2 - x1)) * (y2 - y1)


def normal_cdf(z_score: float) -> float:
    """Return P(Z <= z) for the standard normal distribution."""
    return 0.5 * (1 + math.erf(z_score / math.sqrt(2)))


def z_score(value: float, average: float, spread: float) -> float:
    """Standardise a value using z = (x - mean) / standard deviation."""
    if spread == 0:
        raise ValueError("Standard deviation must not be zero.")
    return (value - average) / spread


def covariance(x_values: Sequence[float], y_values: Sequence[float]) -> float:
    """Return population covariance between two equal-length sequences."""
    if len(x_values) != len(y_values):
        raise ValueError("Both sequences must have the same length.")
    x_average = mean(x_values)
    y_average = mean(y_values)
    return sum(
        (x - x_average) * (y - y_average)
        for x, y in zip(x_values, y_values)
    ) / len(x_values)


def correlation(x_values: Sequence[float], y_values: Sequence[float]) -> float:
    """Return Pearson's correlation coefficient."""
    denominator = standard_deviation(x_values) * standard_deviation(y_values)
    if denominator == 0:
        raise ValueError("Correlation is undefined when a variable has no spread.")
    return covariance(x_values, y_values) / denominator


def linear_regression(
    x_values: Sequence[float], y_values: Sequence[float]
) -> tuple[float, float, float, float]:
    """Return slope, intercept, correlation, and R squared."""
    if len(x_values) != len(y_values) or len(x_values) < 2:
        raise ValueError("Regression needs two equal-length sequences with 2+ values.")
    x_average = mean(x_values)
    y_average = mean(y_values)
    denominator = sum((x - x_average) ** 2 for x in x_values)
    if denominator == 0:
        raise ValueError("Regression needs variation in x values.")
    slope = sum(
        (x - x_average) * (y - y_average)
        for x, y in zip(x_values, y_values)
    ) / denominator
    intercept = y_average - slope * x_average
    r = correlation(x_values, y_values)
    return slope, intercept, r, r**2


def ascii_histogram(values: Sequence[float], boundaries: Sequence[float]) -> str:
    """Build a simple text histogram for the terminal."""
    rows = grouped_frequency(values, boundaries)
    return "\n".join(
        f"{interval:>11} | {'#' * frequency} ({frequency})"
        for interval, frequency, _ in rows
    )


def print_report(debt_ratio: Sequence[float], growth_rate: Sequence[float]) -> None:
    """Print the complete investigation report."""
    average = mean(debt_ratio)
    middle = median(debt_ratio)
    population_sd = standard_deviation(debt_ratio)
    q1, _, q3 = quartiles(debt_ratio)
    boundaries = [45, 60, 75, 90, 105]
    slope, intercept, r, r_squared = linear_regression(growth_rate, debt_ratio)

    print("=" * 68)
    print("NATIONAL DEBT INVESTIGATION | INTRODUCTORY STATISTICS 1")
    print("=" * 68)
    print(f"Observations: {len(debt_ratio)} annual values ({YEAR[0]}–{YEAR[-1]})")

    print("\n1. LOCATION")
    print(f"Mean:              {average:.2f}% of GDP")
    print(f"Median:            {middle:.2f}% of GDP")
    print(f"Mode:              {multimode(debt_ratio)}")
    print(f"Quartile 1 (Q1):   {q1:.2f}")
    print(f"Quartile 3 (Q3):   {q3:.2f}")
    print(f"Interquartile range: {q3 - q1:.2f}")

    print("\n2. DISPERSION")
    print(f"Range:             {max(debt_ratio) - min(debt_ratio):.2f}")
    print(f"Population variance: {population_variance(debt_ratio):.2f}")
    print(f"Sample variance:    {sample_variance(debt_ratio):.2f}")
    print(f"Population SD:      {population_sd:.2f}")
    print(f"Sample SD:          {standard_deviation(debt_ratio, sample=True):.2f}")
    print(f"Pearson skewness:   {pearson_skewness(debt_ratio):.2f}")

    print("\n3. GROUPED DATA AND HISTOGRAM")
    print("Interval     Frequency  Relative")
    for interval, frequency, relative in grouped_frequency(debt_ratio, boundaries):
        print(f"{interval:>11} {frequency:>10}  {relative:>8.2%}")
    print("\n" + ascii_histogram(debt_ratio, boundaries))

    print("\n4. STANDARD NORMAL DISTRIBUTION")
    selected_ratio = 90
    selected_z = z_score(selected_ratio, average, population_sd)
    probability = normal_cdf(selected_z)
    print(f"For x = {selected_ratio}%: z = {selected_z:.2f}")
    print(f"P(X <= {selected_ratio}) = {probability:.2%}")

    print("\n5. LINEAR INTERPOLATION")
    estimated = linear_interpolation(75, 0.0, 90, 1.0, 82)
    print(f"At x = 82 between x = 75 and x = 90: y = {estimated:.2f}")

    print("\n6. CORRELATION AND REGRESSION")
    print(f"Correlation r:     {r:.2f}")
    print(f"R squared:          {r_squared:.2%}")
    print(f"Regression line:    debt = {slope:.2f} * growth + {intercept:.2f}")
    print("Interpretation: a negative slope means higher growth is associated")
    print("with a lower debt ratio in this illustrative sample.")


if __name__ == "__main__":
    print_report(DEBT_RATIO, GROWTH_RATE)
