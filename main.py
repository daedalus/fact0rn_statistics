#!/usr/bin/env python3
"""
Fact0rn wOffset Statistics - Full Pipeline
Uses subprocess to run scripts.

Usage:
    python3 main.py [debug.log_path] [--skip-gnuplot] [--nBits 230]
"""

import sys
import os
import argparse
import subprocess
import logging
import shutil
from pathlib import Path

def setup_logging(log_file):
    """Setup logging to both file and console"""
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description='Fact0rn wOffset Statistics - Full Pipeline'
    )
    parser.add_argument(
        'debug_log',
        nargs='?',
        default=os.path.expanduser('~/.factorn/debug.log'),
        help='Path to debug.log (default: ~/.factorn/debug.log)'
    )
    parser.add_argument(
        '--skip-gnuplot',
        action='store_true',
        help='Skip Gnuplot step'
    )
    parser.add_argument(
        '--nBits',
        type=int,
        default=230,
        help='nBits value for analysis scripts (default: 230)'
    )
    parser.add_argument(
        '--output-dir',
        default='results',
        help='Output directory for logs and results (default: results)'
    )
    
    args = parser.parse_args()
    
    # Get absolute paths
    project_root = Path(__file__).parent.absolute()
    debug_log = Path(args.debug_log).expanduser().absolute()
    
    if not debug_log.exists():
        print(f"Error: debug log not found: {debug_log}")
        sys.exit(1)
    
    output_dir = (project_root / args.output_dir).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    log_file = output_dir / 'pipeline.log'
    csv_file = output_dir / 'wOffset_statistics.csv'
    
    # Setup logging
    logger = setup_logging(str(log_file))
    
    logger.info("=== Fact0rn wOffset Statistics Pipeline ===")
    logger.info(f"Using debug log: {debug_log}")
    logger.info(f"Project root: {project_root}")
    logger.info(f"Started: {subprocess.check_output(['date']).decode().strip()}")
    logger.info("")
    
    success = True
    
    # Step 1: parser.py
    logger.info("=== Step 1: Running parser.py ===")
    with open(output_dir / 'stats_data.txt', 'w') as f:
        result = subprocess.run(
            [sys.executable, str(project_root / 'src/parser.py'), str(debug_log)],
            capture_output=True,
            text=True
        )
        f.write(result.stdout)
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 2: plot_stats.py
    logger.info("=== Step 2: Running plot_stats.py ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/plot_stats.py'), str(debug_log)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 3: model_offset.py
    logger.info("=== Step 3: Running model_offset.py ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/model_offset.py'), str(csv_file)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 4: validate_model.py
    logger.info(f"=== Step 4: Running validate_model.py (nBits={args.nBits}) ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/validate_model.py'), str(debug_log), str(args.nBits)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 5: plot_distribution.py
    logger.info(f"=== Step 5: Running plot_distribution.py (nBits={args.nBits}) ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/plot_distribution.py'), str(debug_log), str(args.nBits)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 6: analyze_bias_source.py
    logger.info("=== Step 6: Running analyze_bias_source.py ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/analyze_bias_source.py'), str(csv_file)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 7: demo_complete.py
    logger.info("=== Step 7: Running demo_complete.py ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/demo_complete.py'), str(debug_log)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 8: analyze_density_ratio.py
    logger.info(f"=== Step 8: Running analyze_density_ratio.py (nBits={args.nBits}) ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/analyze_density_ratio.py'), str(debug_log), str(args.nBits)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 9: mining_optimizer.py
    logger.info("=== Step 9: Running mining_optimizer.py ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/mining_optimizer.py')],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 10: validate_new_hypothesis.py
    logger.info(f"=== Step 10: Running validate_new_hypothesis.py (nBits={args.nBits}) ===")
    result = subprocess.run(
        [sys.executable, str(project_root / 'src/validate_new_hypothesis.py'), str(debug_log), str(args.nBits)],
        cwd=str(project_root / 'src'),
        capture_output=True,
        text=True
    )
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)
    if result.returncode != 0:
        success = False
    
    # Step 11: plot_stats.gp (Gnuplot)
    if not args.skip_gnuplot:
        logger.info("=== Step 11: Running plot_stats.gp (Gnuplot) ===")
        if subprocess.run(['which', 'gnuplot'], capture_output=True).returncode == 0:
            result = subprocess.run(
                ['gnuplot', 'plot_stats.gp'],
                cwd=str(project_root / 'src'),
                capture_output=True,
                text=True
            )
            if result.stdout:
                logger.info(result.stdout)
            if result.stderr:
                logger.warning(result.stderr)
        else:
            logger.info("Gnuplot not found, skipping...")
    
    logger.info("")
    logger.info("=== Pipeline Complete ===")
    logger.info(f"Finished: {subprocess.check_output(['date']).decode().strip()}")
    logger.info(f"Output: {log_file}")
    
    if not success:
        logger.warning("Some steps failed - check log for details")
        sys.exit(1)

if __name__ == '__main__':
    main()
