#!/usr/bin/env python3
"""
Generate zone structure diagram showing TFA zones and system classifications.
TFA Framework - Figure for paper.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

def generate_zone_structure():
    """Generate zone structure diagram with real system data."""

    fig, ax = plt.subplots(figsize=(14, 8))

    # Zone boundaries
    zone1_end = 0.35
    zone2_end = 0.65

    # Zone colors
    ax.axvspan(0, zone1_end, color='lightblue', alpha=0.4, label='Zone 1: Structural')
    ax.axvspan(zone1_end, zone2_end, color='lightgreen', alpha=0.4, label='Zone 2: Generative')
    ax.axvspan(zone2_end, 1.0, color='lightyellow', alpha=0.4, label='Zone 3: Dissipative')

    # Key thresholds
    kappa_star = 1/np.e  # 0.368
    ax.axvline(kappa_star, color='blue', linestyle='-', linewidth=2,
               label=f'κ* = 1/e = {kappa_star:.3f}')
    ax.axvline(zone2_end, color='orange', linestyle='--', linewidth=2,
               label='TRO threshold = 0.65')

    # System data points with error bars
    systems = [
        # (name, kappa, error, y_position, color)
        ('Heartbeat Stars\n(Kirk et al.)', 0.167, 0.086, 0.8, 'navy'),
        ('Gaia Wide Binaries', 0.281, 0.003, 0.7, 'darkblue'),
        ('Main Sequence\n(Solar-type)', 0.45, 0.05, 0.5, 'darkgreen'),
        ('Triple Stars', 0.446, 0.143, 0.4, 'green'),
        ('KOI-54', 0.55, 0.10, 0.3, 'olive'),
        ('Pre-merger\nSystems', 0.72, 0.08, 0.2, 'darkorange'),
    ]

    for name, kappa, error, y, color in systems:
        ax.errorbar(kappa, y, xerr=error, fmt='o', markersize=12,
                   color=color, capsize=5, capthick=2, linewidth=2)
        ax.annotate(name, xy=(kappa, y), xytext=(10, 0),
                   textcoords='offset points', fontsize=10,
                   verticalalignment='center', fontweight='bold')

    # Zone descriptions
    zone_text = [
        (0.175, 0.95, 'ZONE 1\nStructural Stability\nS dominates R\nPredictable evolution'),
        (0.50, 0.95, 'ZONE 2\nGenerative Coupling\nBalanced S-R\n456/k harmonics'),
        (0.825, 0.95, 'ZONE 3\nDissipative/TRO\nR dominates S\nCycling behavior'),
    ]

    for x, y, text in zone_text:
        ax.text(x, y, text, transform=ax.transAxes, fontsize=11,
               verticalalignment='top', horizontalalignment='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Formatting
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Coupling Parameter κ = R/(R+S)', fontsize=14)
    ax.set_ylabel('(System Distribution)', fontsize=12)
    ax.set_title('TFA Zone Structure: Stellar System Classification\n'
                 'κ* = 1/e marks transition from structural to generative regime', fontsize=14)

    # Custom legend
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', alpha=0.4, label='Zone 1: κ < 0.35 (Structural)'),
        mpatches.Patch(facecolor='lightgreen', alpha=0.4, label='Zone 2: 0.35 ≤ κ < 0.65 (Generative)'),
        mpatches.Patch(facecolor='lightyellow', alpha=0.4, label='Zone 3: κ ≥ 0.65 (Dissipative)'),
        plt.Line2D([0], [0], color='blue', linewidth=2, label='κ* = 1/e ≈ 0.368'),
        plt.Line2D([0], [0], color='orange', linestyle='--', linewidth=2, label='TRO threshold = 0.65'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

    ax.get_yaxis().set_ticks([])
    ax.grid(True, alpha=0.3, axis='x')

    # Save
    output_dir = Path(__file__).parent.parent / 'results' / 'stellar'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'zone_structure.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_zone_structure()
