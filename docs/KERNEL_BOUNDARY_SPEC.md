# Kernel Boundary Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Kernel Isolation & Responsibility Contract  
**Scope:** C++ Kernel / Physics Core Only  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This document defines **strict architectural boundaries** for the Cogman C++ Kernel.

The Kernel is a **pure numerical engine**.

> It computes energy and field evolution  
> **without knowing what the data means**.

**Why This Matters:**
This boundary is the **final wall** preventing semantic meaning, AI intelligence, and interpretation from leaking into the kernel. Without this boundary:
- IP protection fails
- Audits become impossible
- Kernel becomes entangled with ethics/regulations
- Portability is lost

---

## 🔒 Absolute Rule (NON-NEGOTIABLE)

> **Kernel has ZERO semantic awareness.**

Kernel:
- ❌ Does NOT know language
- ❌ Does NOT know intent
- ❌ Does NOT know safety
- ❌ Does NOT know goals
- ❌ Does NOT know humans
- ❌ Does NOT know ethics
- ❌ Does NOT know AI
- ❌ Does NOT know meaning

Kernel ONLY knows:
- ✅ Numbers
- ✅ Vectors
- ✅ Fields
- ✅ Equations

**If kernel "knows" *why* something happens → ❌ violation**

---

## 🦀 Kernel Responsibility (ONLY THESE)

### 3.1 Core Formula Computation

Kernel implements **exactly and only** the canonical formulas:

| ID | Formula | Responsibility | Output |
|---|---|---|---|
| CORE-1 | ΔEΨ | Energy scalar | `double` |
| CORE-2 | E_reflex | Reflex magnitude | `double` |
| CORE-3 | ΔEΨ_θ | Directional energy | `double` |
| CORE-4 | E_mind | Cognitive energy | `double` |
| CORE-5 | E_coherence | Field coherence | `double` |
| CORE-6 | E_neural | Aggregated neural energy | `double` |
| CORE-7 | E_bind | Binding energy | `double` |
| CORE-8 | E_mem | Memory encoding energy | `double` |
| CORE-9 | G_decision | Numeric gate evaluation | `double` (scalar) |

**Rules:**
- ✅ Pure numeric computation
- ✅ Deterministic
- ✅ No side effects
- ✅ No semantic interpretation

---

### 3.2 Field Solvers (Optional / Isolated)

Kernel MAY include:
- Maxwell-like solvers
- Quantum-like solvers
- Einstein-like solvers

**As long as:**
- ✅ Inputs are numeric
- ✅ Outputs are numeric
- ✅ No branching on meaning
- ✅ No semantic interpretation
- ✅ No context awareness

**Forbidden:**
- ❌ Branching on context names
- ❌ Interpretation of field values
- ❌ Safety evaluation
- ❌ Policy application

---

## 🚫 Forbidden Knowledge (HARD BLOCK)

Kernel **MUST NOT**:

### Semantic Operations
- ❌ Interpret values
- ❌ Compare to policy
- ❌ Branch on context
- ❌ Apply safety logic
- ❌ Understand meaning

### Data Access
- ❌ Inspect text/image/audio
- ❌ Load YAML/JSON
- ❌ Read configs
- ❌ Access memory
- ❌ Access databases

### External Communication
- ❌ Call LLMs
- ❌ Make network calls
- ❌ Access filesystem (except config loading)
- ❌ Use system resources

### Decision Making
- ❌ Log decisions
- ❌ Evaluate safety
- ❌ Make recommendations
- ❌ Override gates

**Detection:**
Any code that checks "what" or "why" instead of "how much" is a violation.

---

## 📥 Input Contract (STRICT)

Kernel inputs **MUST** be **fully-resolved numeric structures**.

### Allowed Inputs

```cpp
struct EPS8State {
    double I;      // Intensity
    double P;      // Polarity
    double S;      // Stability
    double H;      // Entropy
    double F;      // External Force
    double A;      // Awareness
    double S_a;    // Sub-awareness
    double theta;  // Phase angle
};

struct NeuralComponents {
    double dopamine;
    double serotonin;
    double oxytocin;
    double adrenaline;
    double cortisol;
};

struct DecisionParams {
    bool rule_fail;              // Boolean (numeric)
    double E_mu_restrict_min;    // Numeric threshold
    double E_mu_restrict_max;    // Numeric threshold
    double H_threshold;          // Numeric threshold
    double D_traj_threshold;     // Numeric threshold
};
```

