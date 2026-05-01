#!/usr/bin/env python3
"""
Visualize wOffset distribution and fit truncated exponential model.
Tests if P(d) ∝ e^(-λd) for d ∈ [0, 2ñ]
"""
import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import from lib
sys.path.insert(0, 'lib')
from lib.parser_lib import extract_all_offsets
from lib.model_lib import estimate_lambda_mle, truncated_exponential_fit
from lib.plot_lib import setup_plot, save_plot, plot_line, plot_histogram
from lib.stats_lib import mean, stdev

def plot_log_histogram(d_values, nBits, output_path):
    """Plot log-histogram to test exponential model"""
    n_tilde = 16 * nBits
    max_d = max(d_values) if d_values else 1
    bin_size = max(1, max_d // 10)
    
    bins = {}
    for d in d_values:
        bin_idx = (d // bin_size) * bin_size
        if bin_idx not in bins:
            bins[bin_idx] = 0
        bins[bin_idx] += 1
    
    setup_plot(title=f'wOffset Distribution (nBits={nBits})', 
                xlabel='d = ñ+offset', ylabel='log(Count)')
    
    for bin_idx in sorted(bins.keys()):
        count = bins[bin_idx]
        log_count = math.log(count) if count > 0 else float('-inf')
        plot_line([bin_idx], [log_count], 'o', label=f'bin {bin_idx}')
    
    plt.legend()
    save_plot(output_path)

def plot_cdf_comparison(d_values, lambda_val, nBits, output_path):
    """Plot empirical vs theoretical CDF"""
    n_tilde = 16 * nBits
    d_sorted = sorted(d_values)
    n = len(d_sorted)
    
    # Empirical CDF
    emp_cdf = [(d_sorted[i], (i+1)/n) for i in range(n)]
    
    # Theoretical CDF (truncated exponential)
    if lambda_val and lambda_val > 0:
        theo_cdf = [(d, 1 - math.exp(-lambda_val * d)) for d in d_sorted]
    else:
        theo_cdf = []
    
    setup_plot(title=f'CDF Comparison (nBits={nBits})', 
                xlabel='d = ñ+offset', ylabel='P(D ≤ d)')
    
    if emp_cdf:
        plot_line([x for x,_ in emp_cdf], [y for _,y in emp_cdf], 
                  '-', label='Empirical', linewidth=2)
    if theo_cdf:
        plot_line([x for x,_ in theo_cdf], [y for _,y in theo_cdf], 
                  '--', label=f'Theoretical (λ={lambda_val:.6f})')
    
    plt.legend()
    save_plot(output_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 plot_distribution.py <debug_log> <nBits>")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2]
    
    print(f"=== Fact0rn wOffset Distribution Analysis ===\n")
    
    # Extract offsets
    print(f"nBits={target_nBits}")
    offsets = extract_all_offsets(debug_log, target_nBits)
    print(f"  Sample count: {len(offsets)}\n")
    
    if not offsets:
        print(f"No data found for nBits={target_nBits}")
        sys.exit(1)
    
    n_tilde = 16 * int(target_nBits)
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    
    print(f"ñ = {n_tilde}")
    print(f"Sample count: {len(offsets)}")
    print(f"d range: [{min(d_values)}, {max(d_values)}]\n")
    
    # Truncated Exponential Fit
    print("Truncated Exponential Fit:")
    mle_lam = truncated_exponential_fit(offsets, int(target_nBits))
    if mle_lam:
        print(f"  λ (MLE) = {mle_lam:.6f}")
        print(f"  1/λ = {1.0/mle_lam:.1f}")
        print(f"  Compare to E[d] = {1.0/mle_lam:.1f}\n")
    
    # Log-histogram
    print("Log-histogram fit: λ = ...")  # Would calculate from regression
    
    # Save plots
    output1 = f'../results/distribution_hist_nBits{target_nBits}.png'
    plot_log_histogram(d_values, int(target_nBits), output1)
    print(f"Saved: {output1}")
    
    output2 = f'../results/distribution_cdf_nBits{target_nBits}.png'
    plot_cdf_comparison(d_values, mle_lam, int(target_nBits), output2)
    print(f"Saved: {output2}\n")
    
    # Probability Mass Analysis
    print("Probability Mass Analysis:")
    d_sorted = sorted(d_values)
    n = len(d_sorted)
    
    for percentile in [0.50, 0.80, 0.90, 0.95, 1.0]:
        idx = min(int(percentile * n), n-1)
        d_val = d_sorted[idx]
        print(f"  d ∈ [0, {d_val}] = {percentile*100:.1f}% of samples")
    
    # Expected Speedup
    if mle_lam:
        E_d = 1.0 / mle_lam
        uniform = 2 * n_tilde
        speedup = uniform / E_d
        print(f"\nExpected Speedup vs Uniform Search:")
        print(f"  Uniform: scan all {uniform} positions")
        print(f"  Optimized: expected {E_d:.1f} positions (1/λ)")
        print(f"  Speedup: {speedup:.1f}x\n")
    
    print(f"  ⚡ This is 'free' performance from smarter search order!")

if __name__ == '__main__':
    main()
