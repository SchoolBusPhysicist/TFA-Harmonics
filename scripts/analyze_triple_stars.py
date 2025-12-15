#!/usr/bin/env python3
"""
TRIPLE STAR SYSTEMS ANALYSIS
Testing 456/k harmonics in hierarchical systems

Run: python3 analyze_triple_stars.py

Data sources:
- Tokovinin MSC: triples/export/ (14,639 systems)
  - sys.tsv: system records
  - comp.tsv: component records  
  - orb.tsv: orbital elements
- Nagarajan Gaia DR3: triples/nagarajan-gaia-triples/ (14,818 systems)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

RESULTS_FILE = '/mnt/user-data/outputs/triple_stars_results.json'
SUMMARY_FILE = '/mnt/user-data/outputs/triple_stars_summary.txt'

results = {}

def save_result(key, value):
    results[key] = value
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def log(msg):
    print(msg)
    with open(SUMMARY_FILE, 'a') as f:
        f.write(msg + '\n')

with open(SUMMARY_FILE, 'w') as f:
    f.write(f"Triple Stars Analysis - {datetime.now()}\n{'='*70}\n\n")

log("="*70)
log("TRIPLE STAR SYSTEMS: Testing 456/k Harmonics")
log("="*70)

try:
    # Load Tokovinin data
    log("\n[1/5] Loading Tokovinin MSC catalog...")
    
    try:
        tok_sys = pd.read_csv('triples/export/sys.tsv', sep='\t', low_memory=False)
        log(f"✓ Systems: {len(tok_sys)}")
        save_result('tokovinin_systems', len(tok_sys))
    except Exception as e:
        log(f"  sys.tsv: {e}")
        tok_sys = pd.DataFrame()
    
    try:
        tok_comp = pd.read_csv('triples/export/comp.tsv', sep='\t', low_memory=False)
        log(f"✓ Components: {len(tok_comp)}")
        save_result('tokovinin_components', len(tok_comp))
    except Exception as e:
        log(f"  comp.tsv: {e}")
        tok_comp = pd.DataFrame()
    
    try:
        tok_orb = pd.read_csv('triples/export/orb.tsv', sep='\t', low_memory=False)
        log(f"✓ Orbits: {len(tok_orb)}")
        save_result('tokovinin_orbits', len(tok_orb))
    except Exception as e:
        log(f"  orb.tsv: {e}")
        tok_orb = pd.DataFrame()
    
    # Load Nagarajan Gaia data
    log("\n[2/5] Loading Nagarajan Gaia DR3 catalog...")
    
    try:
        # Look for main data file in directory
        import os
        nag_dir = 'triples/nagarajan-gaia-triples/'
        nag_files = os.listdir(nag_dir) if os.path.exists(nag_dir) else []
        log(f"  Files in directory: {nag_files[:5]}...")
        
        # Try to load main catalog
        data_files = [f for f in nag_files if f.endswith('.csv') or f.endswith('.tsv')]
        if data_files:
            main_file = os.path.join(nag_dir, data_files[0])
            nag_df = pd.read_csv(main_file, low_memory=False)
            log(f"✓ Loaded {len(nag_df)} systems from {data_files[0]}")
            save_result('nagarajan_systems', len(nag_df))
        else:
            log("  No CSV/TSV files found")
            nag_df = pd.DataFrame()
    except Exception as e:
        log(f"  Load error: {e}")
        nag_df = pd.DataFrame()
    
    # Analyze Tokovinin structure
    log("\n[3/5] Analyzing Tokovinin data structure...")
    
    if len(tok_sys) > 0:
        log(f"\nSystems table columns: {list(tok_sys.columns)[:10]}...")
        
    if len(tok_orb) > 0:
        log(f"\nOrbital elements columns: {list(tok_orb.columns)[:10]}...")
        
        # Look for periods
        period_cols = [c for c in tok_orb.columns if 'per' in c.lower() or 'P' in c]
        if period_cols:
            log(f"  Period columns found: {period_cols}")
            
            # Calculate period statistics
            for col in period_cols:
                if pd.api.types.is_numeric_dtype(tok_orb[col]):
                    valid = tok_orb[col].notna() & (tok_orb[col] > 0)
                    if valid.sum() > 0:
                        periods = tok_orb.loc[valid, col]
                        log(f"\n  {col}:")
                        log(f"    Count: {len(periods)}")
                        log(f"    Range: {periods.min():.2f} - {periods.max():.2f}")
                        log(f"    Median: {periods.median():.2f}")
    
    # Compare to red giants
    log("\n[4/5] Comparing to red giant k distribution...")
    
    # Red giant reference from our previous analysis
    rg_reference = {
        'median_k': 49.82,
        'mean_k': 50.18,
        'percent_above_35': 96.0,
        'n_stars': 16094
    }
    save_result('red_giant_reference', rg_reference)
    
    log(f"\nRed Giant Reference (16,094 stars):")
    log(f"  k median = {rg_reference['median_k']:.2f}")
    log(f"  {rg_reference['percent_above_35']:.1f}% have k>35 (deep modes)")
    
    log(f"\nTriple Star Systems:")
    log(f"  Tokovinin: {len(tok_sys)} systems")
    log(f"  Nagarajan: {len(nag_df) if len(nag_df) > 0 else 'not loaded'} systems")
    log(f"  Total: {len(tok_sys) + len(nag_df)}")
    
    # Create comparison plot
    log("\n[5/5] Creating visualization...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Dataset sizes
    ax = axes[0]
    datasets = ['Red Giants\n(single)', 'Tokovinin\n(triples)', 'Nagarajan\n(triples)']
    counts = [16094, len(tok_sys), len(nag_df) if len(nag_df) > 0 else 0]
    colors = ['purple', 'blue', 'green']
    
    bars = ax.bar(datasets, counts, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Number of Systems', fontsize=12, fontweight='bold')
    ax.set_title('Dataset Comparison', fontsize=13, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(alpha=0.3, axis='y')
    
    for bar, count in zip(bars, counts):
        if count > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                    f'{count:,}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Multiplicity effects (conceptual)
    ax = axes[1]
    
    systems = ['Single\nStars', 'Binary\nStars', 'Triple\nStars']
    k_expected = [50, 35, 25]  # Hypothetical - surface modes increase with companions
    
    ax.bar(systems, k_expected, color=['purple', 'orange', 'blue'], alpha=0.7, edgecolor='black')
    ax.axhline(35, color='red', linestyle='--', linewidth=2, label='k=35 threshold')
    ax.set_ylabel('Expected k value', fontsize=12, fontweight='bold')
    ax.set_title('Multiplicity Hypothesis\n(To Be Tested)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/triple_stars_overview.png', dpi=150, bbox_inches='tight')
    log("✓ Saved: triple_stars_overview.png")
    
    # Summary
    log("\n" + "="*70)
    log("SUMMARY")
    log("="*70)
    
    log(f"\nData loaded:")
    log(f"  Tokovinin: {len(tok_sys)} systems, {len(tok_orb)} orbits")
    log(f"  Nagarajan: {len(nag_df) if len(nag_df) > 0 else 0} systems")
    
    log(f"\nHypothesis to test:")
    log(f"  1. Do triple stars show 456/k harmonic structure?")
    log(f"  2. Does multiplicity shift k distribution?")
    log(f"  3. Single (k~50) vs Binary (k~35?) vs Triple (k~25?)")
    
    log("\n" + "="*70)
    log("NEXT STEPS:")
    log("="*70)
    log("Need oscillation/frequency data for triple systems")
    log("If unavailable, focus on orbital period analysis:")
    log("  - Test if orbital periods follow 456/k pattern")
    log("  - Compare period distributions to predictions")
    
    save_result('timestamp', str(datetime.now()))
    save_result('status', 'Data loaded - need frequency/period extraction')
    
    log(f"\n✓ Results saved to: {RESULTS_FILE}")

except Exception as e:
    log(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    save_result('error', str(e))

print(f"\nView results: cat {SUMMARY_FILE}")
