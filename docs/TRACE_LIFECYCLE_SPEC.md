# Trace Lifecycle Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Trace Lifecycle Management  
**Scope:** Trace Creation, Execution, Closure, Replay, Audit  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This specification defines the **complete lifecycle** of Trace from creation → execution → closure → audit.

It ensures that Cogman is:
- ✅ Deterministic
- ✅ Auditable
- ✅ Replayable
- ✅ No ghost states
- ✅ Cannot be bypassed

**Trace is the unit of truth for the entire system.**

**Why This Matters:**
Without proper trace lifecycle:
- Debugging is impossible
- Audit fails
- System cannot defend itself
- Kernel misuse goes undetected

---

## 📋 Trace Definition (Canonical)

### Trace Structure

```python
@dataclass(frozen=True)
class Trace:
    trace_id: str                # Immutable identifier
    state: Literal[
        "CREATED",
        "ACTIVE",
        "BLOCKED",
        "COMPLETED",
        "INVALID",
        "ARCHIVED"
    ]
    created_at: float            # Creation timestamp
    closed_at: Optional[float]   # Closure timestamp (if closed)
    
    origin: Dict[str, Any]      # source_id, modality, adapter
    context: Dict[str, Any]     # gate profile, runtime mode
    
    lifecycle_log: List[Dict]    # Append-only event log
```

**Rules:**
- ✅ `trace_id` is **immutable** (never changes)
- ✅ `lifecycle_log` is **append-only** (never modified)
- ✅ `state` transitions are **locked** (no arbitrary changes)

---

## 🔄 Trace State Machine (LOCKED)

```
┌─────────┐
│ CREATED │
└────┬────┘
     │ admission gate pass
     ▼
┌────────┐
│ ACTIVE │──────────────┐
└───┬────┘              │
    │ blocked           │ completed
    ▼                   ▼
┌────────┐         ┌───────────┐
│BLOCKED │         │ COMPLETED │
└───┬────┘         └────┬───────┘
    │ invalid           │ archive
    ▼                   ▼
┌────────┐         ┌───────────┐
│INVALID │         │ ARCHIVED  │
└────────┘         └───────────┘
```

**State Transition Rules:**
- ❌ **MUST NOT** reverse state (no backward transitions)
- ❌ **MUST NOT** skip state (no direct transitions)
- ✅ **MUST** follow canonical order
- ✅ **MUST** log all transitions

**Allowed Transitions:**
- `CREATED` → `ACTIVE` (gate pass)
- `ACTIVE` → `BLOCKED` (gate fail)
- `ACTIVE` → `COMPLETED` (execution complete)
- `BLOCKED` → `INVALID` (violation detected)
- `COMPLETED` → `ARCHIVED` (archived)

---

## 📊 State Semantics

### 1. CREATED

**Meaning:** Trace created, not yet in Runtime Loop

**Conditions:**
- ✅ Trace created from TrajectoryBuilder
- ✅ Not yet passed Runtime Loop
- ✅ Kernel **NOT** invoked yet

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_CREATED",
  "trace_id": "abc123",
  "source": "perception",
  "modality": "text",
  "timestamp": "2024-12-01T10:30:00Z"
}
```

**Allowed Next States:**
- `ACTIVE` (if gate passes)
- `BLOCKED` (if gate fails immediately)

---

### 2. ACTIVE

**Meaning:** Trace in Runtime Loop, execution in progress

**Conditions:**
- ✅ `trace_id` is valid
- ✅ Gate status == PASS
- ✅ In Runtime Loop
- ✅ WM Controller managing

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_ACTIVE",
  "trace_id": "abc123",
  "gate_status": "PASS",
  "wm_controller": "active",
  "timestamp": "2024-12-01T10:30:01Z"
}
```

**Allowed Next States:**
- `BLOCKED` (if blocked during execution)
- `COMPLETED` (if execution completes)

**Kernel Invocation:**
- ✅ Kernel **MAY** be invoked (if needed)
- ✅ All kernel calls **MUST** be logged

---

### 3. BLOCKED

**Meaning:** Trace stopped by Gate / Safety / Budget

**Conditions:**
- ✅ Stopped by GateCore
- ✅ Stopped by Safety Gate
- ✅ Stopped by Budget Gate
- ✅ Kernel **MUST NOT** be invoked

**Reasons:**
- Entropy overflow
- Safety violation
- Policy reject
- Resource limit

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_BLOCKED",
  "trace_id": "abc123",
  "reason": "entropy_gate",
  "layer": "GateCore",
  "details": {
    "H": 0.85,
    "H_max": 0.62
  },
  "timestamp": "2024-12-01T10:30:02Z"
}
```

**Allowed Next States:**
- `INVALID` (if violation detected)
- `ARCHIVED` (if audit complete)

---

### 4. COMPLETED

**Meaning:** Trace completed full lifecycle

**Conditions:**
- ✅ Ran through complete lifecycle
- ✅ Kernel (if needed) invoked successfully
- ✅ Output emitted

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_COMPLETED",
  "trace_id": "abc123",
  "outputs": ["text", "motor"],
  "kernel_invocations": 3,
  "timestamp": "2024-12-01T10:30:05Z"
}
```

