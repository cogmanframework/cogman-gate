# Memory Field Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Responsibility & Boundary Definition  
**Scope:** All Memory Modules (episodic, semantic, procedural, identity)  
**Last Updated:** 2024-12

---

## 🎯 Purpose

Memory Fields in Cogman Energetic Engine are **passive storage and retrieval systems**.

They exist to:
- Store energetic traces
- Provide resonance-based recall
- Preserve historical state

They **do NOT think, decide, plan, or act**.

---

## 🔒 Core Principle (NON-NEGOTIABLE)

> **Memory has NO authority.**

Memory:
- ❌ Cannot initiate actions
- ❌ Cannot modify trajectories
- ❌ Cannot override gates
- ❌ Cannot evaluate safety
- ❌ Cannot compute decisions

Only:
- **Working Memory Controller (WM)**
- **GateCore (CORE-9)**

may **interpret or act** on memory outputs.

---

## 📊 Memory Model Overview

```
[ WM Controller ]
    ↓ (query)
[ Memory Field ]  ← passive
    ↓ (resonance only)
[ Memory Result ]
```

**Memory is:**
- ✅ Reactive (responds to queries)
- ✅ Deterministic (same query → same result)
- ✅ Side-effect free on recall

**Memory is NOT:**
- ❌ Proactive (does not initiate)
- ❌ Authoritative (does not decide)
- ❌ Active (does not execute)

---

## 🗂️ Memory Field Types

### 4.1 Episodic Field

**Purpose:**  
Store concrete past trajectories and events.

**Stores:**
- EPS-8 snapshots
- Trajectory fragments
- Timestamps
- Trace ID references

**Recall Mechanism:**
```
resonance = f(A, |Eμ|, phase_alignment)
```

**Constraints:**
- ❌ No abstraction
- ❌ No generalization
- ❌ No planning
- ❌ No decision-making

**Write Policy:**
- ✅ End of trajectory
- ✅ After gate evaluation
- ❌ During kernel computation
- ❌ During gate evaluation

---

### 4.2 Semantic / Principle Field

**Purpose:**  
Store stabilized patterns extracted offline (sleep/consolidation).

**Stores:**
- Verified energetic patterns (Sₙ)
- Stability & frequency metadata
- Pattern signatures
- Consolidation timestamps

**Verification Rule (Canonical):**
```
Σ resonance_i ≥ threshold
AND phase_alignment ≥ φ_min
```

**Constraints:**
- ❌ Cannot learn online
- ❌ Can only be written by consolidation engine
- ❌ Recall is boolean + score only
- ❌ No semantic interpretation

**Write Policy:**
- ✅ Consolidation only (offline)
- ✅ After pattern verification
- ❌ During runtime
- ❌ During gate evaluation

---

### 4.3 Procedural / Action Field

**Purpose:**  
Store action-affordance associations.

**Stores:**
- State → action mappings
- Hebbian-style weight matrices
- Action outcome history
- Success/failure statistics

**Learning Rule (Offline / Controlled):**
```
ΔW_ij = η · x_i · x_j
```

**Constraints:**
- ❌ Cannot execute actions
- ❌ Cannot trigger behavior
- ❌ Provides likelihood only
- ❌ No action authority

**Write Policy:**
- ✅ Verified action outcome (offline)
- ✅ After action completion
- ❌ During action execution
- ❌ During gate evaluation

---

### 4.4 Identity Field

**Purpose:**  
Maintain long-term system identity and invariants.

**Stores:**
- Baselines
- Operating ranges
- Versioned calibration data
- System configuration history

**Constraints:**
- ✅ Read-heavy (frequent reads)
- ✅ Write only via controlled calibration
- ❌ Never queried for decisions directly
- ❌ No runtime modification

**Write Policy:**
- ✅ Manual calibration only
- ✅ Versioned updates
- ❌ Automatic modification
- ❌ Runtime changes

---

## 🔌 Query Interface (STRICT)

All memory access **MUST** use a Query Object.

### MemoryQuery Structure

```python
@dataclass
class MemoryQuery:
    eps8: EPS8State          # Query state
    query_type: Literal[
        "episodic",
        "semantic",
        "procedural",
        "identity"
    ]
    resonance_params: Dict[str, Any]  # Resonance parameters
    trace_id: str            # Trace ID for audit
    timestamp: float         # Query timestamp
```

**Mandatory Rules:**
- ❌ No raw data queries
- ❌ No free-form search
- ❌ No cross-field implicit queries
- ❌ No direct database access
- ✅ All queries via Query Object
- ✅ All queries logged

---

## 📤 Memory Result Contract

### MemoryResult Structure

```python
@dataclass
class MemoryResult:
    resonance_score: float        # [0, 1]
    memory_entry: Optional[Any]   # Retrieved entry (if any)
    metadata: Dict[str, Any]     # Additional metadata
    trace_id: str                 # Trace ID
    timestamp: float              # Result timestamp
```

**Guarantees:**
- ✅ No commands
- ✅ No actions
- ✅ No recommendations
- ✅ Only data + score
- ✅ Deterministic (same query → same result)

**What MemoryResult IS:**
- ✅ Data retrieval result
- ✅ Resonance score
- ✅ Metadata