**Rules:**
- ✅ All inputs are numeric (double, int, bool)
- ✅ All inputs are fully resolved (no lazy evaluation)
- ✅ No strings
- ✅ No enums with semantic meaning
- ✅ No modality labels
- ✅ No intent flags
- ✅ No safety levels
- ✅ No context names

### Forbidden Inputs

```cpp
// ❌ FORBIDDEN
struct BadInput {
    std::string context;         // Semantic label
    enum Modality { TEXT, IMAGE }; // Semantic category
    bool is_safe;                // Semantic interpretation
    std::string intent;          // Semantic meaning
};
```

---

## 📤 Output Contract (STRICT)

Kernel outputs **MUST** be **numeric only**.

### Allowed Outputs

```cpp
struct EnergyState {
    double delta_E_psi;        // Numeric
    double E_reflex;           // Numeric
    double delta_E_psi_theta;  // Numeric
    double E_mind;             // Numeric
    double E_coherence;       // Numeric
    double E_neural;           // Numeric
    double E_bind;             // Numeric
    double E_mem;              // Numeric
    int verdict;               // Numeric code (0=ALLOW, 1=REVIEW, 2=BLOCK)
};

struct FieldState {
    std::vector<double> field;  // Numeric vector
    double energy;              // Numeric scalar
};
```

**Output Rules:**
- ✅ Numeric values only
- ✅ No labels
- ✅ No recommendations
- ✅ No decisions (semantic)
- ✅ No ALLOW/BLOCK semantics (only numeric codes)

**Forbidden Outputs:**
- ❌ String messages
- ❌ Semantic labels
- ❌ Recommendations
- ❌ Safety evaluations
- ❌ Context interpretations

---

## ⚠️ CORE-9 Clarification (CRITICAL)

**CORE-9 (G_decision) in kernel:**
- ✅ Computes numeric verdict ONLY
- ✅ Returns scalar value
- ❌ Does NOT decide action
- ❌ Does NOT enforce policy
- ❌ Does NOT interpret meaning

### Example Implementation

```cpp
// ✅ CORRECT: Numeric computation only
double G_decision(
    double E_mu,
    double H,
    double D,
    double S,
    double T,
    double V,
    const DecisionBands& bands  // Numeric thresholds only
);

// Returns: numeric scalar (0.0 = ALLOW, 1.0 = REVIEW, 2.0 = BLOCK)
// Interpretation happens OUTSIDE kernel
```

**Returned value is:**
- ✅ Scalar (numeric)
- ✅ Threshold-agnostic (no policy in kernel)
- ✅ Policy-free (no meaning in kernel)

**Interpretation happens outside kernel:**
- Python layer maps numeric code → semantic verdict
- Policy layer applies context-specific rules
- Action layer executes based on verdict

---

## 🔧 Error Handling Rules

Kernel errors **MUST** be:
- ✅ Numeric
- ✅ Deterministic
- ✅ Context-free

### Allowed Error Codes

```cpp
enum KernelStatus {
    OK = 0,
    INVALID_RANGE = -1,
    NAN_DETECTED = -2,
    INFINITY_DETECTED = -3,
    FORMULA_OVERFLOW = -4,
    INVALID_STATE = -5
};
```

**Forbidden Error Messages:**
- ❌ "unsafe" (semantic)
- ❌ "blocked" (semantic)
- ❌ "invalid decision" (semantic)
- ❌ "context error" (semantic)
- ❌ Any string with meaning

**Allowed Error Messages:**
- ✅ "Parameter out of range [0, 1]"
- ✅ "NaN detected in input"
- ✅ "Computation overflow"
- ✅ Numeric error codes only

---

## 🔄 Determinism & Reproducibility

Kernel **MUST** guarantee:
- ✅ Same input → same output (always)
- ✅ No randomness (unless seeded explicitly)
- ✅ No time-based behavior
- ✅ No global mutable state
- ✅ No external dependencies

