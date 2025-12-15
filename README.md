# KDFA Stellar Harmonics

**Universal Harmonic Structure in Stellar Oscillations: A Real-Number Coupling Framework**

## Overview

This repository contains the complete reproducibility package for the paper:

> **"Universal Harmonic Structure in Stellar Oscillations: A Real-Number Coupling Framework with Neutrino and Number-Theoretic Validation"**
>
> Jason A. King (2025)

**Systems Analyzed:** 25,857 stellar systems + gas giants (Jupiter, Saturn)

## Key Results

| Observable | Predicted | Measured | Match |
|------------|-----------|----------|-------|
| Neutrino D₂ | 1.46 ± 0.10 | 1.495 ± 0.144 | 96.9% |
| Super-K Δm² | 2.50 × 10⁻³ eV² | 2.43 × 10⁻³ eV² | 97.2% |
| Stellar 456-day clustering | Excess | 2.81× expected | p < 0.0001 |
| Jupiter Δν | 152 μHz | 155.3 μHz | 97.9% |
| Saturn p-modes | 608 μHz | ~600 μHz | ~99% |
| Murmuration node | 1/e = 0.3679 | 0.3627 | 98.6% |

## Repository Structure

```
KDFA-Stellar-Harmonics/
├── paper/
│   └── KDFA_stellar_paper_v4.md       # Main paper
├── scripts/
│   ├── validate_heartbeat_stars.py    # Kirk 2016 catalog validation
│   ├── analyze_heartbeat_stars.py     # OGLE/Kepler analysis
│   ├── analyze_triple_stars.py        # Triple system κ analysis
│   ├── analyze_yu2018_red_giants.py   # 16,094 red giants analysis
│   ├── calculate_d2.py                # D₂ correlation dimension
│   └── visualize_neutrino.py          # Neutrino visualization
├── docs/
│   ├── STELLAR_VALIDATION_RESULTS.md  # Full 25,857 system results
│   ├── ZONE_CLASSIFICATIONS.md        # κ values by star type
│   ├── GAS_GIANT_VALIDATION.md        # Jupiter/Saturn validation
│   └── DATA_SOURCES.md                # All raw data links
├── data/
│   ├── 20211217_HESE-7-5-year-data.zip
│   └── 20080911_AMANDA_7_Year_Data.zip
├── MASTER_VALIDATIONS_v1.md           # Complete validation record
├── requirements.txt
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

## Zone Classifications

| System Type | κ Value | Zone | Stability |
|-------------|---------|------|-----------|
| Gaia wide binaries | 0.281 ± 0.003 | Zone 1 | Very stable |
| Heartbeat stars | 0.167 ± 0.086 | Zone 1 | Stable |
| Triple systems | 0.446 ± 0.143 | Zone 2 | Generative |
| KOI-54 | 0.57 | Zone 2 (upper) | Pre-collapse |

See [docs/ZONE_CLASSIFICATIONS.md](docs/ZONE_CLASSIFICATIONS.md) for details.

## Gas Giant Validation

The 456/k pattern appears in gas giants **without fusion**:

| Planet | Measured | Predicted | Error |
|--------|----------|-----------|-------|
| Jupiter | 155.3 μHz | 456/3 = 152 μHz | 2.1% |
| Saturn | ~600 μHz | 456 × 4/3 = 608 μHz | ~1% |

**Conclusion:** The harmonic requires fluid dynamics, not nuclear burning.

See [docs/GAS_GIANT_VALIDATION.md](docs/GAS_GIANT_VALIDATION.md) for details.

## Data Sources

All data is publicly available for independent verification:

- **Kepler Heartbeat Stars**: [Kirk et al. 2016 (VizieR)](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/151/68)
- **Red Giants**: [Yu et al. 2018 (VizieR)](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/236/42)
- **IceCube Neutrinos**: [HESE 7.5-year](https://icecube.wisc.edu/data-releases/)
- **Jupiter**: [Gaulme et al. 2011](https://doi.org/10.1051/0004-6361/201016290)
- **Saturn**: [Mankovich et al. 2019](https://doi.org/10.3847/1538-4357/aaf798)
- **Elliptic Curves**: [LMFDB Database](https://www.lmfdb.org/EllipticCurve/Q/)

See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for complete list.

## Requirements

```
numpy>=1.20.0
scipy>=1.7.0
matplotlib>=3.4.0
pandas>=1.3.0
scikit-learn>=0.24.0
astropy>=5.0.0
astroquery>=0.4.0
```

## Usage

```bash
# Analyze heartbeat stars (Kirk 2016 catalog)
python scripts/validate_heartbeat_stars.py

# Run full 25K analysis
python scripts/analyze_heartbeat_stars.py

# Calculate D₂ for neutrinos
python scripts/calculate_d2.py

# Analyze triple star κ values
python scripts/analyze_triple_stars.py
```

## Falsification Criteria

The framework fails if:
1. D₂ measured outside 1.35-1.55 in independent datasets
2. 456-day stellar excess disappears in larger samples
3. Amplitude damping deviates >5% from prediction
4. Gas giant oscillations deviate >5% from 456/k
5. Murmuration nodes deviate >5% from 1/e

## Documentation

| Document | Contents |
|----------|----------|
| [STELLAR_VALIDATION_RESULTS.md](docs/STELLAR_VALIDATION_RESULTS.md) | Full Monte Carlo analysis of 25,857 systems |
| [ZONE_CLASSIFICATIONS.md](docs/ZONE_CLASSIFICATIONS.md) | κ values and zone structure for all star types |
| [GAS_GIANT_VALIDATION.md](docs/GAS_GIANT_VALIDATION.md) | Jupiter and Saturn oscillation validation |
| [DATA_SOURCES.md](docs/DATA_SOURCES.md) | All raw data links for reproducibility |

## Citation

```bibtex
@article{king2025stellar,
  title={Universal Harmonic Structure in Stellar Oscillations:
         A Real-Number Coupling Framework},
  author={King, Jason A.},
  year={2025},
  note={GitHub: SchoolBusPhysicist/KDFA-Stellar-Harmonics}
}
```

## License

CC-BY-4.0

## Contact

Jason A. King - Independent Researcher, Missouri, USA
GitHub: https://github.com/SchoolBusPhysicist/KDFA-Stellar-Harmonics
