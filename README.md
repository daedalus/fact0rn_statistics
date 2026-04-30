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

## Data Insights

Analysis of the Fact0rn whitepaper and `wOffset_statistics.csv` reveals key insights about the blockchain's Proof of Work mechanism.

### 1. Constraint Boundary Verification

**Whitepaper:** `|wOffset| ≤ 16 · nBits`

**Data:** The minimum wOffset = **exactly -16 · nBits** for all difficulty levels:
- nBits=230: min=-3680 ✓ (16×230=3680)
- nBits=250: min=-4000 ✓ (16×250=4000)
- nBits=300: min=-4800 ✓ (16×300=4800)

**Insight:** Miners consistently operate at the **exact constraint boundary**, suggesting the search space `S = {n ∈ ℕ | |W - n| < 16·nBits}` is being fully utilized.

---

### 2. Phase Transition at nBits ≈ 250

| nBits Range | wOffset Mean | Distribution |
|--------------|---------------|--------------|
| 230-248 | -3500 to -3000 | All negative (gHash < semiprime) |
| 249-253 | -2900 to -17 | Transition zone |
| 254+ | -700 to +140 | Centered around 0 |

**Insight:** Below nBits=250, gHash output **consistently underestimates** the semiprime. Above 250, gHash is roughly **centered on the target**. This suggests a fundamental change in the gHash-to-semiprime relationship.

---

### 3. Heavy-Tailed Distributions at Low Difficulty

| nBits | Kurtosis | Interpretation |
|--------|----------|------------------|
| 230 | 94.11 | Extreme outliers (normal=0) |
| 240 | 5.26 | Heavy tails |
| 260 | 0.17 | More normal |
| 300 | 0.04 | Near-normal |

**Insight:** At low difficulties, the wOffset distribution has **very heavy tails** (kurtosis >> 0), meaning extreme values are common. This suggests the factoring algorithm (ECM) finds widely scattered semiprimes within the search interval.

---

### 4. Optimal Mining Zone: nBits 250-260

- **Lowest absolute wOffset**: nBits=252 has mean=-16.9 (almost 0!)
- **Reward efficiency**: Whitepaper Figure 6 shows rewards double every ~64 bits
- **Sweet spot**: Around nBits=252, miners find semiprimes **closest to gHash output**

**Insight:** This is the "optimal" difficulty where gHash and factoring are best aligned.

---

### 5. Block Time Stability

- **Constant sample count**: ~671 blocks per nBits (230-340 range)
- **Design target**: 30 minutes per block (whitepaper Section 4)
- **Total blocks analyzed**: ~171 difficulty levels × 671 ≈ 114,741 blocks

**Insight:** The system maintains **consistent block production** across difficulty adjustments, validating the difficulty retargeting mechanism.

---

### 6. Skewness Patterns

| nBits | Skewness | Interpretation |
|--------|----------|------------------|
| 230-240 | +2 to +9 | Left tail (negative outliers) |
| 250-260 | 0 to +0.3 | Nearly symmetric |
| 300+ | -0.1 to +0.2 | Symmetric |

**Insight:** At low difficulties, the distribution is **right-skewed** (mean < median, long left tail), indicating miners often find semiprimes far below gHash. At higher difficulties, the distribution becomes symmetric.

---

### 7. Coefficient of Variation (CV) Explosion

| nBits | CV (%) | Interpretation |
|--------|--------|------------------|
| 230 | -16% | Low relative spread |
| 250 | -112% | High relative spread |
| 300 | 1000%+ | Extreme relative spread |

**Insight:** As difficulty increases, the **relative variability explodes** because the mean approaches 0 while stdev remains ~2500-2800. This is an artifact of division by small means.

---

### 8. Mining Strategy Implications

**Whitepaper:** *"gHash produces a pseudo-random integer... miners can expect to find about 200 semiprimes"* within the search interval.

**Data confirms:**
- Search interval width = 2 × 16·nBits = 32·nBits
- For nBits=230: interval = 7360, found 886 valid blocks
- ~12% of the interval produces valid blocks

**Insight:** The gHash design successfully creates a **dense enough search space** where miners reliably find ~200-800 valid semiprimes per gHash output.

---

### Summary of Key Findings

1. ✅ **Constraint respected**: Miners operate exactly at `|wOffset| ≤ 16·nBits` boundary
2. 🔄 **Phase transition**: nBits≈250 marks where gHash alignment with semiprimes shifts
3. 📊 **Heavy tails at low difficulty**: ECM factoring finds extreme values frequently
4. ⚖️ **Stable block times**: ~671 blocks per difficulty level (30min target)
5. 🎯 **Sweet spot**: nBits 250-260 has wOffset closest to 0 (optimal mining)
