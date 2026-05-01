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

# Import from lib
from lib.stats_lib import skew, kurtosis, mad, medad, cv, stderr, pvariance, variance
from lib.parser_lib import parse_debug_log
from lib.plot_lib import setup_plot, save_plot, plot_line, normalize

# Parse debug.log using library function
histo = parse_debug_log(sys.argv[1])
valid_rows = sum(len(v) for v in histo.values())
sys.stderr.write(f"Total valid rows {valid_rows}\n")

# Extract statistics
bits_sorted = sorted(histo.keys(), key=int)
min_vals, median_vals, mean_vals, mode_vals, stdev_vals, skew_vals, kurt_vals, pvar_vals, var_vals, max_vals, count_vals = [], [], [], [], [], [], [], [], [], [], []
mad_vals, cv_vals, medad_vals, stderr_vals = [], [], [], []

for bits in bits_sorted:
    h = histo[bits]
    min_vals.append(min(h))
    median_vals.append(median(h))
    mean_vals.append(round(mean(h), 2))
    mode_vals.append(mode(h))
    stdev_vals.append(round(stdev(h), 2))
    skew_vals.append(round(skew(h), 2))
    kurt_vals.append(round(kurtosis(h), 2))
    pvar_vals.append(round(pvariance(h), 2))
    var_vals.append(round(variance(h), 2))
    max_vals.append(max(h))
    count_vals.append(len(h))
    mad_vals.append(round(mad(h), 2))
    cv_vals.append(round(cv(h), 2))
    medad_vals.append(round(medad(h), 2))
    stderr_vals.append(round(stderr(h), 2))

bits_numeric = [int(b) for b in bits_sorted]

# Export statistics to CSV
csv_filename = '../results/wOffset_statistics.csv'
all_wOffsets = []
for bits in bits_sorted:
    all_wOffsets.extend(histo[bits])

with open(csv_filename, 'w', newline='') as csvfile:
    C = 0
    writer = csv.writer(csvfile)
    writer.writerow(['nBits', 'count', 'min', 'median', 'mean', 'mode', 'stdev', 'skew', 'kurtosis', 'pvariance', 'variance', 'max', 'mad', 'cv', 'medad', 'stderr'])
    for i, bits in enumerate(bits_sorted):
        C += count_vals[i]
        writer.writerow([bits, count_vals[i], min_vals[i], median_vals[i], mean_vals[i], mode_vals[i],
                          stdev_vals[i], skew_vals[i], kurt_vals[i], pvar_vals[i], var_vals[i], max_vals[i],
                          mad_vals[i], cv_vals[i], medad_vals[i], stderr_vals[i]])

    # GROUPED row: must have exactly 16 fields (matching header)
    writer.writerow([
        'GROUPED',
        sum(count_vals),  # count
        min(all_wOffsets),  # min
        round(median(all_wOffsets), 2),  # median
        round(mean(all_wOffsets), 2),  # mean
        mode(all_wOffsets),  # mode
        round(stdev(all_wOffsets), 2),  # stdev
        round(skew(all_wOffsets), 2),  # skew
        round(kurtosis(all_wOffsets), 2),  # kurtosis
        round(pvariance(all_wOffsets), 2),  # pvariance
        round(variance(all_wOffsets), 2),  # variance
        max(all_wOffsets),  # max
        round(mad(all_wOffsets), 2),  # mad
        round(cv(all_wOffsets), 2),  # cv
        round(medad(all_wOffsets), 2),  # medad
        round(stderr(all_wOffsets), 2)  # stderr
    ])

print(f"Statistics exported to {csv_filename}")

# Plot 1: Central tendencies
setup_plot(figsize=(12, 6), title='Fact0rn wOffset - Central Tendencies', xlabel='nBits', ylabel='wOffset value')
plot_line(bits_numeric, min_vals, 'o-', label='min')
plot_line(bits_numeric, median_vals, 's-', label='median')
plot_line(bits_numeric, mean_vals, '^-', label='mean')
plot_line(bits_numeric, mode_vals, 'd-', label='mode')
plot_line(bits_numeric, max_vals, 'v-', label='max')
plt.legend()
save_plot('../results/stats_central.png')

# Plot 2: Standard deviation
setup_plot(title='Fact0rn wOffset - Standard Deviation', xlabel='nBits', ylabel='Standard Deviation')
plot_line(bits_numeric, stdev_vals, 'o-', color='blue', label='stdev')
plt.legend()
save_plot('../results/stats_stdev.png')

# Plot 3: Skewness
setup_plot(title='Fact0rn wOffset - Skewness', xlabel='nBits', ylabel='Skewness')
plot_line(bits_numeric, skew_vals, 'o-', color='green', label='skew')
plt.legend()
save_plot('../results/stats_skew.png')

# Plot 4: Kurtosis
setup_plot(title='Fact0rn wOffset - Kurtosis (Excess)', xlabel='nBits', ylabel='Kurtosis')
plot_line(bits_numeric, kurt_vals, 'o-', color='magenta', label='kurtosis')
plt.legend()
save_plot('../results/stats_kurtosis.png')

# Plot 5: Variance
setup_plot(title='Fact0rn wOffset - Variance', xlabel='nBits', ylabel='Variance')
plot_line(bits_numeric, pvar_vals, 'o-', label='pvariance')
plot_line(bits_numeric, var_vals, 's-', label='variance')
plt.legend()
save_plot('../results/stats_variance.png')

# Plot 6: Sample count
setup_plot(title='Fact0rn wOffset - Sample Count per nBits', xlabel='nBits', ylabel='Sample Count')
plt.bar(bits_numeric, count_vals, alpha=0.7, color='purple')
plt.legend()
save_plot('../results/stats_count.png')

# Plot 7: MAD
setup_plot(title='Fact0rn wOffset - Mean Absolute Deviation', xlabel='nBits', ylabel='MAD')
plot_line(bits_numeric, mad_vals, 'o-', color='orange', label='mad')
plt.legend()
save_plot('../results/stats_mad.png')

# Plot 8: CV
setup_plot(title='Fact0rn wOffset - Coefficient of Variation', xlabel='nBits', ylabel='CV (%)')
plot_line(bits_numeric, cv_vals, 'o-', color='red', label='cv')
plt.legend()
save_plot('../results/stats_cv.png')

# Plot 9: MedAD
setup_plot(title='Fact0rn wOffset - Median Absolute Deviation', xlabel='nBits', ylabel='MedAD')
plot_line(bits_numeric, medad_vals, 'o-', color='cyan', label='medad')
plt.legend()
save_plot('../results/stats_medad.png')

# Plot 10: Standard Error
setup_plot(title='Fact0rn wOffset - Standard Error of Mean', xlabel='nBits', ylabel='Standard Error')
plot_line(bits_numeric, stderr_vals, 'o-', color='brown', label='stderr')
plt.legend()
save_plot('../results/stats_stderr.png')

# Plot 11: All normalized
setup_plot(figsize=(16, 8), title='Fact0rn wOffset - All Statistics (Normalized)', xlabel='nBits', ylabel='Normalized Value (0-1)')
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

print("Generated plots:")
print("  ../results/stats_central.png")
print("  ../results/stats_stdev.png")
print("  ../results/stats_skew.png")
print("  ../results/stats_kurtosis.png")
print("  ../results/stats_variance.png")
print("  ../results/stats_count.png")
print("  ../results/stats_mad.png")
print("  ../results/stats_cv.png")
print("  ../results/stats_medad.png")
print("  ../results/stats_stderr.png")
print("  ../results/stats_all_normalized.png")
