#!/usr/bin/env python3
"""
Visualize wOffset distribution and fit truncated exponential model.
Tests if P(d) ∝ e^(-λd) for d ∈ [0, 2ñ]
"""
import sys
import csv
import math
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def extract_offsets(debug_log_path, target_nBits=None):
    """Extract nBits and wOffset from debug.log"""
    data = defaultdict(list)
    count = 0
    for line in open(debug_log_path, 'r'):
        if "UpdateTip" in line:
            parts = line.split()
            if len(parts) > 7:
                try:
                    nBits = parts[6].split('=')[1]
                    wOffset = int(parts[7].split('=')[1])
                    if target_nBits is None or nBits == target_nBits:
                        data[nBits].append(wOffset)
                        count += 1
                except:
                    pass
    return data

def compute_d_values(nBits, offsets):
    """Convert offsets to d = ñ + offset = 16*nBits + offset"""
    n_tilde = 16 * int(nBits)
    return [n_tilde + offset for offset in offsets]

def plot_log_histogram(d_values, nBits, output_path):
    """Plot log-histogram to test exponential model"""
    n_tilde = 16 * int(nBits)
    
    # Create histogram
    num_bins = 50
    max_d = 2 * n_tilde
    bin_width = max_d / num_bins
    
    bins = [0] * num_bins
    for d in d_values:
        if 0 <= d < max_d:
            idx = int(d / bin_width)
            if idx >= num_bins:
                idx = num_bins - 1
            bins[idx] += 1
    
    # Compute log(frequency)
    bin_centers = [(i + 0.5) * bin_width for i in range(num_bins)]
    log_freq = []
    valid_centers = []
    for i, count in enumerate(bins):
        if count > 0:
            log_freq.append(math.log(count))
            valid_centers.append(bin_centers[i])
    
    # Fit line to log(frequency) vs d (should be linear for exponential)
    if len(valid_centers) > 2:
        # Simple linear regression
        n = len(valid_centers)
        sum_x = sum(valid_centers)
        sum_y = sum(log_freq)
        sum_xy = sum(x * y for x, y in zip(valid_centers, log_freq))
        sum_x2 = sum(x**2 for x in valid_centers)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Predicted lambda
        lambda_est = -slope
    else:
        lambda_est = 0
        intercept = 0
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram
    ax1.bar(bin_centers, bins, width=bin_width*0.8, alpha=0.7, color='blue')
    ax1.set_xlabel('d = ñ + offset (distance from left boundary)')
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'nBits={nBits}: Histogram of d')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, max_d)
    
    # Log-histogram
    ax2.scatter(valid_centers, log_freq, alpha=0.7, color='red', s=30)
    
    # Fit line
    if lambda_est > 0:
        x_fit = [0, max(valid_centers)]
        y_fit = [intercept, intercept + slope * max(valid_centers)]
        ax2.plot(x_fit, y_fit, 'g-', linewidth=2, 
                 label=f'λ={lambda_est:.6f} (slope={-slope:.6f})')
    
    ax2.set_xlabel('d (distance from left boundary)')
    ax2.set_ylabel('log(frequency)')
    ax2.set_title(f'nBits={nBits}: Log-Histogram (linear=exponential)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return lambda_est, bins, bin_centers

def fit_truncated_exponential(d_values, n_tilde):
    """
    Fit truncated exponential P(d) = λe^(-λd) / (1 - e^(-λ*2ñ))
    MLE: λ = 1/mean(d) is approximately correct for small truncation
    """
    if not d_values:
        return None
    
    mean_d = sum(d_values) / len(d_values)
    if mean_d <= 0:
        return None
    
    # Simple MLE (ignoring truncation for rough estimate)
    lambda_mle = 1.0 / mean_d
    
    # Correct for truncation (improves estimate)
    max_d = 2 * n_tilde
    if lambda_mle * max_d < 10:  # Not too extreme
        correction = 1.0 / (1.0 - max_d / (math.exp(lambda_mle * max_d) - 1))
        lambda_mle *= correction
    
    return lambda_mle

def compute_cumulative_probability(d_values, d_max):
    """Empirical CDF"""
    sorted_d = sorted(d_values)
    n = len(sorted_d)
    cdf = []
    for d in [i * d_max / 100 for i in range(101)]:
        count = sum(1 for x in d_values if x <= d)
        cdf.append((d, count / n))
    return cdf

def theoretical_cdf(d, lam, n_tilde):
    """Theoretical CDF for truncated exponential"""
    if lam <= 0:
        return 0
    max_d = 2 * n_tilde
    Z = 1.0 - math.exp(-lam * max_d)  # Normalization
    if Z <= 0:
        return 0
    return (1.0 - math.exp(-lam * d)) / Z

def plot_cdf_comparison(d_values, nBits, lambda_est, output_path):
    """Compare empirical vs theoretical CDF"""
    n_tilde = 16 * int(nBits)
    
    # Empirical CDF
    sorted_d = sorted(d_values)
    n = len(sorted_d)
    emp_d = []
    emp_cdf = []
    for i, d in enumerate(sorted_d):
        emp_d.append(d)
        emp_cdf.append((i + 1) / n)
    
    # Theoretical CDF
    theo_d = [i * 2 * n_tilde / 100 for i in range(101)]
    theo_cdf = [theoretical_cdf(d, lambda_est, n_tilde) for d in theo_d]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(emp_d[:1000], emp_cdf[:1000], 'b-', alpha=0.5, label='Empirical CDF', linewidth=1)
    plt.plot(theo_d, theo_cdf, 'r--', label='Theoretical (trunc. exponential)', linewidth=2)
    plt.xlabel('d = distance from left boundary')
    plt.ylabel('P(D ≤ d)')
    plt.title(f'nBits={nBits}: CDF Comparison (λ={lambda_est:.6f})')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 plot_distribution.py <debug.log> [nBits]")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2] if len(sys.argv) > 2 else '230'
    
    print("=== Fact0rn wOffset Distribution Analysis ===\n")
    
    # Extract data
    data = extract_offsets(debug_log, target_nBits)
    
    if target_nBits not in data:
        print(f"nBits={target_nBits} not found in data")
        sys.exit(1)
    
    offsets = data[target_nBits]
    nBits = int(target_nBits)
    n_tilde = 16 * nBits
    d_values = compute_d_values(target_nBits, offsets)
    
    print(f"nBits={nBits}")
    print(f"ñ = {n_tilde}")
    print(f"Sample count: {len(offsets)}")
    print(f"d range: [{min(d_values)}, {max(d_values)}]")
    print(f"2*ñ = {2*n_tilde}")
    
    # Fit truncated exponential
    lambda_est = fit_truncated_exponential(d_values, n_tilde)
    if lambda_est:
        print(f"\nTruncated Exponential Fit:")
        print(f"  λ (MLE) = {lambda_est:.6f}")
        print(f"  1/λ = {1.0/lambda_est:.1f}")
        print(f"  Compare to E[d] = {sum(d_values)/len(d_values):.1f}")
    
    # Plot log-histogram
    output1 = f'../results/distribution_hist_nBits{nBits}.png'
    lambda_fit, bins, centers = plot_log_histogram(d_values, target_nBits, output1)
    print(f"\nLog-histogram fit: λ = {lambda_fit:.6f}")
    print(f"Saved: {output1}")
    
    # Plot CDF comparison
    output2 = f'../results/distribution_cdf_nBits{nBits}.png'
    plot_cdf_comparison(d_values, target_nBits, lambda_est, output2)
    print(f"Saved: {output2}")
    
    # Compute probability mass in different ranges
    print(f"\nProbability Mass Analysis:")
    max_d = 2 * n_tilde
    ranges = [(0, 0.25*max_d), (0, 0.5*max_d), (0, 0.75*max_d), (0, max_d)]
    
    for r_start, r_end in ranges:
        count = sum(1 for d in d_values if r_start <= d <= r_end)
        pct = 100.0 * count / len(d_values)
        print(f"  d ∈ [{r_start:.0f}, {r_end:.0f}]: {pct:.1f}% of samples")
    
    # Expected speedup
    if lambda_est:
        uniform_work = max_d
        optimized_work = 1.0 / lambda_est
        speedup = uniform_work / optimized_work
        print(f"\nExpected Speedup vs Uniform Search:")
        print(f"  Uniform: scan all {uniform_work} positions")
        print(f"  Optimized: expected {optimized_work:.1f} positions (1/λ)")
        print(f"  Speedup: {speedup:.1f}x")
        print(f"\n  ⚡ This is 'free' performance from smarter search order!")

if __name__ == '__main__':
    main()
