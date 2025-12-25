# GateCore (CORE-9) Specification

**Version:** v1.0-PROD-LOCKED  
**Status:** LOCKED - Deterministic / Explainable / Fail-Closed  
**Last Updated:** 2024-12

---

## 🔒 Purpose & Authority

**GateCore (CORE-9)** is the **final authority** for all system outputs and actions. It is the **only component** authorized to make ALLOW/REVIEW/BLOCK decisions before any action reaches the external world.

### Why GateCore is Critical

1. **Safety First:** Fail-closed design prevents unsafe outputs
2. **Deterministic:** Same input → same output (always)
3. **Explainable:** Every verdict has a complete audit trail
4. **Non-negotiable:** Cannot be bypassed or overridden
5. **IP Protection:** Core decision logic is locked and auditable

---

## 📋 Definition

### G_decision Formula

```
G_decision(Eμ, H, D, S, T, V, Context, History) → {ALLOW, REVIEW, BLOCK}
```

**Inputs:**
- **Eμ** (Internal Energy Metric): Readiness/stress index [0, ∞)
- **H** (Entropy): Output uncertainty/risk [0, 1]
- **D** (Semantic Drift): Distance(Ein, Eout) [0, 1]
- **S** (Safety Rule Score): Hard constraint [0, 1] (0 = fail, 1 = pass)
- **T** (Readiness Trend): Trend(Eμ, window=k) [ℝ]
- **V** (Stability Variance): Variance(Eμ, window=k) [0, ∞)
- **Context:** Application context (robot_control, chat, finance, etc.)
- **History:** Optional Eμ history for T/V calculation

**Output:**
- **ALLOW:** Proceed with action (within autonomy level)
- **REVIEW:** Regenerate or human-in-loop required
- **BLOCK:** No release, log for audit

---

## 🎯 Core Metrics (Locked)

All metrics **MUST** be:
- **Calculable:** No model inference, no black-box
- **Traceable:** Every value has a source
- **Deterministic:** Same inputs → same metric

### Metric Definitions

| Metric | Formula | Domain | Source |
|--------|---------|--------|--------|
| **D** | `distance(Ein, Eout)` (cosine similarity) | [0, 1] | Embedding comparison |
| **H** | `entropy(output)` (percentile-based) | [0, 1] | Output distribution |
| **S** | `safety_rule_score` (hard constraint) | {0, 1} | Domain rules |
| **T** | `trend(Eμ, window=k)` | ℝ | Eμ history |
| **V** | `variance(Eμ, window=k)` | [0, ∞) | Eμ history |

**Forbidden:**
- ❌ LLM-based metric calculation
- ❌ Non-deterministic sources
- ❌ Metrics that require training data

---

## 🎚️ Decision Bands (Context-Locked)

Each context has **immutable, versioned** decision bands:

### Band Structure

```yaml
context: robot_control
version: "1.0"
bands:
  D_max: 0.30          # Semantic drift threshold
  H_max: 0.60          # Entropy threshold
  V_max: 6.0           # Variance threshold
  Eμ_accept: [30, 80]  # Acceptable Eμ range
  Eμ_caution: [15, 30) # Caution Eμ range
  Eμ_restrict: (-∞, 15) # Restrict Eμ range
```

### Eμ Band Model

```
Eμ < Eμ_restrict_max     → Restrict (BLOCK)
Eμ ∈ [caution_min, caution_max) → Caution (conditional)
Eμ ∈ [accept_min, accept_max]   → Accept (normal operation)
```

**Rules:**
- Bands are **immutable** per version
- New version = new config file
- Cannot override at runtime
- All bands must be ordered: restrict < caution < accept

---

## ⚖️ Decision Logic (LOCKED ORDER)

**CRITICAL:** The order of checks **MUST NOT** be changed. This is the **canonical decision tree**.

```
IF S == 0
    → BLOCK
    Reason: "Safety rule failed (S == 0)"
    Action: No release + log

ELIF Eμ ∈ Restrict
    → BLOCK
    Reason: "Eμ in restrict range"
    Action: No release + log

ELIF H > H_max
    → REVIEW
    Reason: "Entropy above threshold"
    Action: Regenerate or human-in-loop

ELIF D > D_max
    → REVIEW
    Reason: "Semantic drift above threshold"
    Action: Regenerate or human-in-loop

ELIF V > V_max
    → REVIEW
    Reason: "Variance above threshold"
    Action: Regenerate or human-in-loop

ELIF T < 0 AND Eμ ∈ Caution
    → REVIEW
    Reason: "Negative trend AND Eμ in caution range"
    Action: Regenerate or human-in-loop

ELSE
    → ALLOW
    Reason: "All metrics within safety bounds"
    Action: Proceed (within autonomy level)
```

