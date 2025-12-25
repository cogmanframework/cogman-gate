# Perception Boundary Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Boundary Definition  
**Scope:** Sensory → Energetic Transition  
**Last Updated:** 2024-12

---

## 🎯 Purpose

Perception Boundary is the **most critical boundary** in the system.

Its responsibility is to:
- Convert "signals" → "energy parameters"
- **Without interpretation**
- **Without thinking meaning**
- **Without decision-making**

> If Perception thinks → system hallucinates  
> If Perception remembers → system is contaminated  
> If Perception decides → system is dangerous

**Why This Matters:**
This boundary is the **gateway from real world to energy world**. If this boundary fails:
- Hallucination propagates through entire system
- Semantic contamination enters energy computation
- Safety boundaries are bypassed

---

## 📊 Architectural Position

```
Real World Signal
    ↓
Sensory Adapter
    ↓
Encoder / Feature Extractor
    ↓
⚠️ PERCEPTION BOUNDARY ⚠️
    ↓
EPS / IPSH / Energy Parameters
    ↓
Trajectory Builder
```

**Perception Boundary = First entry point into Energy World**

**Isolation:**
- Perception Boundary is **isolated** from other layers
- No access to memory, reasoning, or decision-making
- One-way transformation only

---

## 🔒 Core Responsibility (ONLY THIS)

Perception Boundary does **exactly 3 things**:

1. **Normalize signal** (scaling, unit alignment)
2. **Extract measurable features** (statistical, numerical)
3. **Project → energetic parameters** (EPS / IPSH)

**Perception Boundary does NOT:**
- ❌ Create memory
- ❌ Call WM Controller
- ❌ Call Kernel
- ❌ Call GateCore
- ❌ Decide ALLOW / BLOCK
- ❌ Use rule-based meaning
- ❌ Use LLM
- ❌ Generate text / action
- ❌ Create trajectory

**If any of the above occurs → boundary breach**

---

## 🚫 Absolute Prohibitions (NON-NEGOTIABLE)

Perception Boundary **MUST NOT**:

### Semantic Operations
- ❌ Interpret meaning
- ❌ Classify content
- ❌ Extract entities
- ❌ Understand intent
- ❌ Infer emotion

### System Operations
- ❌ Create memory
- ❌ Call WM Controller
- ❌ Call Kernel
- ❌ Call GateCore
- ❌ Make decisions
- ❌ Generate actions

### External Operations
- ❌ Use LLM
- ❌ Make network calls
- ❌ Access databases
- ❌ Read config files (except normalization params)

### Data Operations
- ❌ Create trajectory
- ❌ Write to storage
- ❌ Modify past states
- ❌ Store history

**Detection:**
Any code that imports from `gate/`, `memory/`, `reasoning/`, or `kernel/` is a violation.

---

## 📥 Input Contract (STRICT)

### Allowed Inputs

```python
@dataclass
class OriginPack:
    raw_signal: Any              # Raw signal data
    modality: str                # "text" | "image" | "audio" (numeric code)
    timestamp: float             # Signal timestamp
    source_id: str               # Source identifier
    metadata: Dict[str, Any]     # Additional metadata (non-semantic)
```

**Rules:**
- ✅ `raw_signal` **MUST** be preserved (immutable)
- ❌ **MUST NOT** mutate original signal
- ❌ **MUST NOT** discard original signal
- ✅ All inputs are **read-only** (no modification)

**Input Validation:**
- ✅ Check for empty signal
- ✅ Check for malformed data
- ✅ Check for unsupported modality
- ❌ **MUST NOT** auto-correct or guess

---

## 📤 Output Contract (STRICT)

### Energetic Output (Pre-Trajectory)

```python
@dataclass
class EnergeticState:
    I: float                     # Intensity [0, ∞)
    P: float                     # Polarity [0, 1]
    S: float                     # Stability [0, 1]
    H: float                     # Entropy [0, 1]
    A: float                     # Awareness [0, 1]
    S_a: float                   # Sub-awareness [0, 1]
    E_mu: float                  # Internal energy [0, ∞)
    theta: float                 # Phase [0, 2π)
    meta: Dict[str, Any]         # Non-semantic metadata
```

