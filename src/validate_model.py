#!/usr/bin/env python3
"""
Extract raw wOffset values from debug.log to validate the exponential model.
Also creates log-histogram to test if P(d) ∝ e^(-λd) (should be linear on log scale).
"""
import sys
import math
from collections import defaultdict

def extract_offsets(debug_log_path):
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
                    data[nBits].append(wOffset)
                    count += 1
                except:
                    pass
    
    print(f"Extracted {count} wOffset values across {len(data)} nBits levels")
    return data

def compute_d_values(nBits, offsets):
    """Convert offsets to d = ñ + offset = 16*nBits + offset"""
    n_tilde = 16 * int(nBits)
    d_values = [n_tilde + offset for offset in offsets]
    return d_values

def create_log_histogram(d_values, nBits, num_bins=50):
    """Create histogram and check if log(frequency) is linear in d"""
    if not d_values:
        return None
    
    n_tilde = 16 * int(nBits)
    max_d = max(d_values)
    bin_width = (max_d - 0) / num_bins if max_d > 0 else 1
    
    bins = [0] * num_bins
    bin_edges = [i * bin_width for i in range(num_bins + 1)]
    
    for d in d_values:
        if d >= 0 and d < max_d:
            bin_idx = int(d / bin_width)
            if bin_idx >= num_bins:
                bin_idx = num_bins - 1
            bins[bin_idx] += 1
    
    # Convert to log scale (add small constant to avoid log(0))
    log_bins = []
    for i, count in enumerate(bins):
        if count > 0:
            log_bins.append((bin_edges[i], math.log(count)))
        else:
            log_bins.append((bin_edges[i], None))  # None for log(0)
    
    return log_bins, bin_edges, bins

def fit_exponential_mle(d_values):
    """Maximum Likelihood Estimation for exponential distribution"""
    if not d_values:
        return None
    
    # MLE for exponential: λ = 1 / mean(d)
    mean_d = sum(d_values) / len(d_values)
    if mean_d <= 0:
        return None
    lam = 1.0 / mean_d
    return lam

def test_memoryless_property(d_values, thresholds=[100, 500, 1000]):
    """
    Test memoryless property: P(d > k+m | d > k) ≈ P(d > m)
    For exponential: P(d > x) = e^(-λx)
    """
    if not d_values:
        return {}
    
    lam = fit_exponential_mle(d_values)
    if not lam:
        return {}
    
    results = {}
    for k in thresholds:
        for m in [100, 500, 1000]:
            # Empirical: P(d > k+m | d > k)
            d_greater_k = [d for d in d_values if d > k]
            if not d_greater_k:
                continue
            d_greater_km = [d for d in d_greater_k if d > k + m]
            empirical = len(d_greater_km) / len(d_greater_k)
            
            # Theoretical: P(d > m) = e^(-λm)
            theoretical = math.exp(-lam * m)
            
            results[(k, m)] = {
                'empirical': empirical,
                'theoretical': theoretical,
                'error': abs(empirical - theoretical)
            }
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_model.py <debug.log> [nBits_to_analyze]")
        print("Example: python3 validate_model.py ~/.factorn/debug.log 230")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=== Fact0rn wOffset Raw Data Extraction ===\n")
    
    # Extract data
    data = extract_offsets(debug_log)
    
    if target_nBits:
        # Analyze specific nBits
        if target_nBits in data:
            offsets = data[target_nBits]
            nBits = int(target_nBits)
            n_tilde = 16 * nBits
            d_values = compute_d_values(target_nBits, offsets)
            
            print(f"\nnBits={nBits} Analysis:")
            print(f"  ñ = {n_tilde}")
            print(f"  Sample count: {len(offsets)}")
            print(f"  offset range: [{min(offsets)}, {max(offsets)}]")
            print(f"  d range: [{min(d_values)}, {max(d_values)}]")
            
            # Fit exponential
            lam = fit_exponential_mle(d_values)
            if lam:
                print(f"\n  MLE λ = {lam:.6f}")
                print(f"  E[d] = 1/λ = {1.0/lam:.1f}")
                print(f"  Compare to ñ + mean(offset) = {n_tilde + sum(offsets)/len(offsets):.1f}")
            
            # Log histogram
            log_bins, bin_edges, bins = create_log_histogram(d_values, target_nBits)
            if log_bins:
                print(f"\n  Log-Histogram (check linearity for exponential):")
                print(f"  {'d':>10} | {'count':>8} | {'log(count)':>12}")
                print(f"  " + "-" * 35)
                for i, (d, log_count) in enumerate(log_bins[:10]):  # First 10 bins
                    if log_count is not None:
                        print(f"  {d:>10.1f} | {bins[i]:>8} | {log_count:>12.4f}")
                    else:
                        print(f"  {d:>10.1f} | {bins[i]:>8} | {'-inf':>12}")
            
            # Memoryless test
            print(f"\n  Memoryless Property Test (exponential validation):")
            results = test_memoryless_property(d_values)
            if results:
                print(f"  {'k':>6} | {'m':>6} | {'empirical':>12} | {'theoretical':>12} | {'error':>10}")
                print(f"  " + "-" * 55)
                for (k, m), res in sorted(results.items())[:5]:
                    print(f"  {k:>6} | {m:>6} | {res['empirical']:>12.4f} | {res['theoretical']:>12.4f} | {res['error']:>10.4f}")
                
                avg_error = sum(r['error'] for r in results.values()) / len(results)
                print(f"\n  Average error: {avg_error:.4f}")
                if avg_error < 0.05:
                    print("  ✅ Memoryless property HOLDS (exponential model validated)")
                else:
                    print("  ⚠️  Memoryless property questionable (model may be wrong)")
        else:
            print(f"nBits={target_nBits} not found in data")
    else:
        # Summary across all nBits
        print(f"\nSummary across all nBits levels:")
        print(f"  {'nBits':>6} | {'count':>6} | {'λ (MLE)':>10} | {'E[d]':>10}")
        print(f"  " + "-" * 45)
        for nBits in sorted(data.keys(), key=int)[:10]:  # First 10
            offsets = data[nBits]
            d_values = compute_d_values(nBits, offsets)
            lam = fit_exponential_mle(d_values)
            if lam:
                print(f"  {nBits:>6} | {len(offsets):>6} | {lam:>10.6f} | {1.0/lam:>10.1f}")
        
        print(f"\n  (Use specific nBits argument to see detailed analysis)")

if __name__ == '__main__':
    main()
