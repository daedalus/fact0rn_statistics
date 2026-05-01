# Gnuplot script to plot Fact0rn wOffset statistics
set terminal png size 1200,800 enhanced font "DejaVu Sans,10"
set datafile separator ","
set datafile missing "NaN"

# Plot 1: Central tendencies (min, median, mean, mode, max)
set output '../results/stats_central.png'
set title "Fact0rn wOffset - Central Tendencies by nBits"
set xlabel "nBits"
set ylabel "wOffset value"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:3 with linespoints title 'min', \
      '' skip 1 using 1:4 with linespoints title 'median', \
      '' skip 1 using 1:5 with linespoints title 'mean', \
      '' skip 1 using 1:6 with linespoints title 'mode', \
      '' skip 1 using 1:12 with linespoints title 'max'

# Plot 2: Standard deviation
set output '../results/stats_stdev.png'
set title "Fact0rn wOffset - Standard Deviation by nBits"
set xlabel "nBits"
set ylabel "Standard Deviation"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:7 with linespoints title 'stdev' lc rgb 'blue'

# Plot 3: Skewness
set output '../results/stats_skew.png'
set title "Fact0rn wOffset - Skewness by nBits"
set xlabel "nBits"
set ylabel "Skewness"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:8 with linespoints title 'skew' lc rgb 'green'

# Plot 4: Kurtosis
set output '../results/stats_kurtosis.png'
set title "Fact0rn wOffset - Kurtosis (Excess) by nBits"
set xlabel "nBits"
set ylabel "Kurtosis"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:9 with linespoints title 'kurtosis' lc rgb 'magenta'

# Plot 5: Variance and Population Variance
set output '../results/stats_variance.png'
set title "Fact0rn wOffset - Variance by nBits"
set xlabel "nBits"
set ylabel "Variance"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:10 with linespoints title 'pvariance', \
      '' skip 1 using 1:11 with linespoints title 'variance'

# Plot 6: Sample Count
set output '../results/stats_count.png'
set title "Fact0rn wOffset - Sample Count per nBits"
set xlabel "nBits"
set ylabel "Sample Count"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:2 with boxes title 'count' lc rgb 'purple'

# Plot 7: Mean Absolute Deviation (MAD)
set output '../results/stats_mad.png'
set title "Fact0rn wOffset - Mean Absolute Deviation by nBits"
set xlabel "nBits"
set ylabel "MAD"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:13 with linespoints title 'mad' lc rgb 'orange'

# Plot 8: Coefficient of Variation (CV)
set output '../results/stats_cv.png'
set title "Fact0rn wOffset - Coefficient of Variation by nBits"
set xlabel "nBits"
set ylabel "CV (%)"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:14 with linespoints title 'cv' lc rgb 'red'

# Plot 9: Median Absolute Deviation (MedAD)
set output '../results/stats_medad.png'
set title "Fact0rn wOffset - Median Absolute Deviation by nBits"
set xlabel "nBits"
set ylabel "MedAD"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:15 with linespoints title 'medad' lc rgb 'cyan'

# Plot 10: Standard Error
set output '../results/stats_stderr.png'
set title "Fact0rn wOffset - Standard Error of Mean by nBits"
set xlabel "nBits"
set ylabel "Standard Error"
set grid
plot '../results/wOffset_statistics.csv' skip 1 using 1:16 with linespoints title 'stderr' lc rgb 'brown'

# Plot 11: Combined view (normalized)
set output '../results/stats_all_normalized.png'
set title "Fact0rn wOffset - All Statistics (Normalized)"
set xlabel "nBits"
set ylabel "Normalized Value"
set grid
set key outside right
plot '../results/wOffset_statistics.csv' skip 1 using 1:($3/5000) with linespoints title 'min/5000', \
      '' skip 1 using 1:($4/5000) with linespoints title 'median/5000', \
      '' skip 1 using 1:($5/5000) with linespoints title 'mean/5000', \
      '' skip 1 using 1:($6/5000) with linespoints title 'mode/5000', \
      '' skip 1 using 1:($7/5000) with linespoints title 'stdev/5000', \
      '' skip 1 using 1:($8/5000) with linespoints title 'skew/5000', \
      '' skip 1 using 1:($9/5000) with linespoints title 'kurtosis/5000', \
      '' skip 1 using 1:($10/5000) with linespoints title 'pvariance/5000', \
      '' skip 1 using 1:($11/5000) with linespoints title 'variance/5000', \
      '' skip 1 using 1:($12/5000) with linespoints title 'max/5000', \
      '' skip 1 using 1:($13/5000) with linespoints title 'mad/5000', \
      '' skip 1 using 1:($14/5000) with linespoints title 'cv/5000', \
      '' skip 1 using 1:($15/5000) with linespoints title 'medad/5000', \
      '' skip 1 using 1:($16/5000) with linespoints title 'stderr/5000', \
      '' skip 1 using 1:($2/5000) with linespoints title 'count/5000'

print "Generated: stats_central.png, stats_stdev.png, stats_skew.png, stats_kurtosis.png, stats_variance.png, stats_count.png, stats_mad.png, stats_cv.png, stats_medad.png, stats_stderr.png, stats_all_normalized.png"
