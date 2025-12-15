#!/usr/bin/env python3
"""
HEARTBEAT STARS ANALYSIS
Testing k<35 prediction for tidal surface oscillations

Run: python3 analyze_heartbeat_stars.py

Data sources:
- OGLE: heartbeat/ogle_heartbeat_vizier.vot (991 systems)
- Kepler: heartbeat/kepler/kepler_heartbeat_vizier.vot (22 systems)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io.votable import parse
import json
from datetime import datetime

RESULTS_FILE = '/mnt/user-data/outputs/heartbeat_results.json'
SUMMARY_FILE = '/mnt/user-data/outputs/heartbeat_summary.txt'

results = {}

def save_result(key, value):
    results[key] = value
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def log(msg):
    print(msg)
    with open(SUMMARY_FILE, 'a') as f:
        f.write(msg + '\n')

# Clear previous
with open(SUMMARY_FILE, 'w') as f:
    f.write(f"Heartbeat Stars Analysis - {datetime.now()}\n{'='*70}\n\n")

log("="*70)
log("HEARTBEAT STARS: Testing k<35 Surface Mode Prediction")
log("="*70)

try:
    # Load OGLE data
    log("\n[1/4] Loading OGLE heartbeat stars...")
    try:
        votable = parse('heartbeat/ogle_heartbeat_vizier.vot')
        ogle_table = votable.get_first_table()
        ogle_df = ogle_table.to_table().to_pandas()
        log(f"✓ Loaded {len(ogle_df)} OGLE systems")
        log(f"  Columns: {list(ogle_df.columns)[:5]}...")
        save_result('ogle_count', len(ogle_df))
    except Exception as e:
        log(f"✗ OGLE load failed: {e}")
        ogle_df = pd.DataFrame()
    
    # Load Kepler data  
    log("\n[2/4] Loading Kepler heartbeat stars...")
    try:
        votable = parse('heartbeat/kepler/kepler_heartbeat_vizier.vot')
        kepler_table = votable.get_first_table()
        kepler_df = kepler_table.to_table().to_pandas()
        log(f"✓ Loaded {len(kepler_df)} Kepler systems")
        log(f"  Columns: {list(kepler_df.columns)[:5]}...")
        save_result('kepler_count', len(kepler_df))
    except Exception as e:
        log(f"✗ Kepler load failed: {e}")
        kepler_df = pd.DataFrame()
    
    # KOI-54 reference
    koi54 = {
        'name': 'KOI-54',
        'k_values': [5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17],
        'amplitudes': [527.1, 51.4, 11.6, 20.0, 124.6, 91.3, 24.0, 6.9, 5.9, 20.4, 9.1],
        'k_mean': 10.5,
        'k_median': 11.0
    }
    save_result('koi54_reference', koi54)
    
    log("\n[3/4] Analyzing available parameters...")
    
    # Try to extract periods, frequencies
    if len(ogle_df) > 0:
        log(f"\nOGLE dataset preview:")
        log(f"  Shape: {ogle_df.shape}")
        # Check for period/frequency columns
        period_cols = [c for c in ogle_df.columns if 'per' in c.lower() or 'freq' in c.lower()]
        if period_cols:
            log(f"  Period/freq columns: {period_cols}")
    
    if len(kepler_df) > 0:
        log(f"\nKepler dataset preview:")
        log(f"  Shape: {kepler_df.shape}")
        period_cols = [c for c in kepler_df.columns if 'per' in c.lower() or 'freq' in c.lower()]
        if period_cols:
            log(f"  Period/freq columns: {period_cols}")
    
    # Calculate k if we have oscillation data
    # (This will depend on what columns are actually present)
    # For now, document the structure
    
    log("\n[4/4] Creating comparison plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: KOI-54 k distribution (reference)
    ax = axes[0]
    ax.bar(koi54['k_values'], koi54['amplitudes'], color='green', alpha=0.7, edgecolor='black')
    ax.axvline(35, color='orange', linestyle='--', linewidth=3, label='k=35 threshold')
    ax.set_xlabel('k value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amplitude (ppm)', fontsize=12, fontweight='bold')
    ax.set_title('KOI-54 Heartbeat Star\n(Tidal Surface Modes)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xlim([0, 40])
    
    # Plot 2: Dataset summary
    ax = axes[1]
    datasets = ['OGLE', 'Kepler', 'KOI-54']
    counts = [len(ogle_df), len(kepler_df), 1]
    colors = ['blue', 'red', 'green']
    
    bars = ax.bar(datasets, counts, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Number of Systems', fontsize=12, fontweight='bold')
    ax.set_title('Heartbeat Star Datasets', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/heartbeat_overview.png', dpi=150, bbox_inches='tight')
    log("✓ Saved: heartbeat_overview.png")
    
    # Summary
    log("\n" + "="*70)
    log("SUMMARY")
    log("="*70)
    log(f"\nDatasets loaded:")
    log(f"  OGLE:   {len(ogle_df)} systems")
    log(f"  Kepler: {len(kepler_df)} systems")
    log(f"  Total:  {len(ogle_df) + len(kepler_df)} systems")
    
    log(f"\nKOI-54 reference:")
    log(f"  All k values < 35: {max(koi54['k_values'])} < 35 ✓")
    log(f"  Mean k = {koi54['k_mean']:.1f}")
    log(f"  Prediction: Heartbeat stars = surface tidal modes → k<35")
    
    log("\n" + "="*70)
    log("NEXT STEPS:")
    log("="*70)
    log("Need to extract:")
    log("  1. Orbital periods")
    log("  2. TEO mode frequencies (if available)")
    log("  3. Calculate k = 456/n for each system")
    log("\nThen test: Do heartbeat stars cluster at k<35?")
    
    save_result('timestamp', str(datetime.now()))
    save_result('status', 'Data loaded - need frequency extraction')
    
    log(f"\n✓ Results saved to: {RESULTS_FILE}")

except Exception as e:
    log(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    save_result('error', str(e))

print(f"\nView results: cat {SUMMARY_FILE}")
