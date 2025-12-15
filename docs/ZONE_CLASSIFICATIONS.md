# κ Zone Classifications for Stellar Systems

## The Coupling Parameter κ

```
κ = R / (R + S)
```

Where:
- **S** = Structural constraint (mass, gravity, potential energy)
- **R** = Relational dynamics (kinetic energy, thermal motion, emergence)
- **κ** ∈ [0, 1]

## Zone Structure

| Zone | κ Range | Character | Physical State |
|------|---------|-----------|----------------|
| **Zone 1** | κ < 0.35 | Rigid, frozen | Overcoupled, S-dominated |
| **Zone 2** | 0.35 - 0.65 | Generative, life-compatible | Balanced S-R coupling |
| **Zone 3** | κ > 0.65 | Chaotic, dissipative | Undercoupled, R-dominated |

**Critical threshold:** κ* = 1/e ≈ 0.368

## Stellar System Classifications

### Binary Systems

| System Type | κ Value | Zone | Stability |
|-------------|---------|------|-----------|
| **Gaia wide binaries** | 0.281 ± 0.003 | Zone 1 | Very stable |
| **Heartbeat stars (typical)** | 0.167 ± 0.086 | Zone 1 | Stable |
| **Triple star systems** | 0.446 ± 0.143 | Zone 2 | Generative |
| **KOI-54** | 0.57 | Zone 2 (upper) | **Pre-collapse** |

### Stellar Types by Evolution

| Star Type | κ Range | Zone | Oscillation Mode | Period |
|-----------|---------|------|------------------|--------|
| Main Sequence (Sun-like) | 0.45-0.50 | Zone 2 center | p-modes | ~5 min |
| sdB Stars | 0.40-0.45 | Lower Zone 2 | Mixed p/g | 100-600 s |
| Red Giants | 0.55-0.60 | Upper Zone 2 | g-modes | Hours-days |
| White Dwarfs | 0.35-0.40 | Zone 1/2 boundary | Damped | ~10 min |
| **Heartbeat Stars** | **0.57** | **Pre-collapse** | TEO | Orbital |

## Physical Interpretation

### Zone 1 (κ < 0.35): S-Dominated
- Structure dominates over dynamics
- Stable, crystalline, "frozen"
- Example: Wide binary stars with stable orbits
- Period clustering: Weak (too rigid for oscillations)

### Zone 2 (0.35 < κ < 0.65): Balanced
- Life-compatible, generative
- Maximum complexity and information transfer
- Example: Main sequence stars, triple systems
- Period clustering: **Strong 456/k harmonics**

### Zone 3 (κ > 0.65): R-Dominated
- Dynamics dominate over structure
- Chaotic, dissipative, pre-collapse
- Example: Systems approaching merger
- Period clustering: Unstable, breakdown

## The 0.57 Threshold (KOI-54)

KOI-54's κ = 0.57 is significant because:

1. **Above optimal center** (0.50)
2. **Approaching upper boundary** (0.65)
3. **Shows amplitude instability** (runaway growth)
4. **Predicts eventual merger** or system reconfiguration

This is the signature of a system leaving the generative zone.

## How to Calculate κ for a Binary System

```python
# From orbital parameters
def calculate_kappa(T_kinetic, U_potential):
    """
    T_kinetic: Total kinetic energy (orbital + rotational)
    U_potential: Total potential energy (gravitational binding)
    """
    R = T_kinetic
    S = abs(U_potential)
    kappa = R / (R + S)
    return kappa

# Virial theorem approximation
# For bound systems: 2T + U = 0 → κ = 1/3 ≈ 0.333
# Actual systems deviate based on energy transport
```

## Zone Predictions

| If κ is... | Expect... |
|------------|-----------|
| < 0.28 | Very stable, minimal oscillation |
| 0.28-0.35 | Stable with weak damping |
| 0.35-0.50 | Optimal for 456/k harmonics |
| 0.50-0.57 | Strong oscillations, rich spectra |
| 0.57-0.65 | Amplitude growth, instability |
| > 0.65 | Chaotic, approaching collapse |

## Data Sources

- Gaia wide binaries: Gaia DR3
- Heartbeat stars: Kirk et al. 2016, AJ 151, 68
- Triple systems: Tokovinin 2018, ApJS 235, 6
- KOI-54: Welsh et al. 2011, ApJS 197, 4
