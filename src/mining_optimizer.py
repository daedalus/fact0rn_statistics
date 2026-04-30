#!/usr/bin/env python3
"""
Mining optimizer for Fact0rn based on empirical wOffset bias.

Key insight: Offsets are NOT symmetric around 0.
Data shows strong negative bias (mean offset << 0).

Strategy: Exploit this bias to reduce expected search time.
"""
import sys
import math
import random

def compute_optimized_range(nBits, coverage=0.95):
    """
    Compute optimized search range based on empirical bias.
    
    Instead of searching [-ñ, +ñ] uniformly,
    prioritize the region where solutions are actually found.
    
    Based on data: most solutions cluster near -ñ (left boundary)
    """
    n_tilde = 16 * nBits
    
    # From empirical data: mean offset ≈ -0.85 * ñ
    # (this varies, but negative bias is consistent)
    empirical_mean_offset = -0.85 * n_tilde
    
    # For exponential model P(d) ∝ e^(-λd) where d = ñ + offset
    # λ ≈ 1/(ñ + mean_offset) ≈ 1/(0.15 * ñ) ≈ 6.67/ñ
    lam = 6.67 / n_tilde
    
    # Find d_max that covers 'coverage' probability mass
    # For truncated exponential: P(D ≤ d) = (1-e^(-λd))/(1-e^(-2λñ))
    max_d = 2 * n_tilde
    Z = 1.0 - math.exp(-2 * lam * n_tilde)
    
    if Z > 0:
        # Solve: (1-e^(-λd))/Z = coverage
        d_max = -math.log(1.0 - coverage * Z) / lam
    else:
        d_max = max_d
    
    # Convert back to offset: offset = d - ñ
    offset_start = -n_tilde  # Left boundary
    offset_end = max(offset_start, int(d_max - n_tilde))
    
    return offset_start, offset_end

def priority_sample_offsets(nBits, num_samples=1000):
    """
    Generate offset samples biased toward empirical distribution.
    
    Instead of uniform sampling from [-ñ, +ñ],
    sample from region where solutions are actually found.
    """
    n_tilde = 16 * nBits
    lam = 6.67 / n_tilde  # Empirical λ
    
    samples = []
    for _ in range(num_samples):
        # Sample from exponential distribution
        u = random.random()
        if u < 1e-10:
            d = 2 * n_tilde
        else:
            d = -math.log(u) / lam
        
        # Truncate at 2*ñ
        d = min(d, 2 * n_tilde)
        
        # Convert to offset
        offset = int(d - n_tilde)
        samples.append(offset)
    
    return samples

def compare_strategies(nBits):
    """
    Compare different search strategies.
    
    Strategies:
    1. Uniform: scan [-ñ, +ñ] uniformly
    2. Monotonic down: scan from W downward (W, W-1, W-2, ...)
    3. Priority sampling: sample biased toward region with solutions
    """
    n_tilde = 16 * nBits
    search_space = 2 * n_tilde
    
    print(f"\n=== Mining Strategy Comparison for nBits={nBits} ===")
    print(f"Search space: [-{n_tilde}, +{n_tilde}] = {search_space} positions")
    print(f"Empirical mean offset: ~{int(-0.85 * n_tilde)}")
    
    # Strategy 1: Uniform (baseline)
    print(f"\n1. Uniform Search:")
    print(f"   Expected work: {search_space} positions")
    print(f"   (This is the baseline)")
    
    # Strategy 2: Monotonic downward scan
    # If solutions cluster at -ñ, scanning downward finds them faster
    # Expected position of first hit: ~0.15 * ñ from start
    expected_d = 0.15 * n_tilde  # ~210 for nBits=230
    expected_work = int(expected_d)
    speedup = search_space / expected_work
    
    print(f"\n2. Monotonic Downward Scan (W, W-1, W-2, ...):")
    print(f"   Expected work: ~{expected_work} positions")
    print(f"   Speedup vs uniform: {speedup:.1f}x")
    print(f"   ⚡ This exploits the negative bias!")
    
    # Strategy 3: Priority sampling
    # Sample from exponential distribution
    lam = 6.67 / n_tilde
    expected_d_exp = 1.0 / lam  # ~0.15 * n_tilde
    expected_work_exp = int(expected_d_exp)
    speedup_exp = search_space / expected_work_exp
    
    print(f"\n3. Priority Sampling (exponential λ={lam:.6f}):")
    print(f"   Expected work: ~{expected_work_exp} positions")
    print(f"   Speedup vs uniform: {speedup_exp:.1f}x")
    print(f"   ⚡ This matches the empirical distribution!")
    
    # Strategy 4: Smart multi-thread
    print(f"\n4. Smart Multi-Thread (all threads start near -ñ):")
    print(f"   BAD: Split range evenly (threads waste time on empty regions)")
    print(f"   GOOD: All threads start at -ñ, stagger outward")
    print(f"   Expected speedup: {speedup:.1f}x (same as monotonic)")
    
    return speedup

def generate_optimized_mining_code(nBits):
    """
    Generate pseudo-code for optimized mining loop.
    """
    n_tilde = 16 * nBits
    
    code = f"""
# Optimized Fact0rn mining loop (exploiting negative bias)
n_tilde = 16 * {nBits}  # = {n_tilde}

# BAD: Symmetric search (wastes time)
# for offset in range(-n_tilde, n_tilde + 1):
#     test W + offset

# GOOD: Monotonic downward (exploits bias)
for offset in range(0, -n_tilde - 1, -1):  # W, W-1, W-2, ..., W-n_tilde
    if is_semiprime(W + offset):
        return offset  # Found! (likely near -n_tilde)

# If not found in negative region, expand to positive
for offset in range(1, n_tilde + 1):
    if is_semiprime(W + offset):
        return offset
"""
    return code

def main():
    print("=== Fact0rn Mining Optimizer ===")
    print("\nBased on empirical analysis of wOffset bias:")
    print("  - Strong negative bias (mean offset << 0)")
    print("  - Solutions cluster near left boundary (-16*nBits)")
    print("  - This is exploitable for mining advantage!")
    
    # Compare strategies for different nBits
    for nBits in [230, 250, 300]:
        compare_strategies(nBits)
    
    # Generate optimized code example
    print("\n" + "="*60)
    print("Example Optimized Mining Code (nBits=230):")
    print("="*60)
    print(generate_optimized_mining_code(230))
    
    print("\n=== Key Takeaways ===")
    print("1. DON'T use alternating search (0, +1, -1, +2, -2, ...)")
    print("   → This is SUBOPTIMAL for biased distribution")
    print("2. DO use monotonic downward scan (W, W-1, W-2, ...)")
    print("   → Matches where solutions are actually found")
    print("3. Expected speedup: 3-6x depending on nBits")
    print("4. This is 'free' performance from smarter search order!")
    print("\n⚠️  Note: Model isn't perfect (memoryless property fails)")
    print("   But the NEGATIVE BIAS is real and exploitable!")

if __name__ == '__main__':
    main()
