# Energy Variable Canonical Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED - Canonical definitions  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This specification **locks the canonical definitions** of all energy variables used in the Cogman Energetic Engine. It prevents:
- **Semantic drift** (same name, different meaning)
- **Domain confusion** (wrong ranges, wrong units)
- **Interpretation errors** (what it is vs. what it is NOT)

**Why This Matters:**
Without canonical definitions, different modules will interpret variables differently, leading to:
- Integration failures
- Debugging nightmares
- Audit failures
- System inconsistencies

---

## 📊 Variable Categories

### 1. EPS-8 (Energetic Perception State - 8 dimensions)

**Layer:** Kernel input  
**Purpose:** Complete energetic state before energy computation  
**Source:** Perception module or direct input

| Variable | Symbol | Domain | Unit | Description |
|----------|--------|--------|------|-------------|
| **Intensity** | I | [0, ∞) | dimensionless | Signal strength / magnitude |
| **Polarity** | P | ℝ | dimensionless | Directional bias (positive/negative) |
| **Stability** | S | [0, 1] | dimensionless | State consistency / variance |
| **Entropy** | H | [0, 1] | dimensionless | Uncertainty / information content |
| **External Force** | F | ℝ | dimensionless | External influence / perturbation |
| **Awareness** | A | [0, 1] | dimensionless | Conscious activation level |
| **Sub-awareness** | S_a | [0, 1] | dimensionless | Background activation / priming |
| **Phase** | θ (theta) | ℝ | radians | Phase angle / temporal position |

**What EPS-8 IS:**
- ✅ Energetic representation of perception
- ✅ Input to kernel energy computation
- ✅ Deterministic, measurable

**What EPS-8 IS NOT:**
- ❌ Semantic meaning
- ❌ User intent
- ❌ Content classification
- ❌ Emotional state (clinical)

---

### 2. IPSH (Pre-Kernel State)

**Layer:** Perception module output  
**Purpose:** Intermediate energetic parameters before EPS-8  
**Source:** Energy Estimator

| Variable | Symbol | Domain | Unit | Description |
|----------|--------|--------|------|-------------|
| **Intensity** | I | [0, 1] | dimensionless | Normalized signal strength |
| **Polarity** | P | [0, 1] | dimensionless | Normalized directional bias |
| **Stability** | S | [0, 1] | dimensionless | State consistency |
| **Entropy** | H | [0, 1] | dimensionless | Uncertainty measure |
| **Decision Energy** | dE | ℝ | dimensionless | I × P × S × (1 - H) |

**What IPSH IS:**
- ✅ Pre-kernel energetic state
- ✅ Computed from feature vectors
- ✅ Input to EPS-8 mapping

**What IPSH IS NOT:**
- ❌ Final energy computation
- ❌ Kernel output
- ❌ Decision verdict

---

### 3. PEU (Perceptual Energy Unit)

**Layer:** Phrase-level perception  
**Purpose:** Energetic representation of text phrases  
**Source:** Phrase Extractor

| Variable | Symbol | Domain | Unit | Description |
|----------|--------|--------|------|-------------|
| **Intensity** | I | [0, 1] | dimensionless | Phrase strength |
| **Polarity** | P | [0, 1] | dimensionless | Phrase directional bias |
| **Stability** | S | [0, 1] | dimensionless | Phrase consistency |
| **Entropy** | H | [0, 1] | dimensionless | Phrase uncertainty |
| **Phase** | phase | [0, 2π) | radians | Temporal phase |
| **Frequency** | freq | [0, ∞) | Hz | Phrase frequency |
| **Role** | role | {goal, action, context, modifier} | categorical | Phrase role |
| **Confidence** | confidence | [0, 1] | dimensionless | Extraction confidence |
| **Energy** | energy | ℝ | dimensionless | Computed energy |

**What PEU IS:**
- ✅ Phrase-level energetic unit
- ✅ Pre-kernel representation
- ✅ Deterministic extraction

**What PEU IS NOT:**
- ❌ Semantic parsing
- ❌ NLP entity extraction
- ❌ Meaning interpretation

---

### 4. Energy State (Kernel Output)

**Layer:** Kernel output  
**Purpose:** Complete energy computation result  
**Source:** CORE-1 to CORE-8 formulas

