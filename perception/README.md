# Perception Module

**Purpose:** Perceptual Energy Mapping (Pre-Kernel Layer)

---

## Overview

The perception module provides three main components:

1. **Decoder** - Decode and verify input packets
2. **Energy Estimator** - Estimate IPSH state from feature vectors
3. **Phrase Extractor** - Extract phrases from text and create PEU

---

## Module 1: Decoder

### Purpose

Decode and verify input packets from devices/sensors.

### Features

- Device registration and verification
- Sequence number verification (replay attack prevention)
- Signature verification (optional)
- Hash verification (optional)
- Trust level assessment

### Usage

```python
from perception import Decoder, TrustLevel

# Create decoder
decoder = Decoder(verify_signature=False)

# Register device
decoder.register_device("device_001", {"type": "sensor"})

# Decode packet
packet = {
    "device_id": "device_001",
    "seq": 1,
    "ts": 1234567890.0,
    "mode": "features",
    "phi": [0.5, 0.3, 0.8, 0.2, 0.6],
    "meta": {}
}

result = decoder.decode(packet)

if result.ok and result.trust_level == TrustLevel.OK:
    features = result.x_t
    # Use features...
```

### Input Format

```python
{
    "device_id": str,
    "seq": int,
    "ts": float,
    "mode": "raw" | "features",
    "phi": List[float] (if mode="features"),
    "raw": Any (if mode="raw"),
    "phi_hash": str (optional),
    "proof": {
        "nonce": str,
        "sig": str
    },
    "meta": {
        "fps": float,
        "sensor": str,
        ...
    }
}
```

### Output Format

```python
DecodeResult {
    x_t: Any,              # Raw data or features
    ok: bool,              # Verification status
    meta: Dict,            # Metadata
    device_id: str,
    sequence: int,
    timestamp: float,
    trust_level: TrustLevel  # "OK", "WARN", "FAIL"
}
```

---

## Module 2: Energy Estimator

### Purpose

Estimate IPSH state (Intensity, Polarity, Stability, Entropy) from feature vectors.

### Features

- Intensity calculation (normalized L2 norm)
- Polarity calculation (from delta features)
- Stability calculation (from variance)
- Entropy calculation (from feature distribution)
- Decision energy computation

### Usage

```python
from perception import EnergyEstimator
import numpy as np

# Create estimator
estimator = EnergyEstimator(mu_I=0.5, sigma_I=0.3, lambda_stability=1.0)

# Current feature vector
phi_t = np.array([0.8, 0.6, 0.4, 0.9, 0.3])

# Previous feature vector (optional)
phi_prev = np.array([0.7, 0.5, 0.3, 0.8, 0.2])

# Estimate IPSH state
state = estimator.estimate(phi_t, phi_prev)

print(f"I={state.I:.3f}, P={state.P:.3f}, S={state.S:.3f}, H={state.H:.3f}")
print(f"Decision Energy: {state.dE:.3f}")
```

### Formulas

- **Intensity:** `I_t = clip((||φ_t|| - μ_I) / σ_I)`
- **Polarity:** `P_t = tanh(mean(Δφ_t))` normalized to [0, 1]
- **Stability:** `S_t = exp(-λ × Var(Δφ_t))`
- **Entropy:** `H_t = -Σ p_i log(p_i) / log(d)` normalized to [0, 1]
- **Decision Energy:** `dE = I × P × S × (1 - H)`

---

## Module 3: Phrase Extractor

### Purpose

Extract phrases from text and create PEU (Perceptual Energy Unit) objects.

### Features

- Multi-language support (English, Thai)
- Phrase boundary detection
- Role classification (goal, action, modifier, context)
- Energy-based filtering
- Confidence scoring

### Usage

```python
from perception import PhraseExtractor

# Create extractor
extractor = PhraseExtractor(
    energy_threshold=0.1,
    max_phrase_length=10,
    language="auto"
)

# Extract phrases
text = "I want to create a great system that works well"
peu_list = extractor.extract(text)

for peu in peu_list:
    print(f"Phrase: '{peu.phrase}'")
    print(f"  Role: {peu.role}")
    print(f"  I={peu.I:.3f}, P={peu.P:.3f}, S={peu.S:.3f}, H={peu.H:.3f}")
    print(f"  Energy: {peu.energy:.3f}")
```

### PEU Structure

```python
PEU {
    phrase: str,
    I: float,          # Intensity [0, 1]
    P: float,          # Polarity [0, 1]
    S: float,          # Stability [0, 1]
    H: float,          # Entropy [0, 1]
    phase: float,      # Phase [0, 2π]
    freq: float,       # Frequency (Hz)
    role: str,         # "goal" | "action" | "modifier" | "context"
    confidence: float, # Confidence [0, 1]
    energy: float      # Energy = I × |P| × S × (1 - H)
}
```

### Phrase Extraction Process

1. **Tokenize** - Split text into tokens (language-aware)
2. **Detect Boundaries** - Find phrase boundaries using markers and max length
3. **Create PEU** - Compute I, P, S, H, phase, freq, role for each phrase
4. **Filter** - Filter by energy threshold
5. **Sort** - Sort by energy (descending)

---

## Integration Example

```python
from perception import Decoder, EnergyEstimator, PhraseExtractor
import numpy as np

# 1. Decode packet
decoder = Decoder()
decoder.register_device("sensor_01", {})
result = decoder.decode(packet)

if result.ok:
    # 2. Estimate energy from features
    estimator = EnergyEstimator()
    phi_t = np.array(result.x_t)
    ipsh_state = estimator.estimate(phi_t)
    
    # 3. Extract phrases from text
    extractor = PhraseExtractor()
    peu_list = extractor.extract(text)
    
    # Use results...
```

---

## Constraints

### ✅ Allowed

- Heuristic mapping
- Language-aware logic
- Approximate estimation
- Replaceable implementation

### ❌ Forbidden

- Energy computation (ΔEΨ) - use kernel instead
- Decision gate calls
- Memory operations
- Physiology references

---

## Reference

- **Perceptual Energy Mapping Spec:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`
- **Kernel Interface:** `docs/KERNEL_PE_INTERFACE.md`
- **Audit Checklist:** `docs/PERCEPTUAL_ENERGY_AUDIT_CHECKLIST.md`

---

## Status

**Development Status:** Production-ready  
**Spec Compliance:** ✅ Full compliance  
**Language Support:** English, Thai (basic)

