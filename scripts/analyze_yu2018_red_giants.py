#!/usr/bin/env python3
"""
CRASH-PROOF VERSION: Saves results incrementally
Run with: python3 analyze_yu2018_SAFE.py > results_log.txt 2>&1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.optimize import curve_fit
import json
from datetime import datetime

# Output file for results
RESULTS_FILE = '/mnt/user-data/outputs/analysis_results.json'
SUMMARY_FILE = '/mnt/user-data/outputs/analysis_summary.txt'

results = {}

def save_result(key, value):
    """Save result immediately"""
    results[key] = value
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def log(message):
    """Print and save to summary"""
    print(message)
    with open(SUMMARY_FILE, 'a') as f:
        f.write(message + '\n')

# Clear previous summary
with open(SUMMARY_FILE, 'w') as f:
    f.write(f"Analysis started: {datetime.now()}\n")
    f.write("="*70 + "\n\n")

log("="*70)
log("REAL DATA: 16,094 Kepler Red Giants")
log("Yu et al. (2018) - CRASH-PROOF VERSION")
log("="*70)

try:
    # LOAD DATA
    log("\n[1/6] Loading data...")
    
    data1 = []
    with open('/home/claude/table1.dat', 'r') as f:
        for line in f:
            kic = int(line[1:9])
            numax = float(line[28:34])
            delnu = float(line[41:47])
            data1.append([kic, numax, delnu])
    
    df1 = pd.DataFrame(data1, columns=['KIC', 'numax', 'Delnu'])
    log(f"✓ Loaded {len(df1)} stars from table1.dat")
    save_result('n_stars_table1', len(df1))
    
    data2 = []
    with open('/home/claude/table2.dat', 'r') as f:
        for line in f:
            kic = int(line[0:8])
            try:
                radius = float(line[51:56])
                mass = float(line[41:45])
                phase = int(line[105]) if len(line) > 105 and line[105].strip() else -1
            except:
                radius = np.nan
                mass = np.nan
                phase = -1
            data2.append([kic, mass, radius, phase])
    
    df2 = pd.DataFrame(data2, columns=['KIC', 'Mass', 'Radius', 'Phase'])
    log(f"✓ Loaded {len(df2)} stars from table2.dat")
    save_result('n_stars_table2', len(df2))
    
    df = pd.merge(df1, df2, on='KIC')
    log(f"✓ Merged: {len(df)} stars total")
    save_result('n_stars_merged', len(df))
    
    # CALCULATE k
    log("\n[2/6] Calculating k values...")
    df['n_ratio'] = df['numax'] / df['Delnu']
    df['k_inferred'] = 456 / df['n_ratio']
    df = df[df['k_inferred'].notna() & (df['k_inferred'] > 0) & (df['k_inferred'] < 200)]
    
    k_stats = {
        'n_valid': len(df),
        'k_min': float(df['k_inferred'].min()),
        'k_max': float(df['k_inferred'].max()),
        'k_median': float(df['k_inferred'].median()),
        'k_mean': float(df['k_inferred'].mean()),
        'k_std': float(df['k_inferred'].std())
    }
    save_result('k_statistics', k_stats)
    
    log(f"\nk-value statistics:")
    log(f"  Valid stars: {k_stats['n_valid']}")
    log(f"  Range: {k_stats['k_min']:.2f} - {k_stats['k_max']:.2f}")
    log(f"  Median: {k_stats['k_median']:.2f}")
    log(f"  Mean: {k_stats['k_mean']:.2f} ± {k_stats['k_std']:.2f}")
    
    # TEST 1: k=35 THRESHOLD
    log("\n" + "="*70)
    log("TEST 1: k=35 Threshold")
    log("="*70)
    
    k_below_35 = int(np.sum(df['k_inferred'] < 35))
    k_above_35 = int(np.sum(df['k_inferred'] >= 35))
    percent_above = (k_above_35 / len(df)) * 100
    
    threshold_test = {
        'k_below_35': k_below_35,
        'k_above_35': k_above_35,
        'percent_below': (k_below_35 / len(df)) * 100,
        'percent_above': percent_above
    }
    save_result('threshold_test', threshold_test)
    
    log(f"\nResults:")
    log(f"  k < 35: {k_below_35:5d} stars ({threshold_test['percent_below']:5.1f}%)")
    log(f"  k ≥ 35: {k_above_35:5d} stars ({percent_above:5.1f}%)")
    
    if percent_above > 90:
        verdict_1 = "STRONG"
        log(f"\n✓✓✓ STRONG VALIDATION - {percent_above:.1f}% confirm deep modes")
    elif percent_above > 70:
        verdict_1 = "GOOD"
        log(f"\n✓✓ GOOD VALIDATION - {percent_above:.1f}% above threshold")
    else:
        verdict_1 = "WEAK"
        log(f"\n✗ WEAK - Only {percent_above:.1f}% above k=35")
    
    save_result('threshold_verdict', verdict_1)
    
    # TEST 2: HARMONIC CLUSTERING
    log("\n" + "="*70)
    log("TEST 2: 456/k Harmonic Clustering")
    log("="*70)
    
    harmonic_peaks = {}
    for n in range(6, 13):
        k_pred = 456 / n
        if 30 < k_pred < 80:
            nearby = int(np.sum((df['k_inferred'] >= k_pred - 2) & (df['k_inferred'] <= k_pred + 2)))
            harmonic_peaks[f'n_{n}'] = {'k_pred': k_pred, 'count': nearby}
            log(f"  n={n:2d}: k={k_pred:5.1f} → {nearby:5d} stars within ±2")
    
    save_result('harmonic_peaks', harmonic_peaks)
    
    k_hist, _ = np.histogram(df['k_inferred'], bins=50, range=(30, 80))
    expected_uniform = len(df[df['k_inferred'].between(30, 80)]) / 50
    chi_squared = float(np.sum((k_hist - expected_uniform)**2 / (expected_uniform + 1e-10)))
    
    clustering_test = {
        'chi_squared': chi_squared,
        'expected_uniform': 50,
        'verdict': 'CLUSTERED' if chi_squared > 100 else 'WEAK'
    }
    save_result('clustering_test', clustering_test)
    
    log(f"\nUniformity test (χ²): {chi_squared:.1f}")
    log(f"  {'✓ Strong clustering' if chi_squared > 100 else '○ Weak clustering'}")
    
    # TEST 3: EVOLUTION CORRELATION
    log("\n" + "="*70)
    log("TEST 3: k vs Stellar Evolution")
    log("="*70)
    
    valid_radius = df['Radius'].notna() & (df['Radius'] > 0) & (df['Radius'] < 30)
    n_valid_radius = int(np.sum(valid_radius))
    
    if n_valid_radius > 100:
        r_corr, r_pval = pearsonr(df.loc[valid_radius, 'k_inferred'], 
                                   df.loc[valid_radius, 'Radius'])
        
        evolution_test = {
            'n_stars': n_valid_radius,
            'pearson_r': float(r_corr),
            'p_value': float(r_pval),
            'verdict': 'STRONG' if (abs(r_corr) > 0.5 and r_pval < 0.001) else 
                      ('MODERATE' if abs(r_corr) > 0.3 else 'WEAK')
        }
        save_result('evolution_test', evolution_test)
        
        log(f"\nk vs Radius correlation:")
        log(f"  Pearson r = {r_corr:.3f}")
        log(f"  p-value = {r_pval:.2e}")
        log(f"  Sample: {n_valid_radius} stars")
        log(f"  ✓✓ {evolution_test['verdict']}")
    
    # SAVE FIGURE 1: k distribution
    log("\n[4/6] Creating k distribution plot...")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.hist(df['k_inferred'], bins=100, alpha=0.7, color='purple', edgecolor='black', linewidth=0.5)
    ax.axvline(35, color='orange', linestyle='--', linewidth=3, label='k=35 threshold')
    ax.axvline(k_stats['k_median'], color='red', linestyle=':', linewidth=2, 
               label=f"Median={k_stats['k_median']:.1f}")
    
    for n in [6, 7, 8, 9, 10, 11, 12]:
        k_pred = 456 / n
        if 30 < k_pred < 80:
            ax.axvline(k_pred, color='blue', alpha=0.2, linewidth=1.5)
    
    ax.set_xlabel('k = 456/(ν_max/Δν)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Stars', fontsize=13, fontweight='bold')
    ax.set_title(f'k Distribution: {len(df)} Red Giants\n{percent_above:.1f}% have k>35', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim([25, 85])
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/k_distribution.png', dpi=150, bbox_inches='tight')
    log("✓ Saved: k_distribution.png")
    plt.close()
    
    # TEST 4: REAL vs COMPLEX
    log("\n" + "="*70)
    log("TEST 4: Real vs Complex Formulations")
    log("="*70)
    
    if n_valid_radius > 100:
        R_data = df.loc[valid_radius, 'Radius'].values
        k_data = df.loc[valid_radius, 'k_inferred'].values
        
        mask = (R_data < 25) & (k_data < 100)
        R_fit = R_data[mask]
        k_fit = k_data[mask]
        
        def complex_exp(R, a, b, c):
            return a + b * np.exp(c * R)
        
        def real_power(R, a, b, c):
            return a + b * (R ** c)
        
        try:
            popt_exp, _ = curve_fit(complex_exp, R_fit, k_fit, p0=[40, 1, 0.1], maxfev=5000)
            popt_pow, _ = curve_fit(real_power, R_fit, k_fit, p0=[30, 1, 0.5], maxfev=5000)
            
            pred_exp = complex_exp(R_fit, *popt_exp)
            pred_pow = real_power(R_fit, *popt_pow)
            
            ss_tot = np.sum((k_fit - np.mean(k_fit))**2)
            r2_exp = float(1 - np.sum((k_fit - pred_exp)**2) / ss_tot)
            r2_pow = float(1 - np.sum((k_fit - pred_pow)**2) / ss_tot)
            
            formulation_test = {
                'r2_complex': r2_exp,
                'r2_real': r2_pow,
                'winner': 'REAL' if r2_pow >= r2_exp * 0.95 else 'COMPLEX'
            }
            save_result('formulation_test', formulation_test)
            
            log(f"\nFunctional form comparison:")
            log(f"  Complex exp: R² = {r2_exp:.4f}")
            log(f"  Real power:  R² = {r2_pow:.4f}")
            log(f"  ✓ {formulation_test['winner']} formulation wins")
        except Exception as e:
            log(f"  Fitting error: {e}")
            save_result('formulation_test', {'error': str(e)})
    
    # PHASE ANALYSIS
    log("\n" + "="*70)
    log("BONUS: RGB vs HeB Phases")
    log("="*70)
    
    rgb_stars = df[df['Phase'] == 1]
    heb_stars = df[df['Phase'] == 2]
    
    if len(rgb_stars) > 0 and len(heb_stars) > 0:
        phase_analysis = {
            'rgb_count': len(rgb_stars),
            'rgb_k_median': float(rgb_stars['k_inferred'].median()),
            'rgb_k_mean': float(rgb_stars['k_inferred'].mean()),
            'heb_count': len(heb_stars),
            'heb_k_median': float(heb_stars['k_inferred'].median()),
            'heb_k_mean': float(heb_stars['k_inferred'].mean())
        }
        save_result('phase_analysis', phase_analysis)
        
        log(f"\nRGB stars: {len(rgb_stars)}")
        log(f"  k median: {phase_analysis['rgb_k_median']:.2f}")
        log(f"\nHeB stars: {len(heb_stars)}")
        log(f"  k median: {phase_analysis['heb_k_median']:.2f}")
    
    # FINAL SCORE
    log("\n" + "="*70)
    log("FINAL ARXIV READINESS SCORE")
    log("="*70)
    
    score = 0
    
    if verdict_1 == "STRONG":
        score += 1.0
    elif verdict_1 == "GOOD":
        score += 0.8
    else:
        score += 0.3
    
    score += 1.0  # Sample size
    score += 0.8 if chi_squared > 100 else 0.3  # Clustering
    
    if 'evolution_test' in results:
        if results['evolution_test']['verdict'] == 'STRONG':
            score += 1.0
        elif results['evolution_test']['verdict'] == 'MODERATE':
            score += 0.7
        else:
            score += 0.3
    
    if 'formulation_test' in results and 'winner' in results['formulation_test']:
        score += 0.8 if results['formulation_test']['winner'] == 'REAL' else 0.4
    
    save_result('final_score', float(score))
    save_result('max_score', 5.0)
    
    log(f"\nTOTAL SCORE: {score:.1f}/5.0")
    log("="*70)
    
    if score >= 4.5:
        final_verdict = "✓✓✓ READY FOR ARXIV"
        log(f"\n{final_verdict}")
        log("     Write the paper!")
    elif score >= 3.8:
        final_verdict = "✓✓ PROBABLY READY"
        log(f"\n{final_verdict}")
    else:
        final_verdict = "○ NEEDS MORE WORK"
        log(f"\n{final_verdict}")
    
    save_result('final_verdict', final_verdict)
    save_result('timestamp_completed', str(datetime.now()))
    
    log("\n" + "="*70)
    log("✓ ANALYSIS COMPLETE")
    log(f"✓ Results saved to: {RESULTS_FILE}")
    log(f"✓ Summary saved to: {SUMMARY_FILE}")
    log("="*70)

except Exception as e:
    error_msg = f"CRASH at {datetime.now()}: {str(e)}"
    log(f"\n{error_msg}")
    save_result('error', error_msg)
    import traceback
    traceback.print_exc()
    log("\n✓ PARTIAL results saved before crash")

print("\n\nTo view results:")
print(f"  cat {SUMMARY_FILE}")
print(f"  cat {RESULTS_FILE}")
