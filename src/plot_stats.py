#!/usr/bin/env python3
"""
Plot Fact0rn wOffset statistics from debug.log
"""
import sys
import csv
from statistics import *
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

def skew(data):
    m = mean(data)
    n = len(data)
    m3 = sum((x - m)**3 for x in data) / n
    m2 = sum((x - m)**2 for x in data) / n
    return m3 / (m2 ** 1.5)

def kurtosis(data):
    m = mean(data)
    n = len(data)
    m4 = sum((x - m)**4 for x in data) / n
    m2 = sum((x - m)**2 for x in data) / n
    return m4 / (m2 ** 2) - 3  # excess kurtosis

def mad(data):
    m = mean(data)
    return mean([abs(x - m) for x in data])

def medad(data):
    med = median(data)
    return median([abs(x - med) for x in data])

def cv(data):
    return stdev(data) / mean(data) * 100  # as percentage

def stderr(data):
    return stdev(data) / (len(data) ** 0.5)

# Parse debug.log
histo = {}
for line in open(sys.argv[1], "r"):
    if "UpdateTip" in line:
        D = line.split()
        if len(D) > 7:
            bits = D[6].split("=")[1]
            wOffset = int(D[7].split("=")[1])
            if bits in histo:
                histo[bits].append(wOffset)
            else:
                histo[bits] = []

# Extract statistics
bits_sorted = sorted(histo.keys(), key=int)
min_vals, median_vals, mean_vals, mode_vals, stdev_vals, skew_vals, pvar_vals, var_vals, max_vals, count_vals = [], [], [], [], [], [], [], [], [], []
mad_vals, cv_vals, medad_vals, kurt_vals, stderr_vals = [], [], [], [], []

for bits in bits_sorted:
    h = histo[bits]
    min_vals.append(min(h))
    median_vals.append(median(h))
    mean_vals.append(round(mean(h), 2))
    mode_vals.append(mode(h))
    stdev_vals.append(round(stdev(h), 2))
    skew_vals.append(round(skew(h), 2))
    pvar_vals.append(round(pvariance(h), 2))
    var_vals.append(round(variance(h)))
    max_vals.append(max(h))
    count_vals.append(len(h))
    mad_vals.append(round(mad(h), 2))
    cv_vals.append(round(cv(h), 2))
    medad_vals.append(round(medad(h), 2))
    kurt_vals.append(round(kurtosis(h), 2))
    stderr_vals.append(round(stderr(h), 2))

bits_numeric = [int(b) for b in bits_sorted]

# Export statistics to CSV
csv_filename = '../results/wOffset_statistics.csv'
all_wOffsets = []
for bits in bits_sorted:
    all_wOffsets.extend(histo[bits])

with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['nBits', 'count', 'min', 'median', 'mean', 'mode', 'stdev', 'skew', 'kurtosis', 'pvariance', 'variance', 'max', 'mad', 'cv', 'medad', 'stderr'])
    for i, bits in enumerate(bits_sorted):
        writer.writerow([bits, count_vals[i], min_vals[i], median_vals[i], mean_vals[i], mode_vals[i],
                        stdev_vals[i], skew_vals[i], kurt_vals[i], pvar_vals[i], var_vals[i], max_vals[i],
                        mad_vals[i], cv_vals[i], medad_vals[i], stderr_vals[i]])
    writer.writerow(['GROUPED', min(all_wOffsets), median(all_wOffsets), round(mean(all_wOffsets), 2),
                    mode(all_wOffsets), round(stdev(all_wOffsets), 2), round(skew(all_wOffsets), 2),
                    round(pvariance(all_wOffsets), 2), round(variance(all_wOffsets)), max(all_wOffsets)])

print(f"Statistics exported to {csv_filename}")

# Plot 1: Central tendencies
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, min_vals, 'o-', label='min', markersize=3)
plt.plot(bits_numeric, median_vals, 's-', label='median', markersize=3)
plt.plot(bits_numeric, mean_vals, '^-', label='mean', markersize=3)
plt.plot(bits_numeric, mode_vals, 'd-', label='mode', markersize=3)
plt.plot(bits_numeric, max_vals, 'v-', label='max', markersize=3)
plt.xlabel('nBits')
plt.ylabel('wOffset value')
plt.title('Fact0rn wOffset - Central Tendencies')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_central.png', dpi=150)
plt.close()

# Plot 2: Standard deviation
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, stdev_vals, 'o-', color='blue', markersize=3)
plt.xlabel('nBits')
plt.ylabel('Standard Deviation')
plt.title('Fact0rn wOffset - Standard Deviation')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_stdev.png', dpi=150)
plt.close()

# Plot 3: Skewness
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, skew_vals, 'o-', color='green', markersize=3)
plt.xlabel('nBits')
plt.ylabel('Skewness')
plt.title('Fact0rn wOffset - Skewness')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_skew.png', dpi=150)
plt.close()

