# Runtime Loop Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Deterministic Execution Loop  
**Scope:** System Orchestration & Lifecycle Control  
**Last Updated:** 2024-12

---

## 🎯 Purpose

Runtime Loop is the **system execution mechanism**.

It is **NOT** thinking.  
It is **NOT** deciding.  
It is **NOT** evaluating.

The **only responsibility** of Runtime Loop is:

> **Call modules in correct order  
> Control timing  
> Control lifecycle  
> Control isolation**

**Why This Matters:**
Runtime Loop is the "railway track" of the system. If it becomes "intelligent" or makes decisions, the system fails silently.

---

## 🔒 Core Principle (HARD RULE)

Runtime Loop **MUST** be:

- ✅ Deterministic (same input → same execution)
- ✅ Single-directional (no backtracking)
- ✅ Non-cognitive (no thinking)
- ✅ Non-adaptive (no learning)
- ✅ Policy-agnostic (no policy interpretation)

**Analogy:**
Runtime Loop = *clock + switchboard*

**Runtime Loop is NOT:**
- ❌ A brain (does not think)
- ❌ A driver (does not decide)
- ❌ A judge (does not evaluate)

---

## 📊 Architectural Position

```
External Input
    ↓
Runtime Loop
    ↓
[ Sensory → Perception → WM → Reasoning → Decision → Action ]
    ↓
Output
```

**Runtime Loop:**
- ❌ Does NOT know formulas
- ❌ Does NOT know energy
- ❌ Does NOT know policy
- ❌ Does NOT know meaning

**Runtime Loop ONLY knows:**
- ✅ Module order
- ✅ Phase sequence
- ✅ Error handling
- ✅ Lifecycle management

---

## 🔄 Execution Phases (CANONICAL)

Runtime Loop is divided into **exactly 9 phases** (fixed order):

| Phase | Name | Purpose |
|-------|------|---------|
| **PHASE 0** | Idle / Wait | Wait for input / event |
| **PHASE 1** | Input Intake | Receive external input |
| **PHASE 2** | Sensory Adaptation | Normalize input |
| **PHASE 3** | Perception Boundary | Feature extraction → Energy |
| **PHASE 4** | Trajectory Admission | GateCore admission check |
| **PHASE 5** | Working Memory Control | WM Controller orchestration |
| **PHASE 6** | Reasoning | Structural reasoning |
| **PHASE 7** | Decision | Final decision |
| **PHASE 8** | Action / Output | Execute action |
| **PHASE 9** | Post-Processing | Logging, audit, metrics |

**Rules:**
- ❌ **MUST NOT** skip phases
- ❌ **MUST NOT** reverse order
- ❌ **MUST NOT** reorder phases
- ✅ **MUST** execute in canonical order

---

## 📋 Phase Responsibilities

### PHASE 0 — Idle / Wait

**Purpose:** Wait for input / event

**Operations:**
- ✅ Wait for input / event
- ✅ Check system state (running / paused / sleep)
- ✅ Monitor system health

**Forbidden:**
- ❌ No computation
- ❌ No decision-making
- ❌ No state modification

---

### PHASE 1 — Input Intake

**Purpose:** Receive input from external world

**Operations:**
- ✅ Receive input from external world
- ✅ Assign `request_id`
- ✅ Timestamp input
- ✅ Validate input format

**Output:**
```python
@dataclass
class RawInputEnvelope:
    raw_input: Any
    request_id: str
    timestamp: float
    source_id: str
    metadata: Dict[str, Any]
```

**Forbidden:**
- ❌ No interpretation
- ❌ No semantic processing
- ❌ No energy computation

---

### PHASE 2 — Sensory Adaptation

**Purpose:** Normalize input

**Operations:**
- ✅ Call sensory adapters
- ✅ Normalize input (scaling, unit alignment)
- ✅ Produce `OriginPack`

**Output:**
```python
@dataclass
class OriginPack:
    raw_signal: Any
    modality: str  # "text" | "image" | "audio"
    timestamp: float
    source_id: str
```

**Forbidden:**
- ❌ No interpretation
- ❌ No energy computation
- ❌ No semantic processing

---

### PHASE 3 — Perception Boundary

**Purpose:** Feature extraction → Energy projection

**Operations:**
- ✅ Feature extraction
- ✅ Energy projection (EPS)
- ✅ Boundary enforcement

**Output:**
```python
@dataclass
class EnergeticState:
    I: float
    P: float
    S: float
    H: float
    A: float
    S_a: float
    E_mu: float
    theta: float
```

**⚠️ Last point before energy world**

**Forbidden:**
- ❌ No semantic interpretation
- ❌ No decision-making
- ❌ No memory access

---

### PHASE 4 — Trajectory Admission

**Purpose:** GateCore admission check

**Operations:**
- ✅ Call GateCore
- ✅ Admission check
- ✅ Create trajectory if allowed

