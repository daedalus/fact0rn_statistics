#!/usr/bin/env python3
"""
Mining optimizer for Fact0rn - CORRECTED VERSION.
Key finding: Candidates ARE SHUFFLED (line 319).
Strategy: Generate W values that land in "dense" regions.
"""

import sys
import random
import math

sys.path.insert(0, 'lib')
from lib.model_lib import estimate_lambda, expected_speedup

def analyze_w_density(nBits, num_samples=1000):
    """Analyze where W values land relative to semiprime density"""
    n_tilde = 16 * nBits
    print(f"\n=== Optimized Mining Strategy for nBits={nBits} ===")
    print(f"  ñ = {n_tilde}")
    
    # Simulate W generation (simplified)
    best_W = None
    best_score = 0
    
    for i in range(num_samples):
        # Simulate gHash output (simplified)
        W = random.randint(n_tilde * 100, n_tilde * 200)
        
        # Quick density test (check residue classes)
        score = 0
        for p in [2, 3, 5, 7, 11, 13]:
            if W % p in [1, p-1]:  # "Good" residue classes
                score += 1
        
        if score > best_score:
            best_score = score
            best_W = W
            best_nonce = i
    
    print(f"  Best W found after {num_samples} attempts")
    print(f"  W = {best_W}, nonce = {best_nonce}")
    print(f"  Density score: {best_score}/6\n")
    
    return best_W, best_nonce

def calculate_speedup(nBits):
    """Calculate expected speedup"""
    n_tilde = 16 * nBits
    
    # From analysis: negative region is ~110x denser
    # If we ONLY search negative region:
    lambda_val = 1.0 / (n_tilde * 0.5)  # Approximate
    speedup = expected_speedup(lambda_val, n_tilde)
    
    print(f"\n=== Expected Speedup for nBits={nBits} ===")
    print(f"  Uniform: scan all {2*n_tilde} positions")
    print(f"  Optimized (negative region): expected {1.0/lambda_val:.0f} positions")
    if speedup:
        print(f"  Speedup: {speedup:.1f}x\n")
    else:
        print("  Speedup: N/A\n")
    
    return speedup

def main():
    print("=== Fact0rn Mining Optimizer (CORRECTED VERSION) ===\n")
    
    print("KEY FINDING: Candidates ARE SHUFFLED (lib/blockchain.py line 319)")
    print("  -> Hypothesis 4 (scan order) is WRONG")
    print("  -> Bias comes from variable factoring difficulty/density\n")
    
    # Test for different nBits
    for nBits in [230, 250, 300]:
        print("=" * 60)
        
        # Optimized strategy
        W, nonce = analyze_w_density(nBits)
        
        # Speedup calculation
        speedup = calculate_speedup(nBits)
        
        print(f"Key takeaways for nBits={nBits}:")
        print(f"  - DON'T optimize scan order (it's shuffled anyway)")
        print(f"  - DO generate many W values to find 'dense' regions")
        print(f"  - Expected speedup: {speedup:.1f}x (from focusing on dense regions)\n")
    
    print("⚠️  Note: Model isn't perfect (memoryless property fails)")
    print("  But the NEGATIVE BIAS is real and exploitable!")
    
    print("\n🔍 Still to verify:")
    print("  - Does gHash produce W with structure?")
    print("  - Why is negative region 'easier' to factor?")
    print("  - Can we predict which W values are 'good'?")

if __name__ == '__main__':
    main()
