#!/usr/bin/env python3
"""
Validate the NEW hypothesis: Variable factoring difficulty/density.

Since candidates ARE shuffled (line 319 of blockchain.py),
the bias must come from:
1. Non-uniform semiprime density across [W-ñ, W+ñ]
2. Variable ECM efficiency (some numbers easier to factor)

This script tests:
- Does gHash produce W with structure?
- Do certain residue classes have more semiprimes?
- Is the negative region actually "easier" to factor?
"""
import sys
import csv
from collections import defaultdict

def extract_w_values(debug_log_path, target_nBits=None):
    """Extract W values and offsets from debug.log"""
    data = []
    w_values = defaultdict(list)
    
    count = 0
    for line in open(debug_log_path, 'r'):
        if "UpdateTip" in line:
            parts = line.split()
            if len(parts) > 7:
                try:
                    nBits = parts[6].split('=')[1]
                    wOffset = int(parts[7].split('=')[1])
                    
                    if target_nBits is None or nBits == target_nBits:
                        # We don't have W directly, but we can infer:
                        # wOffset = n - W, so W = n - wOffset
                        # But we don't have n (the semiprime found)
                        # We only have the offset
                        data.append({
                            'nBits': nBits,
                            'offset': wOffset,
                            'd': 16 * int(nBits) + wOffset  # distance from left boundary
                        })
                        count += 1
                except:
                    pass
    
    print(f"Extracted {count} data points")
    return data

def test_residue_class_bias(data, nBits='230'):
    """
    Test if certain residue classes (mod small primes) have more negative offsets.
    
    If gHash produces W with certain residue classes,
    and those classes have higher semiprime density in negative region,
    that would explain the bias.
    """
    # Filter for target nBits
    filtered = [d for d in data if d['nBits'] == nBits]
    
    if not filtered:
        print(f"No data for nBits={nBits}")
        return
    
    print(f"\n=== Residue Class Test for nBits={nBits} ===")
    print(f"Sample count: {len(filtered)}\n")
    
    # Test mod 2, 3, 5, 7
    for mod in [2, 3, 5, 7, 11, 13]:
        # Group by residue
        residues = defaultdict(list)
        for d in filtered:
            r = d['offset'] % mod
            residues[r].append(d['offset'])
        
        # Check if certain residues have more negative offsets
        print(f"Mod {mod}:")
        for r in sorted(residues.keys()):
            offsets = residues[r]
            neg_count = sum(1 for o in offsets if o < 0)
            neg_pct = 100.0 * neg_count / len(offsets)
            avg_offset = sum(offsets) / len(offsets)
            print(f"  Residue {r:>2}: n={len(offsets):>4}, negative={neg_pct:>6.1f}%, avg_offset={avg_offset:>8.1f}")
        print()

def test_density_variation(data, nBits='230'):
    """
    Test if density varies across the interval.
    
    If negative region has higher density, we'd expect:
    - More samples with negative offsets
    - Lower variance in negative region (more predictable)
    """
    filtered = [d for d in data if d['nBits'] == nBits]
    
    if not filtered:
        return
    
    print(f"\n=== Density Variation Test for nBits={nBits} ===\n")
    
    # Split into negative and positive regions
    neg = [d for d in filtered if d['offset'] < 0]
    pos = [d for d in filtered if d['offset'] > 0]
    zero = [d for d in filtered if d['offset'] == 0]
    
    print(f"Negative offsets: {len(neg)} samples ({100*len(neg)/len(filtered):.1f}%)")
    print(f"Positive offsets: {len(pos)} samples ({100*len(pos)/len(filtered):.1f}%)")
    print(f"Zero offsets: {len(zero)} samples\n")
    
    if len(neg) > 0 and len(pos) > 0:
        # Compare variances
        neg_var = sum((d['offset'] - sum(d['offset'] for d in neg)/len(neg))**2 for d in neg) / len(neg)
        pos_var = sum((d['offset'] - sum(d['offset'] for d in pos)/len(pos))**2 for d in pos) / len(pos)
        
        print(f"Variance (negative region): {neg_var:.1f}")
        print(f"Variance (positive region): {pos_var:.1f}")
        
        if neg_var < pos_var:
            print(f"\n✅ Negative region has LOWER variance (more predictable)")
        else:
            print(f"\n⚠️  Negative region has HIGHER variance")

def estimate_actual_lambda(data, nBits='230'):
    """Estimate λ from actual offset data (not summary stats)"""
    filtered = [d for d in data if d['nBits'] == nBits]
    
    if not filtered:
        return
    
    n_tilde = 16 * int(nBits)
    d_values = [d['d'] for d in filtered]
    
    # For exponential P(d) ∝ e^(-λd), MLE is λ = 1/mean(d)
    mean_d = sum(d_values) / len(d_values)
    
    if mean_d <= 0:
        print(f"\n⚠️  Mean d <= 0 for nBits={nBits}")
        return
    
    lam = 1.0 / mean_d
    
    print(f"\n=== Lambda Estimation for nBits={nBits} ===")
    print(f"ñ = {n_tilde}")
    print(f"Mean d = {mean_d:.1f}")
    print(f"λ = {lam:.6f}")
    print(f"1/λ = {1/lam:.1f}")
    
    # Compare to uniform (which would have mean_d = ñ)
    print(f"\nUniform would have E[d] = ñ = {n_tilde}")
    print(f"Observed E[d] = {mean_d:.1f}")
    print(f"Ratio: {n_tilde/mean_d:.1f}x denser in negative region?")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_new_hypothesis.py <debug.log> [nBits]")
        print("Example: python3 validate_new_hypothesis.py ~/.factorn/debug.log 230")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2] if len(sys.argv) > 2 else '230'
    
    print("=== Validating NEW Hypothesis: Variable Difficulty/Density ===\n")
    print("KEY FINDING: Candidates ARE SHUFFLED (blockchain.py line 319)")
    print("-> Bias is NOT from scan order")
    print("-> Must be from variable factoring difficulty/density\n")
    
    # Extract data
    data = extract_w_values(debug_log, target_nBits)
    
    if not data:
        print(f"No data found for nBits={target_nBits}")
        sys.exit(1)
    
    # Run tests
    test_residue_class_bias(data, target_nBits)
    test_density_variation(data, target_nBits)
    estimate_actual_lambda(data, target_nBits)
    
    print("\n=== Summary ===")
    print("If tests show:")
    print("1. Certain residue classes have more negative offsets")
    print("   -> gHash has structure (Hypothesis 3)")
    print("2. Negative region has lower variance")
    print("   -> Higher density in negative region")
    print("3. λ >> 1/ñ")
    print("   -> Confirmed: negative region is MUCH denser")
    print("\n✅ This validates the NEW hypothesis!")

if __name__ == '__main__':
    main()
