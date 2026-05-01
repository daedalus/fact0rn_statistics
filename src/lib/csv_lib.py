#!/usr/bin/env python3
"""
Fact0rn CSV Library - Common CSV loading functions
Used by: model_offset.py, analyze_bias_source.py, etc.
"""

import csv


def load_csv(csv_path, skip_grouped=True):
    """
    Load wOffset statistics from CSV file.
    
    Args:
        csv_path: Path to the CSV file
        skip_grouped: If True, skip the GROUPED row (default: True)
    
    Returns:
        List of dicts with all CSV fields as appropriate types
    """
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if skip_grouped and row.get('nBits') == 'GROUPED':
                continue
            data.append({
                'nBits': int(row['nBits']),
                'count': int(row['count']),
                'min': int(row['min']),
                'median': float(row['median']),
                'mean': float(row['mean']),
                'mode': int(row['mode']),
                'stdev': float(row['stdev']),
                'skew': float(row['skew']),
                'kurtosis': float(row['kurtosis']),
                'pvariance': float(row['pvariance']),
                'variance': float(row['variance']),
                'max': int(row['max']),
                'mad': float(row['mad']),
                'cv': float(row['cv']),
                'medad': float(row['medad']),
                'stderr': float(row['stderr']),
            })
    return data


def load_csv_fields(csv_path, fields, skip_grouped=True):
    """
    Load specific fields from wOffset statistics CSV file.
    
    Args:
        csv_path: Path to the CSV file
        fields: List of field names to load (e.g., ['nBits', 'mean', 'skew'])
        skip_grouped: If True, skip the GROUPED row (default: True)
    
    Returns:
        List of dicts with only the requested fields
    """
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if skip_grouped and row.get('nBits') == 'GROUPED':
                continue
            item = {}
            for field in fields:
                if field in ['nBits', 'count', 'min', 'max', 'mode']:
                    item[field] = int(row[field])
                else:
                    item[field] = float(row[field])
            data.append(item)
    return data
