# Working Memory Controller Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Central Control Unit  
**Scope:** Runtime Orchestration / Control Plane  
**Last Updated:** 2024-12

---

## 🎯 Purpose

Working Memory Controller (WM Controller) is the **central control unit** of the entire system.

**Architectural Analogy:**
- CPU / Scheduler / Router
- **NOT** a human brain
- **NOT** an AI
- **NOT** a semantic interpreter
- **NOT** an ethical judge

> WM Controller = Controls "flow", not "truth"

**Why This Matters:**
WM Controller is the **orchestration layer** that coordinates all system components without making semantic decisions or interpreting meaning.

---

## 🔒 Core Responsibility (ONLY THESE)

WM Controller has **exactly 5 responsibilities**:

1. **Gate Control** (pass / block)
2. **Routing** (where to go next)
3. **Context Modulation** (minor energy adjustment)
4. **Memory Resonance Invocation** (call memory)
5. **Navigation Decision** (select system path)

**WM Controller does NOT:**
- ❌ Create new energy formulas
- ❌ Modify kernel output
- ❌ Write trajectories from scratch
- ❌ Decide instead of GateCore
- ❌ Call LLM for "thinking"
- ❌ Write memory directly
- ❌ Override safety rules

---

## 📊 Position in Architecture

```
Trajectory
    ↓
WM Controller   ← YOU ARE HERE
    ↓
┌───────────────┬───────────────┬───────────────┐
Memory Fields   Kernel           Reasoning       Action
```

**WM Controller:**
- ✅ Calls everything
- ✅ Orchestrates all components
- ❌ **NO component calls WM Controller** (except runtime loop)

**Isolation:**
- WM Controller is **top-level orchestrator**
- Only runtime loop invokes WM Controller
- WM Controller does not know it is being called

---

## 📥 Input Contract (STRICT)

### Required Input

```python
@dataclass
class Trajectory:
    states: List[EPS8State]      # State history
    trace_id: str                 # Trace identifier
    source_modality: str          # Input modality (numeric code)
    timestamp: float              # Creation timestamp
    debug_lineage: Dict[str, Any] # Debug information
```

**Rules:**
- ✅ Use only `states[-1]` as current state
- ❌ **MUST NOT** modify past states
- ❌ **MUST NOT** reorder states
- ❌ **MUST NOT** delete states
- ✅ All states must be traceable

**State Immutability:**
- Past states are **read-only**
- Only append new states
- No retroactive modification

---

## 📤 Output Contract (STRICT)

### WMControllerOutput Structure

```python
@dataclass
class WMControllerOutput:
    trajectory: Trajectory                    # Updated trajectory
    navigation_decision: str                 # Navigation choice
    modulated_eps8: EPS8State                # Context-modulated state
    resonance_scores: Dict[str, float]       # Memory resonance scores
    gate_status: Dict[str, bool]             # Gate pass/fail status
    trace_id: str                            # Trace identifier
    timestamp: float                         # Output timestamp
```

### Allowed Navigation Decisions

| Decision | Purpose | Condition |
|----------|---------|-----------|
| `CREATE_NEW_SN` | Create new semantic node | No strong resonance |
| `EXTEND_PATH` | Extend existing path | Episodic resonance > 0.7 |
| `RECALL_SN` | Recall semantic node | Principle resonance > 0.8 |
| `TRIGGER_ACTION` | Trigger action | I > 0.8 AND S > 0.7 |
| `ACTIVATE_REFLEX` | Activate reflex | H < 0.2 |
| `BLOCKED` | Block execution | Gate failed |

**Rules:**
- ✅ Only one decision per cycle
- ✅ Deterministic (no randomness)
- ✅ No blending (single path)
- ✅ No probabilistic choice

---

## 🚧 Gate Control Layer (FIRST STEP)

WM Controller **MUST** call gates **before** any other operation.

### Required Gates

| Gate | Purpose | Threshold Source |
|------|---------|------------------|
| **Entropy Gate** | Prevent noise / hallucination | Config (H_max) |
| **Safety Gate** | Policy / domain constraint | Config (S_min) |
| **Budget Gate** | Resource / rate / cost | Config (budget_max) |

### Gate Logic

```python
if H > H_max:
    → BLOCKED (entropy gate failed)
if safety_fail:
    → BLOCKED (safety gate failed)
if budget_exceeded:
    → BLOCKED (budget gate failed)
```

**Critical Rules:**
- ❌ WM Controller **MUST NOT** define thresholds itself
- ✅ Use values from config **ONLY**
- ❌ **MUST NOT** override gate verdicts
- ❌ **MUST NOT** reinterpret gate results

**Gate Order:**
1. Entropy Gate (first)
2. Safety Gate (second)
3. Budget Gate (third)

