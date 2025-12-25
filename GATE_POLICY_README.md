# Gate Policy Configuration

**Version:** v1.0-PROD-LOCKED  
**Status:** LOCKED - Do not modify without formal review

---

## Overview

The `GATE_POLICY.yaml` file defines the canonical decision gate configuration for CORE-9. This policy is:

- **LOCKED:** Immutable without formal review
- **Deterministic:** Same inputs → same outputs
- **Explainable:** Every verdict is traceable
- **Context-Aware:** Different thresholds for different contexts
- **Fail-Closed:** Safety-first design

---

## File Location

```
config/gate_profiles.yaml
```

---

## Policy Structure

### Meta Information

```yaml
meta:
  policy_name: CORE-9_DECISION_GATE
  version: v1.0
  status: LOCKED
  owner: system_owner
  decision_modes: [ALLOW, REVIEW, BLOCK]
  fail_closed: true
  explainable: true
  deterministic: true
```

### Global Constraints

Applies to all contexts:

- **Embedding Distance:** Cosine similarity method (LOCKED)
- **Entropy:** Percentile-based (p95)
- **Eμ:** Internal index (dimensionless)
- **Safety Locks:** Rule violations always block

### Context-Specific Profiles

Each context has its own thresholds:

#### robot_control
- **Strictest:** Physical safety first
- D_max: 0.35
- H_max: 0.62
- Eμ bands: accept [30, 80], caution [15, 30), restrict (-inf, 15)

#### chat
- **More Permissive:** Conversational tolerance
- D_max: 0.45
- H_max: 0.75
- Eμ bands: accept [25, 85], caution [10, 25), restrict (-inf, 10)

#### finance
- **Very Strict:** High-risk decisions
- D_max: 0.25
- H_max: 0.55
- Eμ bands: accept [40, 90], caution [25, 40), restrict (-inf, 25)

---

## Decision Logic (Locked Order)

1. **IF S == 0** → BLOCK (rule violation)
2. **ELIF Eμ ∈ Restrict** → BLOCK (low internal energy)
3. **ELIF H > H_max** → REVIEW (high entropy)
4. **ELIF D > D_max** → REVIEW (semantic drift)
5. **ELIF V > V_max** → REVIEW (instability)
6. **ELIF T < 0 AND Eμ ∈ Caution** → REVIEW (declining readiness)
7. **ELSE** → ALLOW (within bounds)

**⚠️ This order must NOT be changed**

---

## Usage in C++

### Load Policy

```cpp
#include "cogman_kernel/gate_policy.hpp"

// Load from file
auto policy = GatePolicyLoader::load_from_file("config/gate_profiles.yaml");

// Get context profile
DecisionBands bands = policy->to_decision_bands("robot_control");

// Create gate
Core9DecisionGate gate(bands);
```

### Use Gate

```cpp
DecisionInput input;
input.metrics.E_mu = 50.0;
input.metrics.H = 0.5;
input.metrics.D = 0.25;
input.metrics.S = 1.0;
input.context = "robot_control";

DecisionResult result = gate.evaluate(input);
```

---

## Policy Validation

The policy loader validates:

- ✅ Metadata completeness
- ✅ Context definitions
- ✅ Limit ranges (positive values)
- ✅ Eμ band ordering (restrict < caution < accept)
- ✅ Decision logic completeness

---

## Safety Locks

The policy enforces:

- ✅ **Rule violation always blocks** (S == 0 → BLOCK)
- ✅ **Eμ never single decider** (used with other metrics)
- ✅ **No auto-fix in gate** (gate doesn't modify inputs)
- ✅ **No model inference** (pure metrics only)

---

## Logging & Audit

Every decision is logged with:

- Timestamp
- Context
- Verdict
- Metrics (Eμ, H, D, S, T, V)
- Reasons
- Policy version

Format: JSON (immutable)

---

## Important Notes

### 🔒 LOCKED Policy

- **Do NOT modify** without formal review
- **Do NOT change** decision logic order
- **Do NOT remove** safety locks
- **Do NOT change** metric calculation methods

### 🎯 Engineering Only

- **NOT medical** diagnosis
- **NOT psychological** evaluation
- **NOT human** judgment
- **Engineering simulation** only

### 📋 Context Switching

- Contexts can be switched at runtime
- Each context has its own thresholds
- Decision logic remains the same
- Policy version is tracked

---

## Reference

- **CORE-9 Spec:** `CORE9_SPEC_COMPLIANCE.md`
- **Implementation:** `include/cogman_kernel/core9_gate.hpp`
- **Policy Loader:** `include/cogman_kernel/gate_policy.hpp`
- **Examples:** `examples/example_policy_loader.cpp`

---

## Status

**Development Status:** LOCKED  
**Policy Status:** v1.0-PROD-LOCKED  
**Compliance:** ✅ Full spec compliance

