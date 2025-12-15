# KDFA Stellar Harmonics

**Universal Harmonic Structure in Stellar Oscillations: A Real-Number Coupling Framework**

## Overview

This repository contains the data, scripts, and analysis supporting the paper:

> **"Universal Harmonic Structure in Stellar Oscillations: A Real-Number Coupling Framework with Neutrino and Number-Theoretic Validation"**
>
> Jason A. King (2025)

## Key Results

| Observable | Predicted | Measured | Match |
|------------|-----------|----------|-------|
| Neutrino D₂ | 1.46 ± 0.10 | 1.495 ± 0.144 | 96.9% |
| Super-K Δm² | 2.50 × 10⁻³ eV² | 2.43 × 10⁻³ eV² | 97.2% |
| Stellar 456-day clustering | Excess | 2.81× expected | p < 0.0001 |
| Murmuration node | 1/e = 0.3679 | 0.3627 | 98.6% |
| 456 = 168e | 456.67 | 456 | 99.85% |

## Repository Structure

```
KDFA-Stellar-Harmonics/
├── paper/
│   └── KDFA_stellar_paper_v4.md    # Main paper (markdown)
├── scripts/
│   ├── validate_heartbeat_stars.py  # Stellar harmonic validation
│   └── visualize_neutrino.py        # Neutrino visualization
├── MASTER_VALIDATIONS_v1.md         # Complete validation record
└── README.md
```

## The Framework

A single real-number equation governs coupled dynamical systems:

```
κ = R / (R + S)
```

Where:
- **S** = Structural constraint (mass, gravity, boundaries)
- **R** = Relational dynamics (energy, correlations, emergence)
- **κ*** = Critical threshold ≈ 1/e ≈ 0.368

**Derived Constants (zero free parameters):**
- κ* = 1/e ≈ 0.368 (critical coupling)
- D₂ = 19/13 ≈ 1.462 (correlation dimension)
- N₀ = 168e ≈ 456 (harmonic constant)

## Data Sources

- **IceCube HESE 7.5-year**: [IceCube Public Data](https://icecube.wisc.edu/data-releases/2021/01/all-sky-point-source-icecube-data-years-2008-2018/)
- **AMANDA 7-year**: [IceCube Data Archive](https://icecube.wisc.edu/science/data/)
- **Kepler Heartbeat Stars**: [Kirk et al. 2016 Catalog](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/151/68)
- **Elliptic Curves**: [LMFDB Database](https://www.lmfdb.org/EllipticCurve/Q/)

## Requirements

```
numpy
scipy
matplotlib
pandas
scikit-learn
```

## Usage

```bash
# Validate stellar harmonics
python scripts/validate_heartbeat_stars.py data/kepler_heartbeat.tsv

# Visualize neutrino data
python scripts/visualize_neutrino.py
```

## Falsification Criteria

The framework fails if:
1. D₂ measured outside 1.35-1.55 in independent datasets
2. 456-day stellar excess disappears in larger samples
3. Amplitude damping deviates >5% from prediction
4. Murmuration nodes deviate >5% from 1/e

## Citation

```bibtex
@article{king2025stellar,
  title={Universal Harmonic Structure in Stellar Oscillations:
         A Real-Number Coupling Framework},
  author={King, Jason A.},
  year={2025},
  note={Independent research}
}
```

## License

CC-BY-4.0

## Contact

Jason A. King - Independent Researcher, Missouri, USA
