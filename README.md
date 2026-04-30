# Fact0rn wOffset Statistics

## Overview
Parses Fact0rn's `~/.factorn/debug.log` to extract `nBits` and `wOffset` values from `UpdateTip` log entries, computes statistical metrics per `nBits` group, and generates visualizations.

## Project Structure
```
fact0rn_statistics/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/                  # Source scripts
│   ├── parser.py         # Extracts statistics from debug.log
│   ├── plot_stats.py     # Generates matplotlib plots and CSV export
│   └── plot_stats.gp     # Gnuplot script (alternative plotting)
└── results/              # Generated outputs
    ├── wOffset_statistics.csv
    ├── stats_central.png
    ├── stats_stdev.png
    ├── stats_skew.png
    ├── stats_kurtosis.png
    ├── stats_variance.png
    ├── stats_count.png
    ├── stats_mad.png
    ├── stats_cv.png
    ├── stats_medad.png
    ├── stats_stderr.png
    └── stats_all_normalized.png
```

## Prerequisites
- Python 3
- `matplotlib` (install via `uv pip install -r requirements.txt`)
- Gnuplot (optional, for alternative plotting)
- Fact0rn debug log at `~/.factorn/debug.log`

## Usage

### Option 1: Python/Matplotlib (Recommended)
```bash
cd src
python3 plot_stats.py ~/.factorn/debug.log
```
This generates PNG plots in `../results/` and exports statistics to `../results/wOffset_statistics.csv`.

### Option 2: Gnuplot
```bash
cd src
python3 parser.py ~/.factorn/debug.log > ../results/stats_data.txt
gnuplot plot_stats.gp
```

### Option 3: Parser Only
```bash
cd src
python3 parser.py ~/.factorn/debug.log
```

## Generated Outputs

### Central Tendencies
![Central Tendencies](results/stats_central.png)
*Min, median, mean, mode, and max wOffset values per nBits*

### Standard Deviation
![Standard Deviation](results/stats_stdev.png)
*Standard deviation of wOffset distribution per nBits*

### Skewness
![Skewness](results/stats_skew.png)
*Skewness of wOffset distribution per nBits*

### Kurtosis
![Kurtosis](results/stats_kurtosis.png)
*Excess kurtosis of wOffset distribution per nBits (normal=0)*

### Variance
![Variance](results/stats_variance.png)
*Population variance (pvariance) and sample variance per nBits*

### Sample Count
![Sample Count](results/stats_count.png)
*Number of wOffset samples per nBits value*

### Mean Absolute Deviation (MAD)
![MAD](results/stats_mad.png)
*Mean absolute deviation from mean per nBits*

### Coefficient of Variation (CV)
![CV](results/stats_cv.png)
*Coefficient of variation (stdev/mean %) per nBits*

### Median Absolute Deviation (MedAD)
![MedAD](results/stats_medad.png)
*Median absolute deviation from median per nBits*

### Standard Error
![Standard Error](results/stats_stderr.png)
*Standard error of the mean per nBits*

### Normalized Statistics
![Normalized Statistics](results/stats_all_normalized.png)
*All statistics normalized to 0-1 range for direct comparison*

### Sample Count
![Sample Count](results/stats_count.png)
*Number of wOffset samples per nBits value*

## CSV Export
The script exports all computed statistics to `results/wOffset_statistics.csv`:

| Column | Description |
|--------|-------------|
| `nBits` | The nBits value (difficulty target) |
| `count` | Number of wOffset samples |
| `min` | Minimum wOffset |
| `median` | Median wOffset |
| `mean` | Mean wOffset |
| `mode` | Mode wOffset |
| `stdev` | Standard deviation |
| `skew` | Skewness (measure of asymmetry) |
| `kurtosis` | Kurtosis - excess (tail heaviness, normal=0) |
| `pvariance` | Population variance |
| `variance` | Sample variance |
| `max` | Maximum wOffset |
| `mad` | Mean Absolute Deviation |
| `cv` | Coefficient of Variation (%) |
| `medad` | Median Absolute Deviation |
| `stderr` | Standard Error of the Mean |

The last row contains `GROUPED` statistics across all nBits values.

## Statistics Computed
For each unique `nBits` value, the following metrics are calculated:

| Metric | Description |
|--------|-------------|
| `count` | Number of wOffset samples |
| `min` | Minimum wOffset |
| `median` | Median wOffset |
| `mean` | Mean wOffset |
| `mode` | Mode wOffset |
| `stdev` | Standard deviation |
| `skew` | Skewness (measure of asymmetry) |
| `kurtosis` | Kurtosis - excess (tail heaviness, normal=0) |
| `pvariance` | Population variance |
| `variance` | Sample variance |
| `max` | Maximum wOffset |
| `mad` | Mean Absolute Deviation |
| `cv` | Coefficient of Variation (stdev/mean × 100%) |
| `medad` | Median Absolute Deviation |
| `stderr` | Standard Error of the Mean (stdev/√n) |

## Sample Output
```
For each nBits calculate their wOffset stats:
nBits min median mean mode stdev skew pvariance variance max
230 -3680 -3584.0 -3476.05 -3665 556.26 9.3 309078.95 309428 2375
231 -3696 -3479 -3361.8 -3653 359.68 2.05 129175.75 129369 -961
...
```
