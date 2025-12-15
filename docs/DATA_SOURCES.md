# Data Sources for Independent Verification

All data used in this analysis is publicly available. Links and references for reproducibility.

## Stellar Catalogs

### Kepler Heartbeat Stars (Kirk et al. 2016)
- **Paper:** Kirk, B., et al. 2016, AJ, 151, 68
- **VizieR Catalog:** https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/151/68
- **Contents:** 173 heartbeat star systems with orbital periods and eccentricities
- **Used for:** Period clustering analysis, κ zone validation

### OGLE Survey Heartbeat Stars
- **Website:** https://ogle.astrouw.edu.pl/
- **Dataset:** 991 heartbeat binary systems (ground-based)
- **Used for:** Extended sample validation

### Yu 2018 Red Giants (16,094 systems)
- **Paper:** Yu, J., et al. 2018, ApJS, 236, 42
- **VizieR Catalog:** https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/236/42
- **Contents:** Kepler red giants with ν_max and Δν measurements
- **Used for:** k-value distribution analysis

### KOI-54 (KIC 5222854)
- **Discovery:** Welsh, W.F., et al. 2011, ApJS, 197, 4
- **DOI:** 10.1088/0067-0049/197/1/4
- **Contents:** Highly eccentric binary with tidally excited oscillations
- **Used for:** κ = 0.57 pre-collapse validation

## Gas Giant Data

### Jupiter Oscillations
- **Paper:** Gaulme, P., et al. 2011, A&A, 531, A104
- **DOI:** https://doi.org/10.1051/0004-6361/201016290
- **Method:** SYMPA Doppler velocimetry
- **Key Result:** Δν = 155.3 ± 2.2 μHz

### Saturn Ring Seismology
- **f-modes:** Hedman, M.M., Nicholson, P.D. 2013, AJ, 146, 12
  - DOI: https://doi.org/10.1088/0004-6256/146/1/12
- **p-modes:** Mankovich, C., et al. 2019, ApJ, 871, 1
  - DOI: https://doi.org/10.3847/1538-4357/aaf798
- **Method:** Cassini C-ring density wave analysis
- **Key Result:** Peak power ~600 μHz

## Neutrino Data (Cross-Validation)

### IceCube HESE 7.5-year
- **Data Release:** https://icecube.wisc.edu/data-releases/2021/01/all-sky-point-source-icecube-data-years-2008-2018/
- **Contents:** 336,516 neutrino events
- **Used for:** D₂ = 1.495 ± 0.144 correlation dimension
- **Format:** Energy (GeV), Zenith (radians)

### AMANDA 7-year
- **Archive:** https://icecube.wisc.edu/science/data/
- **Used for:** Historical comparison

### Super-Kamiokande
- **Δm² measurement:** (2.43 ± 0.13) × 10⁻³ eV²
- **Source:** Super-K Collaboration atmospheric neutrino results

## Solar Data

### Magneto-Rossby Waves
- **Paper:** McIntosh, S.W., et al. 2017, Nature Astronomy, 1, 0086
- **DOI:** https://doi.org/10.1038/s41550-017-0086
- **Key Result:** 450-460 day quasi-periodicity

### Solar Neutrino Flux Periodicities
- **Paper:** Sturrock, P.A. 2008, ApJ, 688, L53
- **Key Results:** 154, 78, 51 day periods

## Number Theory (Cross-Validation)

### Elliptic Curve Murmurations
- **Discovery:** He, Y., Lee, K.H., Oliver, T., Pozdnyakov, A. 2022
- **arXiv:** https://arxiv.org/abs/2204.10140
- **Database:** LMFDB - https://www.lmfdb.org/EllipticCurve/Q/
- **Used for:** 1/e threshold validation at √(p/N) = 0.3627

## Gravitational Wave Data

### LIGO Ringdown
- **Events:** GW150914, GW151226, GW170104
- **Data:** LIGO Open Science Center - https://www.gw-openscience.org/
- **Used for:** Δω/ω₀ = 21/456 = 0.046 validation

## How to Access

### VizieR (Stellar Catalogs)
```bash
# Using Python astroquery
from astroquery.vizier import Vizier
kirk2016 = Vizier.get_catalogs('J/AJ/151/68')[0]
```

### IceCube Data
```bash
# Download HESE 7.5-year
wget https://icecube.wisc.edu/data-releases/...
```

### LMFDB (Elliptic Curves)
```python
# Query via API
import requests
url = "https://www.lmfdb.org/api/ec_curvedata/?conductor=7500-10000"
```

## Citation Format

```bibtex
@article{king2025stellar,
  title={Universal Harmonic Structure in Stellar Oscillations},
  author={King, Jason A.},
  year={2025},
  note={Data sources: Kirk+ 2016, Gaulme+ 2011, IceCube Collaboration}
}
```
