#!/bin/bash
# Fact0rn wOffset Statistics - Full Pipeline
# Runs all analysis scripts and logs output to pipeline.log
# Usage: ./pipeline.sh [debug.log_path]

# Get absolute path of script directory
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")" && pwd)"

# Project root is the same as script directory (pipeline.sh is in project root)
PROJECT_ROOT="$SCRIPT_DIR"

# Get absolute path of debug log (handle relative paths)
if [ -n "$1" ]; then
    # Convert to absolute path
    DEBUG_LOG="$(cd "$(dirname "$1")" 2>/dev/null && pwd)/$(basename "$1")"
else
    DEBUG_LOG="${HOME}/.factorn/debug.log"
fi

LOG_FILE="$PROJECT_ROOT/results/pipeline.log"
CSV_FILE="results/wOffset_statistics.csv"

# Create results directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/results"

echo "=== Fact0rn wOffset Statistics Pipeline ===" | tee "$LOG_FILE"
echo "Using debug log: $DEBUG_LOG" | tee -a "$LOG_FILE"
echo "Project root: $PROJECT_ROOT" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Step 1: parser.py (outputs to stdout, redirect to file)
echo "=== Step 1: Running parser.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 parser.py "$DEBUG_LOG" > ../results/stats_data.txt 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 2: plot_stats.py
echo "=== Step 2: Running plot_stats.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 plot_stats.py "$DEBUG_LOG" 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 3: model_offset.py
echo "=== Step 3: Running model_offset.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 model_offset.py ../"$CSV_FILE" 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 4: validate_model.py (nBits=230)
echo "=== Step 4: Running validate_model.py (nBits=230) ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 validate_model.py "$DEBUG_LOG" 230 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 5: plot_distribution.py (nBits=230)
echo "=== Step 5: Running plot_distribution.py (nBits=230) ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 plot_distribution.py "$DEBUG_LOG" 230 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 6: analyze_bias_source.py
echo "=== Step 6: Running analyze_bias_source.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 analyze_bias_source.py ../"$CSV_FILE" 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 7: demo_complete.py
echo "=== Step 7: Running demo_complete.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 demo_complete.py "$DEBUG_LOG" 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 8: analyze_density_ratio.py (consolidates investigate_why, why_110x_ratio, visualize_density)
echo "=== Step 8: Running analyze_density_ratio.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 analyze_density_ratio.py "$DEBUG_LOG" 230 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 9: mining_optimizer.py
echo "=== Step 9: Running mining_optimizer.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 mining_optimizer.py 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 10: validate_new_hypothesis.py
echo "=== Step 10: Running validate_new_hypothesis.py ===" | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT/src" && python3 validate_new_hypothesis.py "$DEBUG_LOG" 230 2>&1 | tee -a "$LOG_FILE"
cd "$PROJECT_ROOT"

# Step 13: plot_stats.gp (Gnuplot)
echo "=== Step 13: Running plot_stats.gp (Gnuplot) ===" | tee -a "$LOG_FILE"
if command -v gnuplot &> /dev/null; then
    cd "$PROJECT_ROOT/src" && gnuplot plot_stats.gp 2>&1 | tee -a "$LOG_FILE"
    cd "$PROJECT_ROOT"
else
    echo "Gnuplot not found, skipping..." | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "=== Pipeline Complete ===" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "Output: $LOG_FILE" | tee -a "$LOG_FILE"