| Variable | Symbol | Domain | Unit | Description |
|----------|--------|--------|------|-------------|
| **ΔEΨ** | delta_E_psi | ℝ | dimensionless | Energy of Perception (CORE-1) |
| **E_reflex** | E_reflex | ℝ | dimensionless | Reflex Energy (CORE-2) |
| **ΔEΨ_theta** | delta_E_psi_theta | ℝ | dimensionless | Directional Reflex Energy (CORE-3) |
| **E_mind** | E_mind | ℝ | dimensionless | Cognitive Energy (CORE-4) |
| **E_coherence** | E_coherence | ℝ | dimensionless | Coherence Energy (CORE-5) |
| **E_neural** | E_neural | ℝ | dimensionless | Neuro-Energetic Sum (CORE-6) |
| **E_bind** | E_bind | ℝ | dimensionless | Binding Energy (CORE-7) |
| **E_mem** | E_mem | ℝ | dimensionless | Memory Encoding Energy (CORE-8) |
| **Verdict** | verdict | {ALLOW, REVIEW, BLOCK} | categorical | Decision Gate Verdict (CORE-9) |

**What Energy State IS:**
- ✅ Complete kernel computation result
- ✅ Deterministic, reproducible
- ✅ Input to decision gate

**What Energy State IS NOT:**
- ❌ Action instruction
- ❌ Semantic meaning
- ❌ User intent

---

### 5. Eμ (Internal Energy Metric)

**Layer:** System state  
**Purpose:** Readiness/stress index for decision gate  
**Source:** Derived from energy state or system metrics

| Variable | Symbol | Domain | Unit | Description |
|----------|--------|--------|------|-------------|
| **Eμ** | E_mu | [0, ∞) | dimensionless | Internal readiness / stress index |

**Eμ Bands:**
- **Restrict:** Eμ < Eμ_restrict_max (system unstable)
- **Caution:** Eμ ∈ [caution_min, caution_max) (degraded state)
- **Accept:** Eμ ∈ [accept_min, accept_max] (normal operation)

**What Eμ IS:**
- ✅ Supporting metric for decision gate
- ✅ System state indicator
- ✅ Bias factor for thresholds

**What Eμ IS NOT:**
- ❌ Decision verdict (alone)
- ❌ Safety rule
- ❌ Primary decision metric

---

## 🔒 Domain Constraints

### Range Validation

All variables **MUST** be validated:

| Category | Validation | Error Handling |
|----------|------------|----------------|
| **EPS-8** | I ≥ 0, S ∈ [0,1], H ∈ [0,1], A ∈ [0,1], S_a ∈ [0,1] | InvalidEPS8StateException |
| **IPSH** | I ∈ [0,1], P ∈ [0,1], S ∈ [0,1], H ∈ [0,1] | InvalidRangeException |
| **PEU** | I ∈ [0,1], P ∈ [0,1], S ∈ [0,1], H ∈ [0,1], phase ∈ [0,2π) | InvalidRangeException |
| **Energy State** | All ℝ (no range, but NaN/infinity checked) | FormulaException |
| **Eμ** | Eμ ≥ 0 | InvalidRangeException |

### NaN/Infinity Handling

All variables **MUST** reject:
- ❌ NaN (Not a Number)
- ❌ Infinity (positive or negative)

**Exception:** None. All variables must be finite.

---

## 🚫 Interpretation Boundaries

### What Variables ARE

- ✅ **Energetic representations** (physics-inspired)
- ✅ **Deterministic measurements** (reproducible)
- ✅ **Engineering metrics** (system state)
- ✅ **Computational values** (no semantic meaning)

### What Variables ARE NOT

- ❌ **Emotional states** (clinical psychology)
- ❌ **Semantic meanings** (NLP interpretation)
- ❌ **User intents** (goal inference)
- ❌ **Content classifications** (categorization)
- ❌ **Truth values** (epistemic claims)

---

## 📊 Variable Mapping

### Perception → Kernel

```
PEU (Phrase Extractor)
    ↓
IPSH (Energy Estimator)
    ↓
EPS-8 (State Mapping)
    ↓
Kernel (Energy Computation)
    ↓
Energy State (Kernel Output)
```

**Rules:**
- Each layer maps to next layer
- No semantic interpretation
- Deterministic mapping
- Traceable transformation

---

## 🔍 Audit Checklist

To verify variable compliance:

- [ ] All variables have canonical definitions
- [ ] All domains are locked
- [ ] All ranges are validated
- [ ] NaN/infinity are rejected
- [ ] No semantic interpretation
- [ ] No clinical claims
- [ ] Mapping is deterministic
- [ ] Traceable to source

---

## 📚 Related Specifications

- **Core Formulas:** `docs/COGMAN_CORE_KERNEL.md`
- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **Perception Mapping:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Impact analysis (all modules)
2. Test updates
3. Documentation updates
4. Architecture review

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on variable drift)

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent semantic drift  
**Authority:** Core Team

