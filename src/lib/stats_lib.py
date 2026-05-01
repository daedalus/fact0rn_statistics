#!/usr/bin/env python3
"""
Fact0rn Statistics Library - Common Statistical Functions
Used by: plot_stats.py, model_offset.py, analyze_bias_source.py, etc.
"""

from statistics import mean, stdev, median
import math

def percentile(data, p):
    """Calculate percentile p (0-100) from data"""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    k = (p / 100) * (n - 1)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return d0 + d1

def p5(data):
    """5th percentile"""
    return percentile(data, 5)

def p25(data):
    """25th percentile (Q1)"""
    return percentile(data, 25)

def p75(data):
    """75th percentile (Q3)"""
    return percentile(data, 75)

def p95(data):
    """95th percentile"""
    return percentile(data, 95)

def iqr(data):
    """Interquartile Range (Q3 - Q1)"""
    return p75(data) - p25(data)

def mag(data):
    """Mean Absolute rate of change (abs difference between consecutive values)"""
    if len(data) < 2:
        return 0.0
    return mean([abs(data[i+1] - data[i]) for i in range(len(data)-1)])

def mage(data):
    """Mean Amplitude of Large Excursions - avg of excursions > 1 SD from mean"""
    if len(data) < 3:
        return 0.0
    m = mean(data)
    sd = stdev(data) if len(data) > 1 else 0.0
    if sd == 0:
        return 0.0
    # Find turning points (local maxima/minima)
    turning_points = []
    for i in range(1, len(data)-1):
        if (data[i] >= data[i-1] and data[i] >= data[i+1]) or \
           (data[i] <= data[i-1] and data[i] <= data[i+1]):
            turning_points.append(data[i])
    # Filter excursions > 1 SD
    excursions = [abs(tp - m) for tp in turning_points if abs(tp - m) > sd]
    if not excursions:
        return 0.0
    return mean(excursions)

def trend_slope(data):
    """Linear regression slope of data vs index (measures drift over sequence)"""
    n = len(data)
    if n < 2:
        return 0.0
    x = list(range(n))
    sum_x = sum(x)
    sum_y = sum(data)
    sum_xy = sum(x[i] * data[i] for i in range(n))
    sum_x2 = sum(xi**2 for xi in x)
    denom = n * sum_x2 - sum_x**2
    if denom == 0:
        return 0.0
    return (n * sum_xy - sum_x * sum_y) / denom

def gvp(data):
    """Variability Percentage - path length vs flat baseline"""
    if len(data) < 2:
        return 0.0
    # Curve length = sum of abs differences
    curve_length = sum(abs(data[i+1] - data[i]) for i in range(len(data)-1))
    # Flat length = distance from first to last
    flat_length = abs(data[-1] - data[0]) if data[-1] != data[0] else 1.0
    return ((curve_length / flat_length) - 1) * 100

def cv_rate(data):
    """CV of rate-of-change series"""
    if len(data) < 2:
        return 0.0
    rates = [abs(data[i+1] - data[i]) for i in range(len(data)-1)]
    if mean(rates) == 0:
        return 0.0
    return (stdev(rates) / mean(rates)) * 100

def avg_abs_dev(data):
    """Average absolute deviation from mean"""
    if not data:
        return 0.0
    m = mean(data)
    return mean([abs(x - m) for x in data])

def sq_dev_mean(data):
    """Squared deviations from mean (sum of squares)"""
    if not data:
        return 0.0
    m = mean(data)
    return sum((x - m) ** 2 for x in data)

def least_abs_dev(data, predicted=None):
    """Least absolute deviations - sum of abs differences from predicted (or mean)"""
    if not data:
        return 0.0
    ref = predicted if predicted is not None else mean(data)
    return sum(abs(x - ref) for x in data)

def rms(data):
    """Root Mean Square"""
    if not data:
        return 0.0
    return math.sqrt(mean([x ** 2 for x in data]))

def skew(data):
    """Calculate skewness of data"""
    m = mean(data)
    n = len(data)
    m3 = sum((x - m) ** 3 for x in data) / n
    m2 = sum((x - m) ** 2 for x in data) / n
    if m2 == 0:
        return 0.0
    return m3 / (m2 ** 1.5)

def kurtosis(data):
    """Calculate excess kurtosis of data (normal=0)"""
    m = mean(data)
    n = len(data)
    m4 = sum((x - m) ** 4 for x in data) / n
    m2 = sum((x - m) ** 2 for x in data) / n
    if m2 == 0:
        return 0.0
    return m4 / (m2 ** 2) - 3  # excess kurtosis

def mad(data):
    """Mean Absolute Deviation"""
    m = mean(data)
    return mean([abs(x - m) for x in data])

def medad(data):
    """Median Absolute Deviation"""
    med = median(data)
    return median([abs(x - med) for x in data])

def cv(data):
    """Coefficient of Variation (as percentage)"""
    if mean(data) == 0:
        return float('inf')
    return (stdev(data) / mean(data)) * 100

def stderr(data):
    """Standard Error of the Mean"""
    if len(data) == 0:
        return 0.0
    return stdev(data) / (len(data) ** 0.5)

def pvariance(data):
    """Population variance"""
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / len(data)

def variance(data):
    """Sample variance"""
    m = mean(data)
    n = len(data)
    if n <= 1:
        return 0.0
    return sum((x - m) ** 2 for x in data) / (n - 1)