**Output Rules:**
- ✅ All values are numeric
- ✅ All values are in valid ranges
- ❌ **MUST NOT** include trace_id (not created yet)
- ❌ **MUST NOT** include memory references
- ❌ **MUST NOT** include routing information
- ❌ **MUST NOT** include semantic labels

**What Output IS:**
- ✅ Energetic parameters only
- ✅ Numeric values only
- ✅ Pre-trajectory state

**What Output IS NOT:**
- ❌ Trajectory (not created yet)
- ❌ Decision (not made yet)
- ❌ Memory (not accessed)
- ❌ Semantic interpretation

---

## 🔧 Feature Extraction Rules

### Allowed Feature Extraction

| Modality | Allowed Features | Examples |
|----------|-----------------|----------|
| **Text** | Token statistics, variance, polarity score | Word count, character frequency, statistical polarity |
| **Image** | Contrast, intensity histogram | Pixel intensity, contrast metrics, histogram |
| **Audio** | Amplitude, spectral entropy | Amplitude distribution, frequency spectrum, entropy |

**Rules:**
- ✅ Statistical features only
- ✅ Numerical measurements only
- ✅ No semantic interpretation
- ✅ No classification

### Forbidden Feature Extraction

- ❌ **MUST NOT** assign labels
- ❌ **MUST NOT** classify intent
- ❌ **MUST NOT** infer emotion symbolically
- ❌ **MUST NOT** extract entities
- ❌ **MUST NOT** perform NLP operations

**Example (Forbidden):**
```python
# ❌ FORBIDDEN
intent = classify_intent(text)  # Semantic classification
emotion = detect_emotion(text)  # Semantic interpretation
entities = extract_entities(text)  # Semantic extraction
```

**Example (Allowed):**
```python
# ✅ ALLOWED
word_count = len(tokens)  # Statistical
variance = np.var(features)  # Numerical
polarity_score = compute_polarity(features)  # Numerical (not semantic)
```

---

## ⚡ Energy Projection (Canonical Only)

### Allowed Formulas

Only **canonical formulas** are allowed:

```python
# Intensity
I = ||features|| / max_norm

# Entropy
H = variance / max_variance

# Stability
S = 1 / (1 + Δstate)

# Polarity
P = normalized_polarity_score(features)
```

**Rules:**
- ✅ Use only canonical formulas
- ✅ All formulas are deterministic
- ✅ All formulas are numeric
- ❌ **MUST NOT** use heuristic rules
- ❌ **MUST NOT** use domain-specific meaning
- ❌ **MUST NOT** use adaptive thresholds

### Forbidden Projection

- ❌ **MUST NOT** use rule-based meaning
- ❌ **MUST NOT** use context-dependent logic
- ❌ **MUST NOT** use learned thresholds
- ❌ **MUST NOT** use semantic interpretation

**Example (Forbidden):**
```python
# ❌ FORBIDDEN
if "danger" in text:
    I = 1.0  # Semantic rule
if context == "medical":
    H = 0.1  # Domain-specific
```

---

## 🔄 Determinism Requirement

Perception Boundary **MUST** be:
- ✅ Deterministic (same input → same output)
- ✅ Reproducible (no randomness)
- ✅ Stateless (no memory between calls)
- ✅ Config-free (no policy loading)

**Guarantee:**
```
Same input → Same output
Every time.
```

**Forbidden:**
- ❌ Random number generation
- ❌ Time-based behavior
- ❌ Global mutable state
- ❌ Adaptive behavior
- ❌ Learning from data

---

## ⚠️ Error Handling Policy

### Allowed Errors

Perception Boundary **MAY** raise errors for:
- ✅ Malformed input
- ✅ Empty signal
- ✅ Unsupported modality
- ✅ Invalid feature extraction

### Error Handling Rules

**On Error:**
- ✅ **RAISE** exception immediately
- ✅ **DO NOT** recover silently
- ✅ **DO NOT** auto-correct
- ✅ **DO NOT** guess values
- ✅ **DO NOT** use fallback defaults

**Forbidden:**
- ❌ Silent fallback
- ❌ Auto-correction
- ❌ Guesswork
- ❌ Default values (except for normalization)

**Example:**
```python
# ✅ CORRECT
if not signal:
    raise ValueError("Empty signal")

# ❌ FORBIDDEN
if not signal:
    signal = default_signal  # Auto-correction
    return default_energetic_state  # Fallback
```