# Plot 4: Variance (both population and sample)
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, pvar_vals, 'o-', label='pvariance', markersize=3)
plt.plot(bits_numeric, var_vals, 's-', label='variance', markersize=3)
plt.xlabel('nBits')
plt.ylabel('Variance')
plt.title('Fact0rn wOffset - Variance')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_variance.png', dpi=150)
plt.close()

# Plot 5: Sample count per nBits
plt.figure(figsize=(12, 6))
plt.bar(bits_numeric, count_vals, alpha=0.7, color='purple')
plt.xlabel('nBits')
plt.ylabel('Sample Count')
plt.title('Fact0rn wOffset - Sample Count per nBits')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('../results/stats_count.png', dpi=150)
plt.close()

# Plot 6: Mean Absolute Deviation (MAD)
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, mad_vals, 'o-', color='orange', markersize=3)
plt.xlabel('nBits')
plt.ylabel('MAD')
plt.title('Fact0rn wOffset - Mean Absolute Deviation')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_mad.png', dpi=150)
plt.close()

# Plot 7: Coefficient of Variation (CV)
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, cv_vals, 'o-', color='red', markersize=3)
plt.xlabel('nBits')
plt.ylabel('CV (%)')
plt.title('Fact0rn wOffset - Coefficient of Variation')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_cv.png', dpi=150)
plt.close()

# Plot 8: Median Absolute Deviation (MedAD)
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, medad_vals, 'o-', color='cyan', markersize=3)
plt.xlabel('nBits')
plt.ylabel('MedAD')
plt.title('Fact0rn wOffset - Median Absolute Deviation')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_medad.png', dpi=150)
plt.close()

# Plot 9: Kurtosis
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, kurt_vals, 'o-', color='magenta', markersize=3)
plt.xlabel('nBits')
plt.ylabel('Kurtosis')
plt.title('Fact0rn wOffset - Kurtosis (Excess)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_kurtosis.png', dpi=150)
plt.close()

# Plot 10: Standard Error
plt.figure(figsize=(12, 6))
plt.plot(bits_numeric, stderr_vals, 'o-', color='brown', markersize=3)
plt.xlabel('nBits')
plt.ylabel('Standard Error')
plt.title('Fact0rn wOffset - Standard Error of Mean')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_stderr.png', dpi=150)
plt.close()

# Plot 11: All normalized to 0-1 range
plt.figure(figsize=(16, 8))
def normalize(lst):
    mn, mx = min(lst), max(lst)
    return [(x - mn)/(mx - mn) for x in lst]

plt.plot(bits_numeric, normalize(min_vals), 'o-', label='min (norm)', markersize=2)
plt.plot(bits_numeric, normalize(median_vals), 's-', label='median (norm)', markersize=2)
plt.plot(bits_numeric, normalize(mean_vals), '^-', label='mean (norm)', markersize=2)
plt.plot(bits_numeric, normalize(mode_vals), 'd-', label='mode (norm)', markersize=2)
plt.plot(bits_numeric, normalize(stdev_vals), 'o--', label='stdev (norm)', markersize=2)
plt.plot(bits_numeric, normalize(skew_vals), 's--', label='skew (norm)', markersize=2)
plt.plot(bits_numeric, normalize(kurt_vals), 's:', label='kurtosis (norm)', markersize=2)
plt.plot(bits_numeric, normalize(pvar_vals), 'X-', label='pvariance (norm)', markersize=2)
plt.plot(bits_numeric, normalize(var_vals), 'X--', label='variance (norm)', markersize=2)
plt.plot(bits_numeric, normalize(max_vals), 'v-', label='max (norm)', markersize=2)
plt.plot(bits_numeric, normalize(count_vals), 'P:', label='count (norm)', markersize=2)
plt.plot(bits_numeric, normalize(mad_vals), 'o:', label='mad (norm)', markersize=2)
plt.plot(bits_numeric, normalize(cv_vals), '^:', label='cv (norm)', markersize=2)
plt.plot(bits_numeric, normalize(medad_vals), 'd:', label='medad (norm)', markersize=2)
plt.plot(bits_numeric, normalize(stderr_vals), 'h:', label='stderr (norm)', markersize=2)
plt.xlabel('nBits')
plt.ylabel('Normalized Value (0-1)')
plt.title('Fact0rn wOffset - All Statistics (Normalized)')
plt.legend(ncol=3, fontsize=7)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../results/stats_all_normalized.png', dpi=150)
plt.close()

print("  ../results/stats_mad.png")
print("  ../results/stats_cv.png")
print("  ../results/stats_medad.png")
print("  ../results/stats_kurtosis.png")
print("  ../results/stats_stderr.png")

print("  ../results/stats_count.png")

print("Generated plots:")
print("  ../results/stats_central.png")
print("  ../results/stats_stdev.png")
print("  ../results/stats_skew.png")
print("  ../results/stats_variance.png")
print("  ../results/stats_all_normalized.png")