**Allowed Next States:**
- `ARCHIVED` (after audit)

---

### 5. INVALID

**Meaning:** Trace violates specification

**Conditions:**
- ✅ Trace violates spec
- ✅ Bypass detected
- ✅ Kernel violation detected

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_INVALID",
  "trace_id": "abc123",
  "violation": "kernel_called_from_cli",
  "details": {
    "caller": "cli",
    "expected": "runtime"
  },
  "timestamp": "2024-12-01T10:30:03Z"
}
```

**Rules:**
- ❌ **MUST NOT** be archived
- ❌ **MUST NOT** be replayed
- ✅ **MUST** be logged for audit

---

### 6. ARCHIVED

**Meaning:** Trace closed and archived

**Conditions:**
- ✅ Trace closed (COMPLETED or BLOCKED)
- ✅ Audit complete
- ✅ Archived for long-term storage

**Lifecycle Log Entry:**
```json
{
  "event": "TRACE_ARCHIVED",
  "trace_id": "abc123",
  "archived_at": "2024-12-01T10:35:00Z",
  "retention_days": 90
}
```

**Rules:**
- ✅ Read-only (cannot be modified)
- ✅ Replayable (can be replayed)
- ✅ Auditable (can be audited)

---

## 📝 Lifecycle Log (Append-Only)

Every Trace **MUST** have an append-only lifecycle log.

### Log Entry Structure

```python
@dataclass
class LifecycleLogEntry:
    event: str                   # Event type
    layer: str                   # Layer name
    trace_id: str                # Trace identifier
    timestamp: float             # Event timestamp
    data: Dict[str, Any]         # Event-specific data
```

### Example Log Entries

**WM Decision:**
```json
{
  "event": "WM_DECISION",
  "layer": "WM_CONTROLLER",
  "trace_id": "abc123",
  "decision": "RECALL_SN",
  "eps8_snapshot": {
    "I": 0.7,
    "P": 0.6,
    "S": 0.8,
    "H": 0.3,
    "A": 0.5,
    "S_a": 0.4,
    "theta": 1.2
  },
  "timestamp": "2024-12-01T10:30:02Z"
}
```

**Kernel Invocation:**
```json
{
  "event": "KERNEL_INVOKED",
  "layer": "RUNTIME",
  "trace_id": "abc123",
  "mode": "default",
  "eps8": {...},
  "timestamp": "2024-12-01T10:30:03Z"
}
```

**Rules:**
- ❌ **MUST NOT** overwrite
- ❌ **MUST NOT** delete
- ✅ **MUST** be append-only
- ✅ **MUST** be immutable

---

## 🔨 Trace Creation Rules

Trace can **ONLY** be created by:

**✅ TrajectoryBuilder**

**❌ Forbidden Creators:**
- ❌ CLI (cannot create trace)
- ❌ Kernel (cannot create trace)
- ❌ Memory (cannot create trace)
- ❌ Reasoning (cannot create trace)
- ❌ Tools / Scripts (cannot create trace)

**Creation Process:**
```python
# ✅ ALLOWED
trajectory = TrajectoryBuilder.create(energetic_state)
trace = Trace(
    trace_id=generate_trace_id(),
    state="CREATED",
    created_at=time.time(),
    origin={...},
    context={...},
    lifecycle_log=[{
        "event": "TRACE_CREATED",
        "timestamp": time.time()
    }]
)
```

---

## 🔒 Trace Closure Rules

Trace can be closed when:

- ✅ `COMPLETED` (execution complete)
- ✅ `BLOCKED` (stopped by gate)
- ✅ `INVALID` (violation detected)

**Closure Function:**
```python
def close_trace(trace: Trace, reason: str) -> None:
    """
    Close trace with reason.
    
    Args:
        trace: Trace to close
        reason: Closure reason (COMPLETED, BLOCKED, INVALID)
    """
    if trace.state not in ["ACTIVE", "CREATED"]:
        raise TraceViolation("Cannot close trace in state: " + trace.state)
    
    trace.state = reason
    trace.closed_at = time.time()
    
    # Log closure
    trace.lifecycle_log.append({
        "event": f"TRACE_{reason}",
        "timestamp": time.time()
    })
