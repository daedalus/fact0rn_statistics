"""
Parsing the Fact0rn project statistics of the ~/.factorn/debug.log
we create an histogram arround nBits as key and wOffset as a list
We operate with the wOffset list extracting it's statistics

messages like: 2026-04-30T14:18:40Z UpdateTip: new best=c0131e22a4856afdd9705a139da863e8f6d80435da64f896e29a531f1a3f6868 height=1 version=0x20000000 nBits=230 wOffset=-2672"
"""

import sys
from statistics import mean, median, mode, stdev
from lib.stats_lib import skew, kurtosis, mad, medad, cv, stderr, pvariance, variance

def parse_debug_log(debug_log_path, target_nBits=None):
    """
    Parse Fact0rn debug.log for UpdateTip entries.
    Returns dict: {nBits: [wOffset1, wOffset2, ...]}
    If target_nBits is set, only return that nBits level.
    """
    histo = {}
    K = set()  # Track unique (Hash, height) pairs to avoid double-counting
    
    for line in open(debug_log_path, "r"):
        if "UpdateTip" in line:
            D = line.split()
            if len(D) > 7:
                bits = int(D[6].split("=")[1])
                wOffset = int(D[7].split("=")[1])
                
                # Avoid double-counting
                key = (D[3].split("=")[1], D[4].split("=")[1])
                if key in K:
                    continue
                K.add(key)
                
                if bits not in histo:
                    histo[bits] = []
                histo[bits].append(wOffset)
    
    if target_nBits is not None:
        if target_nBits in histo:
            return {target_nBits: histo[target_nBits]}
        return {}
    
    return histo

def extract_all_offsets(debug_log_path, target_nBits='230'):
    """Extract ALL offsets from debug.log for a specific nBits"""
    offsets = []
    for line in open(debug_log_path, "r"):
        if "UpdateTip" in line:
            D = line.split()
            if len(D) > 7:
                bits = int(D[6].split("=")[1])
                wOffset = int(D[7].split("=")[1])
                if bits == int(target_nBits):
                    offsets.append(wOffset)
    return offsets

def extract_w_values(debug_log_path, target_nBits=None):
    """Extract W values and offsets from debug.log (used by validate_new_hypothesis.py)"""
    data = {}
    for line in open(debug_log_path, "r"):
        if "UpdateTip" in line:
            D = line.split()
            if len(D) > 7:
                bits = D[6].split("=")[1]
                wOffset = int(D[7].split("=")[1])
                if bits not in data:
                    data[bits] = []
                data[bits].append(wOffset)
    
    if target_nBits is not None:
        if target_nBits in data:
            return {target_nBits: data[target_nBits]}
        return {}
    return data


def main():
    histo = parse_debug_log(sys.argv[1])
    valid_rows = sum(len(v) for v in histo.values())
    sys.stderr.write(f"Total valid rows {valid_rows}\n")
    
    print("For each nBits calculate their wOffset stats:")
    print("nBits count min median mean mode stdev skew kurtosis pvariance variance max mad cv medad stderr")
    for bits in histo:
        h = histo[bits]
        print(bits, len(h), min(h), median(h), round(mean(h),2), mode(h), round(stdev(h),2), round(skew(h),2), round(kurtosis(h),2), round(pvariance(h),2), round(variance(h)), max(h), round(mad(h),2), round(cv(h),2), round(medad(h),2), round(stderr(h),2))
    
    print("grouped nBits stats:")
    print("min median mean mode stdev skew kurtosis pvariance variance max mad cv medad stderr")
    h = []
    for bits in histo:
        h += histo[bits]
    print(min(h), median(h), round(mean(h),2), mode(h), round(stdev(h),2), round(skew(h),2), round(kurtosis(h),2), round(pvariance(h),2), round(variance(h)), max(h), round(mad(h),2), round(cv(h),2), round(medad(h),2), round(stderr(h),2))


if __name__ == '__main__':
    main()
