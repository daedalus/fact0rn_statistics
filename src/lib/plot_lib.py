#!/usr/bin/env python3
"""
Fact0rn Plotting Utilities Library
Used by: plot_stats.py, plot_distribution.py, visualize_density.py, etc.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def setup_plot(figsize=(12, 6), title='', xlabel='', ylabel=''):
    """Create a new plot with common settings"""
    plt.figure(figsize=figsize)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)

def save_plot(output_path, dpi=150):
    """Save current plot to file"""
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi)
    plt.close()

def plot_line(x, y, style='o-', label='', markersize=3, color=None, **kwargs):
    """Plot a line with given style"""
    if color:
        plt.plot(x, y, style, label=label, markersize=markersize, color=color, **kwargs)
    else:
        plt.plot(x, y, style, label=label, markersize=markersize, **kwargs)

def plot_histogram(data, bins=50, alpha=0.7, label=''):
    """Plot histogram"""
    plt.hist(data, bins=bins, alpha=alpha, label=label)

def normalize(values):
    """Normalize a list of values to 0-1 range"""
    if not values:
        return values
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:
        return [0.5] * len(values)
    return [(v - min_val) / (max_val - min_val) for v in values]
