#!/usr/bin/env python3
"""
Fact0rn Statistics Library - Common Statistical Functions
Used by: plot_stats.py, model_offset.py, analyze_bias_source.py, etc.
"""

from statistics import mean, stdev, median
import math

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
