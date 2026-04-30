#!/usr/bin/env python3
"""
Empirical model for P(offset | nBits) in Fact0rn mining.
Based on first-hit distribution theory from mining loop analysis.

Key insight: If scanning monotonically from W toward -ñ (downward),
the distribution of first-found semiprime follows approximately:
P(d) ∝ e^(-λd) where d = ñ + offset = distance from left boundary
"""
import sys
import csv
import math
from statistics import mean, stdev

def load_csv(csv_path):
    """Load wOffset statistics from CSV"""
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['nBits'] != 'GROUPED':
                data.append({
                    'nBits': int(row['nBits']),
                    'count': int(row['count']),
                    'min': int(row['min']),
                    'median': float(row['median']),
                    'mean': float(row['mean']),
                    'max': int(row['max']),
                    'stdev': float(row['stdev']),
                    'skew': float(row['skew']),
                    'kurtosis': float(row['kurtosis']),
                })
    return data

def estimate_lambda(nBits, mean_offset):
    """
    For exponential distribution: E[d] = 1/λ
    where d = ñ + offset = 16*nBits + offset
    E[d] = 16*nBits + E[offset]
    λ = 1 / E[d]
    """
    n_tilde = 16 * nBits
    E_d = n_tilde + mean_offset  # mean distance from left boundary
    if E_d <= 0:
        return None
    lam = 1.0 / E_d
    return lam

def predict_cumulative_probability(lam, d):
    """P(D <= d) = 1 - e^(-λd) for exponential distribution"""
    return 1.0 - math.exp(-lam * d)

def predict_probability_mass(lam, d_start, d_end):
    """Probability mass between d_start and d_end"""
    return predict_cumulative_probability(lam, d_end) - predict_cumulative_probability(lam, d_start)

def analyze_lambda_stability(data):
    """Check if λ is stable across nBits (as analysis suggests)"""
    results = []
    for row in data:
        nBits = row['nBits']
        lam = estimate_lambda(nBits, row['mean'])
        if lam:
            n_tilde = 16 * nBits
            E_d = n_tilde + row['mean']
            results.append({
                'nBits': nBits,
                'lambda': lam,
                'E_d': E_d,
                'n_tilde': n_tilde,
                'mean_offset': row['mean']
            })
    return results

def find_optimal_search_range(lam, n_tilde, coverage=0.90):
    """
    Find the search range that covers 'coverage' probability mass.
    Solve: 1 - e^(-λd) = coverage => d = -ln(1-coverage)/λ
    """
    if lam <= 0:
        return n_tilde * 2  # Full range as fallback
    d_max = -math.log(1.0 - coverage) / lam
    return min(int(d_max), 2 * n_tilde)