**If any gate fails → BLOCKED (no further processing)**

---

## 🔗 Resonance Routing (Memory Invocation)

WM Controller is the **sole authority** for invoking memory.

### Canonical Resonance Formula

```
Res(S, M) = cosine(S.vector, M.vector) × e^(-|θ_s - θ_m|)
```

Where:
- `S` = Current state vector
- `M` = Memory entry vector
- `θ_s` = State phase
- `θ_m` = Memory phase

### Memory Types

| Type | Purpose | Access Pattern |
|------|---------|----------------|
| **Episodic** | Concrete past events | Read-only |
| **Semantic / Principle** | Stabilized patterns | Read-only |
| **Procedural** | Action-affordance mappings | Read-only |
| **Identity** | System baselines | Read-only |

**WM Controller Rules:**
- ✅ Calls memory via Query Object
- ✅ Receives resonance scores only
- ❌ **MUST NOT** interpret memory content
- ❌ **MUST NOT** modify memory
- ❌ **MUST NOT** write memory directly

**Memory Invocation:**
```python
# WM Controller calls memory
memory_query = MemoryQuery(
    eps8=current_state,
    query_type="episodic",
    resonance_params={"threshold": 0.5},
    trace_id=trace_id
)

memory_result = memory_adapter.query(memory_query)
resonance_score = memory_result.resonance_score  # Use score only
```

---

## 🎚️ Context Modulation (VERY LIMITED)

WM Controller **MAY** adjust EPS8 state **slightly** for context.

### Allowed Modulation

```python
S' = S × context_gain  # Stability modulation only
```

Where:
- `context_gain` ∈ [0.9, 1.1] (small adjustment)
- Only affects `S` (Stability)
- All other parameters unchanged

### Forbidden Modulation

- ❌ **MUST NOT** re-encode
- ❌ **MUST NOT** recompute entropy
- ❌ **MUST NOT** touch polarity (P)
- ❌ **MUST NOT** touch phase (θ)
- ❌ **MUST NOT** modify Intensity (I)
- ❌ **MUST NOT** modify Awareness (A)

### Clamping Rules

All modulated values **MUST** be clamped to valid ranges:
- `S'` ∈ [0, 1] (after modulation)
- All other values unchanged

**Rationale:**
Context modulation is **minimal** and **reversible**. It does not change the fundamental energetic state.

---

## 🧭 Navigation Decision Logic

WM Controller selects **exactly one route** per cycle.

### Canonical Navigation Logic

```python
if principle_resonance > 0.8:
    navigation_decision = "RECALL_SN"
elif episodic_resonance > 0.7:
    navigation_decision = "EXTEND_PATH"
elif I > 0.8 and S > 0.7:
    navigation_decision = "TRIGGER_ACTION"
elif H < 0.2:
    navigation_decision = "ACTIVATE_REFLEX"
else:
    navigation_decision = "CREATE_NEW_SN"
```

**Rules:**
- ✅ Deterministic (same input → same output)
- ✅ No blending (single path only)
- ✅ No probabilistic choice
- ✅ No randomness
- ✅ Config-driven thresholds

**Forbidden:**
- ❌ Probabilistic routing
- ❌ Multi-path execution
- ❌ Adaptive thresholds
- ❌ Learning-based routing

---

## 📝 Trajectory Handling Rules

### Allowed Operations

- ✅ Append new state to trajectory
- ✅ Read past states (read-only)
- ✅ Create new trajectory
- ✅ Extend existing trajectory

### Forbidden Operations

- ❌ **MUST NOT** delete states
- ❌ **MUST NOT** reorder states
- ❌ **MUST NOT** modify past states
- ❌ **MUST NOT** merge trajectories
- ❌ **MUST NOT** split trajectories

### Traceability

Every state **MUST** be traceable:
- ✅ Trace ID linkage
- ✅ Timestamp precision
- ✅ State lineage
- ✅ Source identification

---

## 🔗 Relationship with GateCore

| Component | Role |
|-----------|------|
| **GateCore** | Decides ALLOW / REVIEW / BLOCK |
| **WM Controller** | Uses verdict for routing |

**WM Controller Rules:**
- ✅ Calls GateCore for decision
- ✅ Uses verdict for routing
- ❌ **MUST NOT** override GateCore
- ❌ **MUST NOT** reinterpret verdict
- ❌ **MUST NOT** bypass GateCore

**Data Flow:**
```
WM Controller
    ↓ (metrics)
GateCore (CORE-9)
    ↓ (verdict: ALLOW/REVIEW/BLOCK)
WM Controller
    ↓ (routing based on verdict)
Action / Memory / Reasoning
```

---

## 🔗 Relationship with Kernel