```

**Rules:**
- ✅ Closure is **irreversible**
- ✅ Closure **MUST** be logged
- ❌ **MUST NOT** close active trace without reason

---

## 🔄 Replay Policy (Critical)

Replay **MUST**:
- ✅ Use `trace_id`
- ✅ Use stored `lifecycle_log`
- ❌ **MUST NOT** call kernel again
- ❌ **MUST NOT** write memory
- ❌ **MUST NOT** emit action

**Replay = Deterministic Reconstruction**

### Replay Modes

| Mode | Kernel | Memory | Output | Purpose |
|------|--------|--------|--------|---------|
| **inspect** | ❌ | ❌ | ❌ | Read-only inspection |
| **explain** | ❌ | ❌ | ✅ (text) | Generate explanation |
| **verify** | ❌ | ❌ | ✅ (verdict) | Verify correctness |
| **simulate** | ❌ | ❌ | ✅ (simulated) | Simulate output |

**Replay Implementation:**
```python
def replay_trace(trace_id: str, mode: str = "inspect") -> ReplayResult:
    """
    Replay trace deterministically.
    
    Args:
        trace_id: Trace identifier
        mode: Replay mode (inspect, explain, verify, simulate)
    
    Returns:
        ReplayResult with reconstructed state
    """
    trace = load_trace(trace_id)
    
    if trace.state == "INVALID":
        raise TraceViolation("Cannot replay INVALID trace")
    
    # Reconstruct from lifecycle_log
    reconstructed_state = reconstruct_from_log(trace.lifecycle_log)
    
    # Generate output based on mode
    if mode == "explain":
        return generate_explanation(reconstructed_state)
    elif mode == "verify":
        return verify_correctness(reconstructed_state)
    elif mode == "simulate":
        return simulate_output(reconstructed_state)
    else:
        return reconstructed_state
```

**Rules:**
- ✅ Replay is **deterministic** (same log → same result)
- ✅ Replay has **no side effects**
- ❌ **MUST NOT** modify original trace
- ❌ **MUST NOT** create new trace

---

## 🔍 Audit Guarantees

System **MUST** be able to answer:

1. **What started this trace?**
   - Source, modality, adapter
   - Initial state

2. **Which gates did it pass?**
   - GateCore verdict
   - Safety gate status
   - Budget gate status

3. **Who called kernel?**
   - Caller (must be "runtime")
   - Invocation context
   - Kernel results

4. **What output came from which state?**
   - Output source state
   - Output generation process

5. **Why was it blocked / allowed?**
   - Block reason
   - Gate verdict
   - Metrics at decision point

**If system cannot answer these → audit fails**

**Audit Query Example:**
```python
def audit_trace(trace_id: str) -> AuditReport:
    """
    Generate audit report for trace.
    
    Returns:
        AuditReport with complete trace analysis
    """
    trace = load_trace(trace_id)
    
    return AuditReport(
        trace_id=trace_id,
        origin=trace.origin,
        gate_history=extract_gate_events(trace.lifecycle_log),
        kernel_invocations=extract_kernel_events(trace.lifecycle_log),
        output_source=extract_output_events(trace.lifecycle_log),
        decision_reason=extract_decision_events(trace.lifecycle_log)
    )
```

---

## 💾 Storage Layout (RECOMMENDED)

```
storage/trace/
├── active/
│   └── trace_<id>.json
├── completed/
│   └── trace_<id>.json
├── blocked/
│   └── trace_<id>.json
├── invalid/
│   └── trace_<id>.json
└── archived/
    └── trace_<id>.json
```

**Storage Rules:**
- ✅ Traces stored by state
- ✅ Immutable storage (no modification)
- ✅ Append-only logs
- ✅ Retention policy (configurable)

---

## 🛡️ Hard Invariants (MUST HOLD)

These invariants **MUST** hold at all times:

1. **`trace_id` is immutable**
   - Never changes after creation
   - Used for all operations

2. **Kernel invocation implies ACTIVE state**
   - Kernel **MUST NOT** be called for non-ACTIVE traces
   - All kernel calls **MUST** be logged

3. **CLI never changes trace state**
   - CLI **MUST NOT** modify trace state
   - CLI **MUST NOT** create trace

4. **Replay never mutates system**
   - Replay is read-only
   - Replay has no side effects

5. **INVALID trace cannot be archived**
   - INVALID traces **MUST NOT** be archived
   - INVALID traces **MUST** be logged for audit

**Enforcement:**
- Runtime checks
- Code review
- Automated tests

---

## 📋 Summary (LOCKED INTENT)

**Trace is:**
- ✅ Unit of truth (complete system state)
- ✅ Audit trail (complete history)
- ✅ Replay source (deterministic reconstruction)
- ✅ Evidence (system defense)

**Trace is NOT:**
- ❌ Mutable (cannot be modified)
- ❌ Optional (must exist for all operations)
- ❌ Semantic (no meaning interpretation)

**If this Trace exists, your system can prove itself.  
If this Trace does not exist, your system has no right to be called a system.**

---

## 📚 Related Specifications

- **Runtime Loop:** `docs/RUNTIME_LOOP_SPEC.md`
- **Kernel Invocation:** `docs/KERNEL_INVOCATION_SPEC.md`
- **CLI Execution:** `docs/CLI_EXECUTION_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Audit & Traceability:** `docs/AUDIT_TRACE_SPEC.md` (if exists)

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
**Purpose:** Ensure system is auditable and replayable  
**Authority:** Core Team  
**Enforcement:** Runtime checks + audit tools