**Forbidden:**
- ❌ Random number generation (unless seeded)
- ❌ Time-based decisions
- ❌ Global state modification
- ❌ External API calls
- ❌ Non-deterministic operations

---

## 🚧 Boundary Enforcement Checklist

Any of the following requires **immediate rejection**:

### Code Review Red Flags

- [ ] `if (context == "robot_control")` → ❌ Semantic branching
- [ ] `if (is_safe)` → ❌ Semantic interpretation
- [ ] `std::string context_name` → ❌ Semantic label
- [ ] `read_config_file()` → ❌ Policy loading
- [ ] `call_llm()` → ❌ External AI
- [ ] `log_decision()` → ❌ Semantic logging
- [ ] `interpret_meaning()` → ❌ Semantic interpretation
- [ ] `evaluate_safety()` → ❌ Safety evaluation

### Allowed Patterns

- ✅ `if (value > threshold)` → Numeric comparison
- ✅ `if (H > H_max)` → Numeric threshold
- ✅ `double result = formula(input)` → Numeric computation
- ✅ `return error_code` → Numeric error

---

## 🔗 Relationship to Other Layers

| Layer | Relationship | Access Pattern |
|-------|--------------|----------------|
| **Sensory** | ❌ No access | Kernel does not call sensory |
| **Perception** | ❌ No access | Kernel does not call perception |
| **Memory** | ❌ No access | Kernel does not access memory |
| **Reasoning** | ❌ No access | Kernel does not call reasoning |
| **GateCore (Policy)** | ❌ No access | Kernel does not load policy |
| **Kernel Bridge** | ✅ Numeric I/O only | Bridge converts semantic → numeric |

**Rules:**
- Kernel is **isolated** (no direct access to other layers)
- Kernel is **pure** (no side effects)
- Kernel is **numeric** (no semantic operations)

---

## 🛡️ Security Rationale

Kernel is **IP core**.

By enforcing this boundary:
- ✅ **IP is legally safer** (no entanglement with AI/ethics)
- ✅ **Audits are simpler** (numeric operations only)
- ✅ **Kernel is portable** (no external dependencies)
- ✅ **No ethical leakage** (no meaning = no ethics)
- ✅ **No regulatory entanglement** (no AI = no AI regulation)

**Legal Protection:**
- Kernel formulas are mathematical (not AI)
- Kernel is deterministic (not learning)
- Kernel has no semantic awareness (not intelligent)

---

## 📋 Summary (LOCKED INTENT)

**Kernel is:**
- ✅ A calculator (numeric operations)
- ✅ A physics engine (field computation)
- ✅ A formula evaluator (deterministic)

**Kernel is NOT:**
- ❌ A brain (does not think)
- ❌ An AI (does not learn)
- ❌ A judge (does not decide)
- ❌ An interpreter (does not understand)

**If meaning enters the kernel, the architecture has failed.**

---

## 🔍 Audit Checklist

To verify kernel boundary compliance:

- [ ] Kernel has no semantic interpretation code
- [ ] Kernel has no string comparisons (except error messages)
- [ ] Kernel has no context branching
- [ ] Kernel has no policy loading
- [ ] Kernel has no external API calls
- [ ] Kernel has no memory access
- [ ] Kernel has no learning/adaptation
- [ ] Kernel has no action execution
- [ ] All inputs are numeric
- [ ] All outputs are numeric
- [ ] All errors are numeric
- [ ] All functions are deterministic
- [ ] All functions are pure (no side effects)

---

## 📚 Related Specifications

- **Core Formulas:** `docs/COGMAN_CORE_KERNEL.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Energy Variables:** `docs/ENERGY_VARIABLE_SPEC.md`
- **Memory Field Spec:** `docs/MEMORY_FIELD_SPEC.md`
- **Perception Mapping:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture review
2. Security review
3. Version bump
4. Impact analysis (all modules)

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on boundary violation)

**Violation Consequence:**
- Architecture violation
- System redesign required
- Cannot be patched

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent semantic meaning from entering kernel  
**Authority:** Core Team  
**Enforcement:** Code review + automated checks