**What MemoryResult IS NOT:**
- ❌ Action instruction
- ❌ Decision verdict
- ❌ Safety evaluation
- ❌ Semantic interpretation

---

## ✍️ Write Policy (CRITICAL)

### Allowed Writes

| Field | Write Condition | Authority |
|-------|----------------|-----------|
| **Episodic** | End of trajectory | WM Controller |
| **Semantic** | Consolidation only | Consolidation Engine |
| **Procedural** | Verified action outcome | Action Verifier |
| **Identity** | Manual calibration | System Admin |

### Forbidden Writes

Memory **MUST NOT** be written:
- ❌ During gate evaluation
- ❌ During kernel computation
- ❌ During reasoning
- ❌ During action execution
- ❌ By unauthorized modules

**Enforcement:**
- Write locks during critical operations
- Audit trail for all writes
- Version control for all changes

---

## 🔍 Determinism & Traceability

Every memory operation **MUST** log:

```json
{
  "trace_id": "abc123",
  "memory_field": "episodic",
  "operation": "recall",
  "query": {
    "eps8": {...},
    "query_type": "episodic",
    "resonance_params": {...}
  },
  "result": {
    "resonance_score": 0.73,
    "memory_entry_id": "mem_001"
  },
  "timestamp": "2024-12-01T10:30:00Z",
  "version": "v1.0"
}
```

**Requirements:**
- ✅ All operations logged
- ✅ Trace ID linkage
- ✅ Version tracking
- ✅ Timestamp precision
- ✅ Audit trail completeness

---

## 🚫 Anti-Pattern Safeguards

The following are **explicit violations**:

### Architecture Violations

1. **Memory selecting actions**
   - ❌ Memory → Action (direct)
   - ✅ Memory → WM Controller → Action (mediated)

2. **Memory ranking decisions**
   - ❌ Memory → Decision (direct)
   - ✅ Memory → GateCore → Decision (mediated)

3. **Memory overriding GateCore**
   - ❌ Memory verdict > GateCore verdict
   - ✅ GateCore is final authority

4. **Memory triggering reflex**
   - ❌ Memory → Reflex (direct)
   - ✅ Memory → WM Controller → Reflex (mediated)

5. **Memory acting as planner**
   - ❌ Memory → Plan (direct)
   - ✅ Memory → Reasoning → Plan (mediated)

**Detection:**
- Code review checklist
- Runtime monitoring
- Architecture audit

**Consequence:**
- Architecture violation
- System redesign required
- Cannot be patched

---

## 🔗 Relationship to Other Modules

| Module | Relationship | Access Pattern |
|--------|--------------|----------------|
| **Kernel** | No direct access | Memory does not call kernel |
| **GateCore** | Read-only influence | GateCore queries memory (if needed) |
| **Reasoning** | Input only | Reasoning reads memory, does not write |
| **WM Controller** | Sole orchestrator | WM Controller manages all memory access |
| **LLM** | Annotation only | LLM annotates memory, does not modify |
| **Perception** | No direct access | Perception does not access memory |
| **Action** | No direct access | Action does not access memory |

**Rules:**
- Memory is **passive** (does not initiate)
- Memory is **reactive** (responds to queries)
- Memory is **non-authoritative** (does not decide)

---

## 🛡️ Security & Safety Notes

### Memory Content Safety

- **Memory content is non-authoritative**
  - Corrupted memory cannot force action
  - Invalid memory cannot override gate
  - Memory is advisory only

### Memory Access Safety

- **All memory influence is mediated by GateCore**
  - Memory → GateCore → Decision
  - No direct memory → action path
  - All paths are auditable

### Memory Integrity

- **Memory corruption detection**
  - Checksums on all entries
  - Version validation
  - Consistency checks

- **Memory isolation**
  - Each field is isolated
  - No cross-field contamination
  - Fail-safe on corruption

---

## 📋 Summary (Locked Intent)

**Memory in Cogman is:**
- ✅ A field (storage and retrieval)
- ✅ Passive (reactive only)
- ✅ Deterministic (reproducible)
- ✅ Non-authoritative (advisory only)

**Memory in Cogman is NOT:**
- ❌ A mind (does not think)
- ❌ A judge (does not decide)
- ❌ An agent (does not act)
- ❌ A planner (does not plan)

**If memory ever decides, the system is broken.**

---

## 🔍 Audit Checklist

To verify memory compliance:

- [ ] Memory has no action execution code
- [ ] Memory has no decision logic
- [ ] Memory has no gate override
- [ ] Memory has no semantic interpretation
- [ ] All memory access via Query Object
- [ ] All memory operations logged
- [ ] Memory writes are controlled
- [ ] Memory is passive (reactive only)
- [ ] Memory results are non-authoritative
- [ ] Memory influence is mediated

---

## 📚 Related Specifications

- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Energy Variables:** `docs/ENERGY_VARIABLE_SPEC.md`
- **Perception Mapping:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architectural review
2. Version bump
3. Backward compatibility audit
4. Impact analysis (all modules)

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on boundary violation)

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent memory from becoming authoritative  
**Authority:** Core Team

