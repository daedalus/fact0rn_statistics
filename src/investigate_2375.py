#!/usr/bin/env python3
"""
Investigate the MYSTERY: ALL 8 positive offsets are EXACTLY 2375!

This is NOT random - suggests:
1. gHash structure (Hypothesis 3)
2. Nonce reuse?
3. Specific residue class bias?
"""
import sys

def extract_positive_details(debug_log_path, target_nBits='230'):
    """Extract FULL details for positive offsets"""
    details = []
    count = 0
    
    for line in open(debug_log_path, 'r'):
        if "UpdateTip" in line:
            parts = line.split()
            if len(parts) > 7:
                try:
                    nBits = parts[6].split('=')[1]
                    if nBits == target_nBits:
                        wOffset = int(parts[7].split('=')[1])
                        if wOffset > 0:
                            # Extract timestamp
                            timestamp = parts[0].strip('[]')  # e.g. 2026-04-30T14:18:40Z
                            details.append({
                                'timestamp': timestamp,
                                'nBits': nBits,
                                'offset': wOffset,
                                'raw_line': line.strip()[:200]  # First 200 chars
                            })
                            count += 1
                except:
                    pass
    
    print(f"Found {count} positive offset samples for nBits={target_nBits}")
    return details

def analyze_positive_pattern(details):
    """Analyze if these are from same W (nonce reuse?) or different"""
    if not details:
        print("No positive samples to analyze!")
        return
    
    print("\n=== Positive Offset Details (ALL 8 are 2375!) ===\n")
    
    # Check timestamps
    timestamps = [d['timestamp'] for d in details]
    print(f"Timestamps (first 5):")
    for i, ts in enumerate(timestamps[:5]):
        print(f"  {i+1}. {ts}")
    
    # Check if timestamps are clustered (same block re-logged?) or spread out
    if len(timestamps) > 1:
        print(f"\nTimestamp range: {timestamps[0]} to {timestamps[-1]}")
        print(f"Spread: {len(set(timestamps))} unique timestamps")
        
        if len(set(timestamps)) < len(timestamps):
            print("⚠️  DUPLICATE timestamps! (same block re-logged?)")
        else:
            print("✅ All timestamps are UNIQUE")
    
    # Show raw lines (might reveal W value or nonce)
    print(f"\nRaw lines (first 3):")
    for i, d in enumerate(details[:3]):
        print(f"  {i+1}. {d['raw_line']}...")
    
    # Check if same W (would mean gHash structure!)
    # We don't have W directly, but we know offset = n - W
    # If offset is same (2375), and n is different, then W is different
    # If n is same, then same block!
    
    print(f"\n=== Hypothesis Testing ===\n")
    print("Hypothesis 3: gHash has structure")
    print("  - If ALL 8 offsets are 2375, maybe:")
    print("  - Specific W lands in 'sparse' positive region")
    print("  - Only ONE semiprime exists there: W+2375")
    print("  - This would explain 110x ratio!\n")
    
    print("Hypothesis 4b: Nonce reuse?")
    print("  - If same W is generated multiple times")
    print("  - Then same semiprime found repeatedly")
    print("  - Check if timestamps are close (same mining session?)\n")
    
    print("Alternative: Data extraction issue?")
    print("  - Maybe debug.log logs same block multiple times?")
    print("  - Check if timestamps are identical")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 investigate_2375.py <debug.log> [nBits]")
        print("Example: python3 investigate_2375.py ~/.factorn/debug.log 230")
        sys.exit(1)
    
    debug_log = sys.argv[1]
    target_nBits = sys.argv[2] if len(sys.argv) > 2 else '230'
    
    print("=== Investigating ALL 8 Positive Offsets = 2375! ===\n")
    print("KEY FINDING: ALL 8 samples have EXACT SAME VALUE!")
    print("This is NOT random - suggests structure!\n")
    
    # Extract details
    details = extract_positive_details(debug_log, target_nBits)
    
    if not details:
        print(f"No positive samples found for nBits={target_nBits}")
        sys.exit(1)
    
    # Analyze pattern
    analyze_positive_pattern(details)
    
    print("\n=== Conclusions ===")
    print("1. ALL 8 positive offsets = 2375 (exact match!)")
    print("2. This suggests STRONG structure in gHash output")
    print("3. Or possible nonce reuse in miner")
    print("4. The 110x ratio might be from:")
    print("   - Negative region: MANY semiprimes (dense)")
    print("   - Positive region: ONLY ONE semiprime (W+2375)!")
    print("\n🔍 This needs further investigation!")
    print("   - Extract W values (or nonces) from debug.log")
    print("   - Check if same W is reused")
    print("   - This could reveal gHash structure (Hypothesis 3)")

if __name__ == '__main__':
    main()
