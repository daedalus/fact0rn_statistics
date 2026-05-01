#!/usr/bin/env python3
"""
Fact0rn Debug Log Parser Library
Used by: parser.py, plot_stats.py, validate_model.py, investigate_why.py, etc.
"""

def parse_debug_log(debug_log_path, target_nBits=None):
    """
    Parse Fact0rn debug.log for UpdateTip entries.
    Returns dict: {nBits: [wOffset1, wOffset2, ...]}
    If target_nBits is set, only return that nBits level.
    """
    histo = {}
    K = set()  # Track unique (Hash, height) pairs to avoid double-counting
    
    for line in open(debug_log_path, 'r'):
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
    for line in open(debug_log_path, 'r'):
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
    for line in open(debug_log_path, 'r'):
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

