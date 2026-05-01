#!/bin/bash
# Fact0rn wOffset Statistics - Full Pipeline
# Runs all analysis scripts and logs output to pipeline.log

LOG_FILE="pipeline.log"
DEBUG_LOG="${HOME}/.factorn/debug.log"
CSV_FILE="results/wOffset_statistics.csv"

# Change to script directory
cd "$(dirname "$0")"

# Create results directory if it doesn't exist
mkdir -p results

echo "=== Fact0rn wOffset Statistics Pipeline ===" | tee "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Step 1: parser.py (outputs to stdout, redirect to file)
echo "=== Step 1: Running parser.py ===" | tee -a "$LOG_FILE"
cd src && python3 parser.py "$DEBUG_LOG" > ../results/stats_data.txt 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 2: plot_stats.py
echo "=== Step 2: Running plot_stats.py ===" | tee -a "$LOG_FILE"
cd src && python3 plot_stats.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 3: model_offset.py
echo "=== Step 3: Running model_offset.py ===" | tee -a "$LOG_FILE"
cd src && python3 model_offset.py ../"$CSV_FILE" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 4: validate_model.py (nBits=230)
echo "=== Step 4: Running validate_model.py (nBits=230) ===" | tee -a "$LOG_FILE"
cd src && python3 validate_model.py "$DEBUG_LOG" 230 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 5: plot_distribution.py (nBits=230)
echo "=== Step 5: Running plot_distribution.py (nBits=230) ===" | tee -a "$LOG_FILE"
cd src && python3 plot_distribution.py "$DEBUG_LOG" 230 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 6: analyze_bias_source.py
echo "=== Step 6: Running analyze_bias_source.py ===" | tee -a "$LOG_FILE"
cd src && python3 analyze_bias_source.py 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 7: demo_complete.py
echo "=== Step 7: Running demo_complete.py ===" | tee -a "$LOG_FILE"
cd src && python3 demo_complete.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 8: investigate_why.py
echo "=== Step 8: Running investigate_why.py ===" | tee -a "$LOG_FILE"
cd src && python3 investigate_why.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 9: mining_optimizer_v2.py
echo "=== Step 9: Running mining_optimizer_v2.py ===" | tee -a "$LOG_FILE"
cd src && python3 mining_optimizer_v2.py 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 10: validate_new_hypothesis.py
echo "=== Step 10: Running validate_new_hypothesis.py ===" | tee -a "$LOG_FILE"
cd src && python3 validate_new_hypothesis.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 11: visualize_density.py
echo "=== Step 11: Running visualize_density.py ===" | tee -a "$LOG_FILE"
cd src && python3 visualize_density.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 12: why_110x_ratio.py
echo "=== Step 12: Running why_110x_ratio.py ===" | tee -a "$LOG_FILE"
cd src && python3 why_110x_ratio.py "$DEBUG_LOG" 2>&1 | tee -a ../"$LOG_FILE"
cd ..
echo "" | tee -a "$LOG_FILE"

# Step 13: plot_stats.gp (Gnuplot - requires stats_data.txt from parser.py)
echo "=== Step 13: Running plot_stats.gp (Gnuplot) ===" | tee -a "$LOG_FILE"
if command -v gnuplot &> /dev/null; then
    cd src && gnuplot plot_stats.gp 2>&1 | tee -a ../"$LOG_FILE"
    cd ..
else
    echo "Gnuplot not found, skipping..." | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

echo "=== Pipeline Complete ===" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "Output: $LOG_FILE"
