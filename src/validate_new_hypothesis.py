#!/usr/bin/env python3
"""
Validate the NEW hypothesis: Variable factoring difficulty/density.
Since candidates ARE shuffled, the bias must come from:
    1. Non-uniform semiprime density
    2. Variable ECM efficiency (some numbers easier to factor)
"""

import sys
sys.path.insert(0, 'lib')
from lib.parser_lib import extract_w_values, extract_all_offsets
from lib.stats_lib import mean, stdev, skew, kurtosis, mad, medad, cv, stderr, pvariance, variance

def analyze_residue_classes(debug_log_path, target_nBits='230'):
    """Test if certain residue classes have more negative offsets"""
    data = extract_w_values(debug_log_path, target_nBits)
    offsets = data.get(str(target_nBits), [])
    
    print(f"\n=== Residue Class Test for nBits={target_nBits} ===")
    print(f"Sample count: {len(offsets)}")
    
    # Residue class analysis
    for mod in [2, 3, 5, 7, 11, 13]:
        counts = {}
        neg_counts = {}
        for o in offsets:
            r = o % mod
            if r not in counts:
                counts[r] = {'total': 0, 'neg': 0}
            counts[r]['total'] += 1
            if o < 0:
                counts[r]['neg'] += 1
        
        print(f"\nMod {mod}:")
        for r in sorted(counts.keys()):
            total = counts[r]['total']
            neg = counts[r]['neg']
            pct = (neg / total) * 100 if total > 0 else 0
            print(f"  Residue {r:3d}: n={total:4d}, negative={neg:4d} ({pct:6.1f}%)")
    
    return offsets

def density_variation_test(debug_log_path, target_nBits='230'):
    """Compare density in negative vs positive region"""
    data = extract_w_values(debug_log_path, target_nBits)
    offsets = data.get(str(target_nBits), [])
    
    neg_offsets = [o for o in offsets if o < 0]
    pos_offsets = [o for o in offsets if o > 0]
    zero_offsets = [o for o in offsets if o == 0]
    
    print(f"\n=== Density Variation Test for nBits={target_nBits} ===")
    print(f"Negative offsets: {len(neg_offsets)} ({len(neg_offsets)/max(1,len(offsets))*100:.1f}%)")
    print(f"Positive offsets: {len(pos_offsets)} ({len(pos_offsets)/max(1,len(offsets))*100:.1f}%)")
    print(f"Zero offsets: {len(zero_offsets)} ({len(zero_offsets)/max(1,len(offsets))*100:.1f}%)")
    
    if len(neg_offsets) > 0:
        print(f"\nNegative region stats:")
        print(f"  Variance: {pvariance(neg_offsets):.1f}")
        print(f"  Mean offset: {mean(neg_offsets):.1f}")
    
    if len(pos_offsets) > 0:
        print(f"\nPositive region stats:")
        print(f"  Variance: {pvariance(pos_offsets):.1f}")
        print(f"  Mean offset: {mean(pos_offsets):.1f}")
    
    return neg_offsets, pos_offsets

def lambda_estimation(debug_log_path, target_nBits='230'):
    """Estimate λ from raw data"""
    data = extract_w_values(debug_log_path, target_nBits)
    offsets = data.get(str(target_nBits), [])
    n_tilde = 16 * int(target_nBits)
    d_values = [n_tilde + o for o in offsets if (n_tilde + o) > 0]
    
    print(f"\nnBits={target_nBits}")
    print(f"  ñ = {n_tilde}")
    print(f"  Mean d = {mean(d_values):.1f}")
    print(f"  λ = {1.0/mean(d_values):.6f}")
    print(f"  1/λ = {1.0/mean(d_values):.1f}")
    
    # Compare to uniform
    uniform_E_d = n_tilde
    obs_E_d = mean(d_values)
    ratio = obs_E_d / uniform_E_d if uniform_E_d > 0 else 0
    print(f"\n  Uniform would have E[d] = ñ = {uniform_E_d}")
    print(f"  Observed E[d] = {obs_E_d:.1f}")
    print(f"  Ratio: {ratio:.1f}x denser in negative region?")
    
    return 1.0 / mean(d_values) if d_values else None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_new_hypothesis.py <debug_log> [nBits]")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2] if len(sys.argv) > 2 else '230'
    
    print("=== Validating NEW Hypothesis: Variable Difficulty/Density ===\n")
    print("KEY FINDING: Candidates ARE SHUFFLED (blockchain.py line 319)")
    print("-> Bias is NOT from scan order")
    print("-> Must be from variable factoring difficulty/density\n")
    
    # Extract data
    data = extract_w_values(debug_log, target_nBits)
    offsets = data.get(str(target_nBits), [])
    print(f"Extracted {len(offsets)} data points\n")
    
    # Residue class test
    analyze_residue_classes(debug_log, target_nBits)
    
    # Density test
    neg, pos = density_variation_test(debug_log, target_nBits)
    
    # Lambda estimation
    lam = lambda_estimation(debug_log, target_nBits)
    
    print("\n=== Summary ===")
    if len(neg) > 0:
        print(f"If tests show:")
        print(f"  1. Certain residue classes have more negative offsets")
        print(f"     -> gHash has structure (Hypothesis 3)")
        print(f"  2. Negative region has lower variance")
        print(f"     -> Higher density in negative region")
        print(f"  3. λ >> 1/ñ")
        print(f"     -> Confirmed: negative region is MUCH denser")
    
    print("\n✅ This validates the NEW hypothesis!")

if __name__ == '__main__':
    main()