**WM Controller:**
- ✅ Sends EPS8 → Kernel
- ✅ Receives numeric output
- ✅ Uses output for routing

**Kernel:**
- ❌ Does NOT know WM Controller
- ❌ Does NOT know trajectory
- ❌ Does NOT know memory
- ❌ Does NOT know context

**Isolation:**
- Kernel is **pure numeric engine**
- WM Controller is **orchestration layer**
- No semantic leakage between layers

---

## 📊 Logging & Traceability (MANDATORY)

Every decision **MUST** be logged:

```json
{
  "trace_id": "abc123",
  "wm_step": 12,
  "navigation": "RECALL_SN",
  "gates": {
    "entropy": true,
    "safety": true,
    "budget": true
  },
  "resonance": {
    "principle": 0.82,
    "episodic": 0.31,
    "procedural": 0.15,
    "identity": 0.95
  },
  "modulated_eps8": {
    "I": 0.75,
    "P": 0.60,
    "S": 0.68,
    "H": 0.25
  },
  "timestamp": "2024-12-01T10:30:00Z",
  "version": "v1.0"
}
```

**Requirements:**
- ✅ All decisions logged
- ✅ All gate results logged
- ✅ All resonance scores logged
- ✅ All navigation choices logged
- ✅ Trace ID linkage
- ✅ Version tracking

---

## 🔄 Determinism Guarantee

WM Controller **MUST** guarantee:
- ✅ Deterministic (same input → same output)
- ✅ Reproducible (no randomness)
- ✅ Config-driven (no hardcoded logic)
- ✅ Stateless (except trajectory reference)

**Forbidden:**
- ❌ Random number generation
- ❌ Time-based decisions
- ❌ Global mutable state
- ❌ Non-deterministic operations

---

## 🛡️ Security & Audit Rationale

**WM Controller is:**
- ✅ **Easiest audit point** (central control)
- ✅ **Autonomy control point** (human-in-the-loop)
- ✅ **Security boundary** (separate from kernel)

**Separation from Kernel:**
- ✅ Prevents regulatory risk
- ✅ Prevents semantic leakage
- ✅ Prevents IP contamination
- ✅ Enables independent audit

**Why This Matters:**
WM Controller can be audited and modified without touching the locked kernel.

---

## 🚫 Anti-Pattern Safeguards

The following are **explicit violations**:

### Architecture Violations

1. **WM Controller creating formulas**
   - ❌ WM Controller → New formula
   - ✅ WM Controller → Use existing formulas only

2. **WM Controller overriding GateCore**
   - ❌ WM Controller → Override verdict
   - ✅ WM Controller → Use GateCore verdict

3. **WM Controller interpreting memory**
   - ❌ WM Controller → Interpret memory content
   - ✅ WM Controller → Use resonance scores only

4. **WM Controller writing memory**
   - ❌ WM Controller → Write memory directly
   - ✅ WM Controller → Delegate to memory module

5. **WM Controller making semantic decisions**
   - ❌ WM Controller → Semantic interpretation
   - ✅ WM Controller → Numeric routing only

**Detection:**
- Code review checklist
- Runtime monitoring
- Architecture audit

**Consequence:**
- Architecture violation
- System redesign required
- Cannot be patched

---

## 📋 Summary (LOCKED INTENT)

**WM Controller is:**
- ✅ Traffic controller (orchestrates flow)
- ✅ Router (selects paths)
- ✅ Scheduler (coordinates components)

**WM Controller is NOT:**
- ❌ A thinker (does not think)
- ❌ A judge (does not decide policy)
- ❌ A semantic interpreter (does not understand meaning)
- ❌ An AI (does not learn)

**If WM Controller becomes "intelligent", the system becomes dangerous.**

---

## 🔍 Audit Checklist

To verify WM Controller compliance:

- [ ] WM Controller has no formula creation
- [ ] WM Controller has no gate override
- [ ] WM Controller has no memory interpretation
- [ ] WM Controller has no memory writing
- [ ] WM Controller has no semantic decisions
- [ ] All gates called before other operations
- [ ] All navigation decisions are deterministic
- [ ] All operations are logged
- [ ] All trajectories are traceable
- [ ] Context modulation is minimal
- [ ] Memory invocation is read-only
- [ ] Kernel interaction is numeric only

---

## 📚 Related Specifications

- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Memory Field Spec:** `docs/MEMORY_FIELD_SPEC.md`
- **Energy Variables:** `docs/ENERGY_VARIABLE_SPEC.md`
- **Perception Mapping:** `docs/PERCEPTUAL_ENERGY_MAPPING_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture review
2. Safety review
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
**Purpose:** Define central control unit boundaries  
**Authority:** Core Team  
**Enforcement:** Code review + runtime monitoring