**Output:**
```python
Trajectory | BLOCKED
```

**Runtime Loop Rules:**
- ❌ Does NOT decide
- ✅ Just branches by result
- ✅ If BLOCKED → log and continue to next input

**Forbidden:**
- ❌ No override of GateCore verdict
- ❌ No reinterpretation
- ❌ No bypass

---

### PHASE 5 — Working Memory Control

**Purpose:** WM Controller orchestration

**Operations:**
- ✅ Call WM Controller
- ✅ Receive navigation hint
- ✅ Receive modulated EPS

**Runtime Loop Rules:**
- ❌ Does NOT interpret hint
- ❌ Does NOT override
- ✅ Passes hint to next phase

**Forbidden:**
- ❌ No interpretation of navigation hint
- ❌ No modification of WM output
- ❌ No bypass of WM Controller

---

### PHASE 6 — Reasoning

**Purpose:** Structural reasoning

**Operations:**
- ✅ Call Reasoning Module
- ✅ Receive structured output (graph / plan / tree)

**Runtime Loop Rules:**
- ❌ Does NOT interpret structure
- ❌ Does NOT evaluate structure
- ✅ Passes structure to next phase

**Forbidden:**
- ❌ No decision here
- ❌ No evaluation
- ❌ No scoring

---

### PHASE 7 — Decision

**Purpose:** Final decision

**Operations:**
- ✅ Call Decision Module
- ✅ Receive final action intent

**Runtime Loop Rules:**
- ❌ No voting
- ❌ No filtering
- ✅ Passes decision to next phase

**Forbidden:**
- ❌ No override of decision
- ❌ No reinterpretation
- ❌ No bypass

---

### PHASE 8 — Action / Output

**Purpose:** Execute action

**Operations:**
- ✅ Call Action handlers
- ✅ Produce observable output
- ✅ Attach trace_id

**Output:**
```python
@dataclass
class ActionOutput:
    action_type: str
    output_data: Any
    trace_id: str
    timestamp: float
```

**Forbidden:**
- ❌ No modification of action
- ❌ No override
- ❌ No bypass

---

### PHASE 9 — Post-Processing (Optional)

**Purpose:** Logging, audit, metrics

**Operations:**
- ✅ Logging
- ✅ Audit trail
- ✅ Async memory consolidation trigger
- ✅ Metrics collection

**Rules:**
- ✅ **MUST NOT** affect current loop
- ✅ **MUST NOT** block execution
- ✅ **MUST** be asynchronous (if possible)

**Forbidden:**
- ❌ No state modification
- ❌ No decision influence
- ❌ No blocking operations

---

## 💻 Runtime Loop Pseudocode (CANONICAL)

```python
def runtime_loop():
    while system_running:
        # PHASE 0: Idle / Wait
        input = wait_for_input()
        
        # PHASE 1: Input Intake
        raw_input = intake_input(input)
        
        # PHASE 2: Sensory Adaptation
        origin = sensory.adapt(raw_input)
        
        # PHASE 3: Perception Boundary
        features = perception.encode(origin)
        eps = perception.project_energy(features)
        
        # PHASE 4: Trajectory Admission
        trajectory = gatecore.admit(eps)
        
        if trajectory is BLOCKED:
            log_block(trajectory)
            continue  # Next input
        
        # PHASE 5: Working Memory Control
        wm_output = wm_controller.process(trajectory)
        
        # PHASE 6: Reasoning
        reasoning_output = reasoning.process(
            trajectory=wm_output.trajectory
        )
        
        # PHASE 7: Decision
        decision = decision_module.decide(
            reasoning_output
        )
        
        # PHASE 8: Action / Output
        output = action.execute(
            decision,
            trace_id=trajectory.trace_id
        )
        
        # PHASE 9: Post-Processing
        runtime.post_process(trajectory, output)
```

**Rules:**
- ✅ Execute phases in order
- ✅ No skipping
- ✅ No backtracking
- ✅ No reordering

---

## 🔄 Determinism Contract

Runtime Loop **MUST** guarantee:

- ✅ Same input sequence → same execution path
- ✅ Same timing → same behavior
- ✅ Same configuration → same results

**Guarantee:**
```
Same input sequence + Same timing + Same config
    ↓
Same execution path
```

**Forbidden:**
- ❌ No randomness
- ❌ No learning
- ❌ No adaptation
- ❌ No time-based behavior (except timing control)

---

## ⚠️ Error Handling Policy

### Error Handling Rules

**On Error:**
- ✅ **ABORT** current loop cycle
- ✅ **LOG** error
- ✅ **CONTINUE** to next input

**Forbidden:**
- ❌ Retry with modified data
- ❌ Fallback decision
- ❌ Heuristic bypass
- ❌ Auto-correction