---

## 🔗 Relationship with WM Controller

| Component | Knows About |
|-----------|-------------|
| **Perception** | ❌ WM Controller (does not know) |
| **WM Controller** | ✅ Energetic Output (receives output) |

**Data Flow:**
```
Perception Boundary
    ↓ (EnergeticState)
Trajectory Builder
    ↓ (Trajectory)
WM Controller
```

**Rules:**
- ✅ One-way only (Perception → WM Controller)
- ❌ Perception **MUST NOT** call WM Controller
- ❌ Perception **MUST NOT** know about WM Controller
- ❌ WM Controller **MUST NOT** call Perception

---

## 🛡️ Security & Safety Rationale

**Why this boundary is hard-locked:**

1. **Prevent Hallucination**
   - If Perception interprets meaning, false signals enter energy world
   - Hallucination propagates through entire system

2. **Prevent Semantic Leakage**
   - If Perception uses semantic rules, meaning leaks into energy computation
   - Kernel becomes contaminated

3. **Prevent Covert Policy**
   - If Perception applies policy, safety boundaries are bypassed
   - GateCore becomes ineffective

4. **Prevent Accidental Autonomy**
   - If Perception makes decisions, system acts without gate
   - Safety is compromised

**This layer is non-intelligent by design.**

---

## 🧪 Testability Requirements

### Mandatory Tests

All tests **MUST** verify:

- [ ] Same input → same EPS (determinism)
- [ ] Boundary does not write memory
- [ ] Boundary does not branch on meaning
- [ ] Boundary does not call other layers
- [ ] Boundary does not use randomness
- [ ] Boundary does not access external resources
- [ ] Boundary raises errors on invalid input (no silent fallback)

### Test Examples

```python
# Determinism test
def test_determinism():
    input_signal = "test signal"
    output1 = perception_boundary.process(input_signal)
    output2 = perception_boundary.process(input_signal)
    assert output1 == output2  # Must be identical

# Isolation test
def test_isolation():
    # Verify no imports from other layers
    assert "gate" not in perception_module.__imports__
    assert "memory" not in perception_module.__imports__
    assert "kernel" not in perception_module.__imports__
```

---

## 🔍 Audit Checklist

Auditor **SHOULD** verify:

### Code Inspection
- [ ] No imports from `gate/`
- [ ] No imports from `memory/`
- [ ] No imports from `reasoning/`
- [ ] No imports from `kernel/`
- [ ] No imports from `wm/` or `runtime/`
- [ ] No network calls
- [ ] No randomness (unless seeded)
- [ ] No global mutable state

### Function Inspection
- [ ] No semantic interpretation functions
- [ ] No classification functions
- [ ] No entity extraction functions
- [ ] No decision-making functions
- [ ] No memory access functions
- [ ] No trajectory creation functions

### Data Flow Inspection
- [ ] Input is read-only (not modified)
- [ ] Output is numeric only
- [ ] No side effects
- [ ] No external state modification

---

## 📋 Summary (LOCKED INTENT)

**Perception Boundary is:**
- ✅ Customs checkpoint of reality (gateway to energy world)
- ✅ Signal normalizer (scaling, alignment)
- ✅ Feature extractor (statistical, numerical)
- ✅ Energy projector (canonical formulas)

**Perception Boundary is NOT:**
- ❌ A translator (does not interpret)
- ❌ A thinker (does not think)
- ❌ A judge (does not decide)
- ❌ An AI (does not learn)

**If this boundary becomes "intelligent", the system is unsafe.**

---

## 📚 Related Specifications

- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **Energy Variables:** `docs/ENERGY_VARIABLE_SPEC.md`
- **Perception Mapping:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`
- **WM Controller:** `docs/WM_CONTROLLER_SPEC.md`
- **Memory Field Spec:** `docs/MEMORY_FIELD_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture approval
2. Safety approval
3. Version bump
4. Impact analysis (all downstream modules)

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on boundary violation)

**Violation Consequence:**
- Boundary breach
- System redesign required
- Cannot be patched

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent semantic contamination from entering energy world  
**Authority:** Core Team  
**Enforcement:** Code review + automated import checks

