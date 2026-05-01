#!/usr/bin/env python3
"""
Extract raw wOffset values from debug.log to validate the exponential model.
Also creates log-histogram and CDF plots to test P(d) ∝ e^(-λd).
"""
import sys
import math

# Import from lib
sys.path.insert(0, 'lib')
from lib.parser_lib import extract_all_offsets, parse_debug_log
from lib.model_lib import estimate_lambda_mle, memoryless_test, truncated_exponential_fit
from lib.plot_lib import setup_plot, save_plot, plot_line, plot_histogram

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 validate_model.py <debug_log> <nBits>")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = int(sys.argv[2])
    
    print(f"=== Fact0rn wOffset Raw Data Extraction ===\n")
    
    # Extract offsets for target nBits
    print(f"Extracting offsets for nBits={target_nBits}...")
    offsets = extract_all_offsets(debug_log, str(target_nBits))
    print(f"  Found {len(offsets)} samples\n")
    
    if not offsets:
        print(f"No data found for nBits={target_nBits}")
        sys.exit(1)
    
    # Basic stats
    n_tilde = 16 * target_nBits
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    
    print(f"ñ = {n_tilde}")
    print(f"  Sample count: {len(offsets)}")
    print(f"  Offset range: [{min(offsets)}, {max(offsets)}]")
    print(f"  d range: [{min(d_values)}, {max(d_values)}]\n")
    
    # MLE λ
    mle_lam = estimate_lambda_mle(offsets, target_nBits)
    if mle_lam:
        print(f"  MLE λ = {mle_lam:.6f}")
        print(f"  1/λ = {1.0/mle_lam:.1f}")
        print(f"  Compare to E[d] = {1.0/mle_lam:.1f}\n")
    
    # Log-histogram
    print("  Log-Histogram (check linearity for exponential):")
    print("           d |    count |   log(count)")
    print("  " + "-" * 50)
    
    # Create histogram bins
    max_d = max(d_values) if d_values else 1
    bin_size = max(1, max_d // 10)
    bins = {}
    for d in d_values:
        bin_idx = (d // bin_size) * bin_size
        if bin_idx not in bins:
            bins[bin_idx] = 0
        bins[bin_idx] += 1
    
    for bin_idx in sorted(bins.keys()):
        count = bins[bin_idx]
        log_count = math.log(count) if count > 0 else float('-inf')
        print(f"       {bin_idx:6.1f} | {count:7d} | {log_count:8.4f}")
    
    # Memoryless property test
    print(f"\n  Memoryless Property Test (exponential validation):")
    print("       k |      m |    empirical |  theoretical |      error")
    print("  " + "-" * 70)
    
    test_cases = [(100, 100), (100, 500), (100, 1000), (500, 100), (500, 500)]
    errors = []
    
    for k, m in test_cases:
        emp, theo, err = memoryless_test(offsets, target_nBits, k, m)
        if emp is not None:
            print(f"    {k:5d} |  {m:5d} | {emp:10.4f} | {theo:12.4f} |   {err:.4f}")
            errors.append(err)
    
    if errors:
        avg_error = sum(errors) / len(errors)
        print(f"\n  Average error: {avg_error:.4f}")
        if avg_error > 0.1:
            print("  ⚠️  Memoryless property questionable (model may be wrong)")
        else:
            print("  ✅ Memoryless property holds (exponential model valid)")
    
    # Truncated exponential fit
    print(f"\nTruncated Exponential Fit:")
    trunc_lam = truncated_exponential_fit(offsets, target_nBits)
    if trunc_lam:
        print(f"  λ (MLE) = {trunc_lam:.6f}")
        print(f"  1/λ = {1.0/trunc_lam:.1f}")
        print(f"  Compare to E[d] = {1.0/trunc_lam:.1f}")

if __name__ == '__main__':
    main()