**Example:**
```python
# ✅ CORRECT
try:
    trajectory = gatecore.admit(eps)
except Exception as e:
    log_error(e)
    continue  # Next input

# ❌ FORBIDDEN
try:
    trajectory = gatecore.admit(eps)
except Exception as e:
    trajectory = fallback_trajectory  # Fallback
    continue
```

**Error Types:**
- ✅ Module errors (propagate and abort)
- ✅ Validation errors (log and abort)
- ✅ System errors (log and abort)

---

## 🔀 Concurrency Model

Runtime Loop is:
- ✅ **Single authority** (one loop per system)
- ✅ **Single timeline** (sequential execution)

**Concurrency Allowed Only In:**
- ✅ I/O waiting (non-blocking)
- ✅ Async logging (background)
- ✅ Background consolidation (separate process)

**Forbidden:**
- ❌ No concurrent decision paths
- ❌ No parallel execution of phases
- ❌ No race conditions
- ❌ No shared mutable state

**Thread Safety:**
- ✅ Each loop cycle is isolated
- ✅ No shared state between cycles
- ✅ All modules are stateless (or thread-safe)

---

## 😴 Interaction with Sleep / Consolidation

**Sleep Engine:**
- ✅ **NEVER** called inline
- ✅ **NEVER** blocks runtime loop
- ✅ Triggered asynchronously

**Runtime Loop only emits:**
```python
sleep_hint = {
    "trajectory_id": "...",
    "consolidation_needed": True,
    "timestamp": "..."
}
```

**Rules:**
- ✅ Sleep/consolidation is **separate process**
- ✅ Runtime loop **does not wait** for consolidation
- ✅ Runtime loop **does not block** on sleep

---

## 🛡️ Security Boundaries

Runtime Loop **MUST NOT** import:
- ❌ `kernel/` (no direct kernel access)
- ❌ `gate/` (no direct gate access)
- ❌ `memory/` (no direct memory access)
- ❌ `reasoning/` internals (interface only)

**Runtime Loop sees modules only via interfaces:**

```python
# ✅ ALLOWED: Interface access
from wm_controller import WMControllerInterface
from reasoning import ReasoningInterface

# ❌ FORBIDDEN: Direct import
from kernel import core_formulas  # Direct access
from gate import decision_logic  # Direct access
```

**Isolation:**
- ✅ Runtime Loop is **orchestration layer**
- ✅ Modules are **black boxes** to Runtime Loop
- ✅ No semantic leakage

---

## 🔍 Audit Checklist

Auditor **MUST** confirm:

### Code Inspection
- [ ] No formulas in runtime
- [ ] No thresholds
- [ ] No policy logic
- [ ] No state mutation across cycles
- [ ] No hidden branching
- [ ] No imports from `kernel/`, `gate/`, `memory/`
- [ ] No semantic interpretation

### Execution Inspection
- [ ] Phases execute in order
- [ ] No phase skipping
- [ ] No phase backtracking
- [ ] Errors abort cycle (no fallback)
- [ ] Deterministic execution

### Interface Inspection
- [ ] All module access via interfaces
- [ ] No direct internal access
- [ ] No bypass of modules

---

## 📋 Examples

### Example (VALID)

**Execution Path:**
```
Input → Sensory → Perception → GateCore → BLOCKED → log → next input
```

**Execution Path:**
```
Input → Sensory → Perception → GateCore → Trajectory → WM → Reasoning → Decision → Action
```

**Analysis:**
- ✅ Phases in order
- ✅ No skipping
- ✅ No backtracking
- ✅ Deterministic

---

### Example (INVALID)

**❌ FORBIDDEN:**
```python
# ❌ FORBIDDEN: Skip decision
if confidence < 0.6:
    skip_decision()  # Bypass

# ❌ FORBIDDEN: Retry with modification
if perception_failed:
    retry_perception(different_parameters)  # Modification

# ❌ FORBIDDEN: Optimize path
if fast_path_available:
    skip_reasoning()  # Optimization
```

---

## 📋 Summary (LOCKED INTENT)

**Runtime Loop is:**
- ✅ Railway track (fixed path)
- ✅ Clock (timing control)
- ✅ Switchboard (module orchestration)

**Runtime Loop is NOT:**
- ❌ A driver (does not decide)
- ❌ A brain (does not think)
- ❌ A judge (does not evaluate)

**If the track starts thinking, the system fails silently.**

---

## 📚 Related Specifications

- **WM Controller:** `docs/WM_CONTROLLER_SPEC.md`
- **Perception Boundary:** `docs/PERCEPTION_BOUNDARY_SPEC.md`
- **Reasoning Module:** `docs/REASONING_MODULE_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture approval
2. Safety approval
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
**Purpose:** Prevent Runtime Loop from becoming "intelligent"  
**Authority:** Core Team  
**Enforcement:** Code review + phase execution monitoring