def calculate_expected_speedup(lam, n_tilde):
    """
    Calculate expected speedup vs uniform search.
    Uniform search: expected work = full range = 2*n_tilde
    Optimized (exponential): expected work = E[d] = 1/λ
    Speedup = uniform / optimized = 2*n_tilde / (1/λ)
    """
    optimized_work = 1.0 / lam
    uniform_work = 2 * n_tilde
    speedup = uniform_work / optimized_work
    return speedup

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else '../results/wOffset_statistics.csv'
    
    print("=== FACT0RN wOffset Empirical Model ===\n")
    
    # Load data
    data = load_csv(csv_path)
    print(f"Loaded {len(data)} nBits levels\n")
    
    # Estimate lambda across nBits
    print("1) Lambda Estimation (Exponential Model P(d) ∝ e^(-λd))")
    print("   where d = ñ + offset = distance from left boundary (-16*nBits)")
    print("   nBits | ñ | E[d] | λ (1/E[d]) | E[offset]")
    print("   " + "-" * 60)
    
    lam_results = analyze_lambda_stability(data)
    
    # Focus on stable range (nBits 230-300)
    stable_range = [r for r in lam_results if 230 <= r['nBits'] <= 300]
    
    for r in stable_range[:10]:  # Show first 10
        print(f"   {r['nBits']:5d} | {r['n_tilde']:5d} | {r['E_d']:8.1f} | {r['lambda']:.6f} | {r['mean_offset']:8.1f}")
    
    # Check lambda stability
    lam_values = [r['lambda'] for r in stable_range]
    avg_lam = mean(lam_values)
    std_lam = stdev(lam_values) if len(lam_values) > 1 else 0
    
    print(f"\n   Average λ in stable range: {avg_lam:.6f}")
    print(f"   Std dev: {std_lam:.6f}")
    print(f"   Stability: {'STABLE' if std_lam/avg_lam < 0.3 else 'VARIABLE'}")
    
    # Optimal search range
    print("\n2) Optimal Search Strategy")
    print("   Based on exponential model P(d) ∝ e^(-λd):")
    
    for r in stable_range[:5]:
        nBits = r['nBits']
        lam = r['lambda']
        n_tilde = r['n_tilde']
        
        # Find range covering 80%, 90%, 95% probability mass
        for coverage in [0.80, 0.90, 0.95]:
            d_max = find_optimal_search_range(lam, n_tilde, coverage)
            print(f"   nBits={nBits}: {coverage*100:.0f}% mass in d ∈ [0, {d_max}] (vs 2*ñ={2*n_tilde})")
        
        # Expected speedup
        speedup = calculate_expected_speedup(lam, n_tilde)
        print(f"   → Expected speedup vs uniform: {speedup:.1f}x")
        print()
    
    # Memoryless property test (key validation)
    print("3) Memoryless Property Test (for exponential distribution)")
    print("   If P(d>k+m | d>k) ≈ P(d>m), model is memoryless")
    print("   This would validate the 'first-hit' exponential model")
    print("   NOTE: Requires raw offset data from debug.log to properly test")
    print("   With only summary stats, we can't fully validate this.")
    
    # Actionable insights
    print("\n4) Actionable Mining Optimizations")
    print("   A. Monotonic Scanning:")
    print("      If miner scans S = {W, W-1, W-2, ...} (downward),")
    print("      this is already optimal for the exponential model.")
    print("      AVOID: Alternating (0, +1, -1, +2, -2, ...) - SUBOPTIMAL")
    
    print("\n   B. Priority Sampling:")
    print("      Sample offsets from exponential distribution with λ")
    print(f"      λ ≈ {avg_lam:.6f} (average across stable range)")
    print("      Bias search toward small d (near left boundary)")
    
    print("\n   C. Multi-thread Strategy:")
    print("      BAD: Split range evenly across threads")
    print("      GOOD: All threads start near d=0, stagger outward")
    print("      Reason: Expected reward density is NOT uniform")
    
    print("\n   D. Expected Speedup:")
    speedup_low = calculate_expected_speedup(avg_lam, 16*230)
    speedup_high = calculate_expected_speedup(avg_lam, 16*300)
    print(f"      At nBits=230: ~{speedup_low:.1f}x faster than uniform")
    print(f"      At nBits=300: ~{speedup_high:.1f}x faster than uniform")
    print("      This is 'free' hashpower from smarter search order!")
    
    # Model validation suggestions
    print("\n5) Model Validation (Next Steps)")
    print("   Test 1: Log-histogram of d = ñ + offset")
    print("           If linear on log scale → exponential model holds")
    print("   Test 2: Memoryless property P(d>k+m|d>k) ≈ P(d>m)")
    print("           Requires raw debug.log data (not just summary stats)")
    print("   Test 3: Per-miner comparison")
    print("           If all miners show same λ → protocol-level effect")
    print("           If λ varies → implementation-level (scan order)")
    
    print("\n=== End of Analysis ===")
    print("NOTE: This model assumes first-hit exponential distribution.")
    print("      Validation with raw offset data is STRONGLY recommended.")

if __name__ == '__main__':
    main()