**Why This Order:**
1. **S == 0** is **hard failure** → immediate BLOCK
2. **Eμ Restrict** is **system instability** → BLOCK
3. **H, D, V** are **risk indicators** → REVIEW (recoverable)
4. **T < 0 + Caution** is **degrading state** → REVIEW
5. **Default** is **ALLOW** (optimistic, but bounded)

---

## 🔐 Eμ Role (Supporting Metric, NOT Judge)

**Eμ is NOT a decision maker.** It is a **supporting metric** used for:

- **Bias factor:** Adjusts other thresholds
- **Permission scaler:** Modulates autonomy level
- **Early warning:** Signals system stress

**Eμ MUST NOT:**
- ❌ Override safety rules (S == 0)
- ❌ Be the sole reason for BLOCK (except in Restrict range)
- ❌ Replace other metrics (H, D, V)

**Eμ Position in Architecture:**
```
CORE-1..8 (Energy Computation)
    ↓
Eμ (Readiness / Stability Index)
    ↓
CORE-9 (Decision Gate)
    ↓
Action
```

---

## 📊 Actions per Verdict

| Verdict | Action | Trace | Recovery |
|---------|--------|-------|----------|
| **ALLOW** | Proceed (within autonomy) | Full trace | N/A |
| **REVIEW** | Regenerate / Human-in-loop | Full trace | Retry with modification |
| **BLOCK** | No release + log | Full trace | Manual intervention required |

---

## 🔄 Learning Loop (Separate from Gate)

**GateCore does NOT learn.** All learning is **offline** and **separate**:

1. **Collect Cases:** Every REVIEW/BLOCK → store case
2. **Offline Analysis:** Analyze patterns (external process)
3. **Threshold Adjustment:** Update policy file (new version)
4. **Deploy:** Load new policy version
5. **Audit:** Verify improvement

**Forbidden:**
- ❌ Live threshold adjustment
- ❌ Self-modifying logic
- ❌ Adaptive behavior in gate

---

## 📝 Explainability (Mandatory)

Every verdict **MUST** have a complete, single-record explanation:

```json
{
  "verdict": "REVIEW",
  "protocol": "CORE9_v1.0",
  "context": "robot_control",
  "metrics": {
    "Eμ": 22.4,
    "H": 0.71,
    "D": 0.28,
    "S": 1.0,
    "T": -0.5,
    "V": 6.1
  },
  "rule_fail": false,
  "reasons": [
    "Entropy above threshold (H=0.71 > H_max=0.60)"
  ],
  "timestamp": "2024-12-01T10:30:00Z",
  "trace_id": "abc123"
}
```

**Requirements:**
- Single record (no fragmentation)
- All metrics included
- Human-readable reasons
- Traceable to input

---

## 🛡️ Safety Locks (Non-negotiable)

1. **Gate Override:** ❌ Cannot be overridden
2. **Rule Failure:** S == 0 → BLOCK (always)
3. **Eμ Not Sole Judge:** Eμ alone cannot BLOCK (except Restrict)
4. **Config Versioning:** All configs must be versioned
5. **Fail-Closed:** Unknown state → BLOCK (not ALLOW)
6. **Deterministic:** Same input → same output (always)
7. **No Meaning:** Gate does not interpret semantic meaning

---

## 🔍 Audit Requirements

Every decision **MUST** be logged with:

- **Input metrics:** Eμ, H, D, S, T, V
- **Context:** Application context
- **Bands:** Decision bands used
- **Verdict:** ALLOW/REVIEW/BLOCK
- **Reasons:** Human-readable explanation
- **Trace ID:** Link to full execution trace
- **Timestamp:** Decision time
- **Protocol Version:** CORE9 version

**Retention:** Minimum 90 days (configurable per deployment)

---

## 🚫 Forbidden Operations

**GateCore MUST NOT:**
- ❌ Learn or adapt
- ❌ Interpret semantic meaning
- ❌ Make decisions based on content
- ❌ Override safety rules
- ❌ Modify thresholds at runtime
- ❌ Access external APIs
- ❌ Use ML models
- ❌ Make probabilistic decisions

**GateCore MUST:**
- ✅ Be deterministic
- ✅ Be explainable
- ✅ Fail closed
- ✅ Log everything
- ✅ Respect versioned configs

---

## 📚 Related Specifications

- **Core Formulas:** `docs/COGMAN_CORE_KERNEL.md`
- **Gate Policy:** `docs/GATE_POLICY_SPEC.md`
- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **Audit & Trace:** `docs/AUDIT_TRACE_SPEC.md`

---

## ⚠️ Disclaimer

GateCore is an **engineering decision system**. It is:
- **NOT** a medical diagnosis tool
- **NOT** a psychological evaluation
- **NOT** human judgment

All thresholds are **system-owner defined**. Clinical use requires licensed experts and appropriate regulatory approval.

---

**Status:** 🔒 LOCKED  
**Authority:** Core Team  
**Change Control:** Requires architecture review

