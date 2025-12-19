#!/usr/bin/env python3
"""
Verify D₂ measurements from HESE 7.5-year data

This script independently calculates D₂ to verify which measurement is correct:
- 1.495 ± 0.144 (originally claimed)
- 1.46 ± 0.07 (weighted combined)
"""

import json
import numpy as np
from scipy.spatial.distance import pdist, cdist
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("D₂ VERIFICATION FROM HESE 7.5-YEAR DATA")
print("=" * 70)
print()

# Load HESE data
with open('data/HESE-7-year-data-release-main/HESE-7-year-data-release/resources/data/HESE_data.json') as f:
    data = json.load(f)

# Extract event data
energy = np.array(data['recoDepositedEnergy'])  # in GeV
zenith = np.array(data['recoZenith'])  # in radians

n_events = len(energy)
print(f"HESE 7.5-year events: {n_events}")
print(f"Energy range: {energy.min()/1e3:.1f} - {energy.max()/1e3:.0f} TeV")
print(f"Zenith range: {np.degrees(zenith.min()):.1f}° - {np.degrees(zenith.max()):.1f}°")
print()

# Prepare features (normalized)
log_e = np.log10(energy)
cos_zenith = np.cos(zenith)

# Normalize to [0, 1]
log_e_norm = (log_e - log_e.min()) / (log_e.max() - log_e.min())
cos_z_norm = (cos_zenith - cos_zenith.min()) / (cos_zenith.max() - cos_zenith.min())

features = np.column_stack([log_e_norm, cos_z_norm])

print(f"Feature space: [log10(E), cos(zenith)] normalized to [0,1]")
print()

def grassberger_procaccia(X, n_radii=30):
    """Calculate D₂ using Grassberger-Procaccia algorithm."""
    N = len(X)
    distances = pdist(X, metric='euclidean')

    d_min = np.percentile(distances[distances > 0], 5)
    d_max = np.percentile(distances, 95)
    r_values = np.logspace(np.log10(d_min), np.log10(d_max), n_radii)

    C_r = []
    for r in r_values:
        count = np.sum(distances < r)
        C_r.append(2.0 * count / (N * (N - 1)))
    C_r = np.array(C_r)

    # Scaling region
    valid = (C_r > 0.01) & (C_r < 0.99)
    if np.sum(valid) < 5:
        return np.nan, np.nan

    log_r = np.log(r_values[valid])
    log_C = np.log(C_r[valid])

    coeffs, cov = np.polyfit(log_r, log_C, 1, cov=True)
    D2 = coeffs[0]
    error = np.sqrt(cov[0, 0])

    return D2, error, r_values, C_r

def bootstrap_d2(X, n_bootstrap=1000):
    """Bootstrap estimation of D₂ uncertainty."""
    d2_samples = []
    N = len(X)

    for i in range(n_bootstrap):
        indices = np.random.choice(N, size=N, replace=True)
        sample = X[indices]
        d2, _, _, _ = grassberger_procaccia(sample)
        if not np.isnan(d2):
            d2_samples.append(d2)

    return np.mean(d2_samples), np.std(d2_samples), d2_samples

# Calculate D₂
print("-" * 70)
print("GRASSBERGER-PROCACCIA ANALYSIS")
print("-" * 70)
print()

D2_direct, err_direct, r_vals, C_vals = grassberger_procaccia(features)
print(f"Direct fit: D₂ = {D2_direct:.3f} ± {err_direct:.3f}")

# Bootstrap (with smaller n for speed)
print("\nRunning bootstrap (500 iterations)...")
D2_boot, err_boot, samples = bootstrap_d2(features, n_bootstrap=500)
print(f"Bootstrap:  D₂ = {D2_boot:.3f} ± {err_boot:.3f}")

# Calculate 95% CI
ci_low = np.percentile(samples, 2.5)
ci_high = np.percentile(samples, 97.5)
print(f"95% CI:     [{ci_low:.3f}, {ci_high:.3f}]")

print()
print("-" * 70)
print("COMPARISON WITH DOCUMENTED VALUES")
print("-" * 70)
print()

# Two claimed values
val1 = 1.495
err1 = 0.144
val2 = 1.46
err2 = 0.07

# Our measurement
measured = D2_boot
measured_err = err_boot

# Calculate deviations
diff1 = abs(measured - val1)
diff2 = abs(measured - val2)
combined_err1 = np.sqrt(measured_err**2 + err1**2)
combined_err2 = np.sqrt(measured_err**2 + err2**2)
sigma1 = diff1 / combined_err1
sigma2 = diff2 / combined_err2

print(f"Our measurement:     D₂ = {measured:.3f} ± {measured_err:.3f}")
print()
print(f"Value 1 (paper):     D₂ = {val1:.3f} ± {err1:.3f}")
print(f"  Difference: {diff1:.3f}, σ = {sigma1:.2f}")
print()
print(f"Value 2 (combined):  D₂ = {val2:.3f} ± {err2:.3f}")
print(f"  Difference: {diff2:.3f}, σ = {sigma2:.2f}")
print()

# KDFA prediction
kdfa_pred = 1.45
kdfa_err = 0.10
diff_kdfa = abs(measured - kdfa_pred)
combined_kdfa = np.sqrt(measured_err**2 + kdfa_err**2)
sigma_kdfa = diff_kdfa / combined_kdfa

print(f"KDFA Prediction:     D₂ = {kdfa_pred:.3f} ± {kdfa_err:.3f}")
print(f"  Difference: {diff_kdfa:.3f}, σ = {sigma_kdfa:.2f}")

print()
print("-" * 70)
print("CONCLUSION")
print("-" * 70)
print()

if sigma1 < sigma2:
    print(f"Value 1 ({val1} ± {err1}) is CLOSER to our measurement")
    print(f"  ({sigma1:.2f}σ vs {sigma2:.2f}σ)")
else:
    print(f"Value 2 ({val2} ± {err2}) is CLOSER to our measurement")
    print(f"  ({sigma2:.2f}σ vs {sigma1:.2f}σ)")

print()
print(f"Both values match KDFA prediction (D₂ = 1.45 ± 0.10) within:")
print(f"  Value 1: {abs(val1 - kdfa_pred)/kdfa_err:.2f}σ of prediction")
print(f"  Value 2: {abs(val2 - kdfa_pred)/kdfa_err:.2f}σ of prediction")
print(f"  Our measurement: {sigma_kdfa:.2f}σ of prediction")

print()
print("=" * 70)
