#!/usr/bin/env python3
"""
Fact0rn Lambda/Exponential Model Library
Used by: model_offset.py, validate_model.py, plot_distribution.py, etc.
"""

import math

def estimate_lambda(nBits, mean_offset):
    """
    For exponential distribution: E[d] = 1/λ
    where d = 16*nBits + offset = distance from left boundary
    E[d] = 16*nBits + E[offset]
    λ = 1 / E[d]
    """
    n_tilde = 16 * nBits
    E_d = n_tilde + mean_offset
    if E_d <= 0:
        return None
    return 1.0 / E_d

def estimate_lambda_mle(offsets, nBits):
    """Maximum Likelihood Estimate of λ from raw offset data"""
    n_tilde = 16 * nBits
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    if not d_values:
        return None
    # MLE for exponential: λ = 1 / mean(d)
    return 1.0 / mean(d_values)

def expected_speedup(lambda_val, n_tilde):
    """Calculate expected speedup vs uniform search"""
    if lambda_val is None or lambda_val == 0:
        return None
    E_d = 1.0 / lambda_val
    uniform_search_space = 2 * n_tilde
    return uniform_search_space / E_d

def memoryless_test(offsets, nBits, k, m):
    """
    Test memoryless property: P(d > k+m | d > k) ≈ P(d > m)
    Returns: (empirical, theoretical, error)
    """
    n_tilde = 16 * nBits
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    
    if not d_values:
        return (None, None, None)
    
    # P(d > k)
    P_d_gt_k = sum(1 for d in d_values if d > k) / len(d_values)
    
    # P(d > k+m | d > k) = P(d > k+m) / P(d > k)
    P_d_gt_km = sum(1 for d in d_values if d > k + m) / len(d_values)
    
    if P_d_gt_k == 0:
        return (None, None, None)
    
    empirical = P_d_gt_km / P_d_gt_k
    
    # Theoretical: P(d > m) = e^(-λm)
    lambda_val = 1.0 / mean(d_values)
    theoretical = math.exp(-lambda_val * m)
    
    error = abs(empirical - theoretical)
    
    return (empirical, theoretical, error)

def truncated_exponential_fit(offsets, nBits):
    """Fit truncated exponential to offset data"""
    n_tilde = 16 * nBits
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    if not d_values:
        return None
    return 1.0 / mean(d_values)
