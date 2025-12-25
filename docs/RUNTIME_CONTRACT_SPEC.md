# Runtime Contract Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Runtime Loop ↔ Module Interface Contracts  
**Scope:** All Runtime Loop Phase Contracts  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This document defines **strict interface contracts** between Runtime Loop and all modules.

**Runtime Contract = Data Contract + Execution Contract + Error Contract**

**Why This Matters:**
Without clear contracts:
- Modules cannot be swapped
- Integration becomes fragile
- Testing becomes impossible
- Audits fail
- System becomes unmaintainable

---

## 🔒 Core Principle (HARD RULE)

> **Runtime Loop is a contract enforcer.**

Runtime Loop:
- ✅ Validates all inputs/outputs
- ✅ Enforces phase order
- ✅ Handles contract violations
- ✅ Logs all contract breaches

Runtime Loop does NOT:
- ❌ Interpret contract data
- ❌ Modify contract data
- ❌ Bypass contracts
- ❌ Auto-correct violations

**Contract Violation = System Error**

---

## 📊 Contract Structure

Each phase has **exactly 3 contracts**:

1. **Input Contract** (what Runtime Loop provides)
2. **Output Contract** (what module must return)
3. **Error Contract** (how errors are handled)

---

## 🔄 Phase Contracts

### PHASE 0: Idle / Wait

**Purpose:** Wait for input / event

**Input Contract:**
```python
# No input (idle state)
None
```

**Output Contract:**
```python
# No output (waiting)
None
```

**Error Contract:**
- No errors possible (idle state)

**Rules:**
- ✅ Runtime Loop waits here
- ✅ No module invocation
- ✅ No data processing

---

### PHASE 1: Input Intake

**Purpose:** Receive external input

**Input Contract:**
```python
# Runtime Loop receives from external source
external_input: Any  # Raw input from external system
request_id: str      # Unique request identifier
timestamp: float     # Input timestamp
source_id: str       # Source identifier
metadata: Dict[str, Any]  # Additional metadata
```

**Output Contract:**
```python
@dataclass
class RawInputEnvelope:
    raw_input: Any              # Preserved raw input
    request_id: str             # Request identifier
    timestamp: float             # Input timestamp
    source_id: str               # Source identifier
    metadata: Dict[str, Any]    # Additional metadata
```

**Error Contract:**
- **On Error:** ABORT cycle, LOG error, CONTINUE to next input
- **Error Types:** Invalid input, missing fields, malformed data

**Rules:**
- ✅ Preserve raw input (immutable)
- ✅ Generate unique request_id
- ✅ Record timestamp
- ❌ **MUST NOT** modify raw input
- ❌ **MUST NOT** interpret input

---

### PHASE 2: Sensory Adaptation

**Purpose:** Normalize input

**Input Contract:**
```python
@dataclass
class RawInputEnvelope:
    raw_input: Any
    request_id: str
    timestamp: float
    source_id: str
    metadata: Dict[str, Any]
```

**Output Contract:**
```python
@dataclass
class OriginPack:
    raw_signal: Any              # Normalized signal (immutable)
    modality: str                # "text" | "image" | "audio" (numeric code)
    timestamp: float              # Signal timestamp
    source_id: str                # Source identifier
    metadata: Dict[str, Any]     # Additional metadata (non-semantic)
```

**Error Contract:**
- **On Error:** ABORT cycle, LOG error, CONTINUE to next input
- **Error Types:** Unsupported modality, normalization failure, invalid signal

**Rules:**
- ✅ Normalize signal only (no interpretation)
- ✅ Preserve raw_signal (immutable)
- ✅ Set modality (numeric code only)
- ❌ **MUST NOT** interpret meaning
- ❌ **MUST NOT** extract features
- ❌ **MUST NOT** modify original signal

**Module:** `sensory/` adapters

---

### PHASE 3: Perception Boundary

**Purpose:** Feature extraction → Energy projection

**Input Contract:**
```python
@dataclass
class OriginPack:
    raw_signal: Any
    modality: str
    timestamp: float
    source_id: str
    metadata: Dict[str, Any]
```

**Output Contract:**
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

**Error Contract:**
- **On Error:** ABORT cycle, LOG error, CONTINUE to next input
- **Error Types:** Feature extraction failure, energy computation error, invalid state

**Rules:**
- ✅ Extract features only (no interpretation)
- ✅ Project to energy parameters
- ✅ Validate all energy values (range, NaN, infinity)
- ❌ **MUST NOT** interpret meaning
- ❌ **MUST NOT** create trajectory
- ❌ **MUST NOT** call Kernel directly
- ❌ **MUST NOT** make decisions

**Module:** `perception/` modules

**Reference:** `docs/PERCEPTION_BOUNDARY_SPEC.md`

---

### PHASE 4: Trajectory Admission

**Purpose:** GateCore admission check

**Input Contract:**
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
    meta: Dict[str, Any]

# Plus trajectory context
trajectory: Optional[Trajectory]  # Existing trajectory (if any)
trace_id: str                     # Trace identifier
```

**Output Contract:**
```python
@dataclass
class AdmissionResult:
    verdict: Literal["ALLOW", "REVIEW", "BLOCK"]
    reason: str                   # Explainable reason
    metrics: Dict[str, float]     # Decision metrics
    trajectory: Optional[Trajectory]  # Updated trajectory (if ALLOW)
    trace_id: str                 # Trace identifier
```

**Error Contract:**
- **On Error:** BLOCK verdict, LOG error, NO trajectory creation
- **Error Types:** Invalid state, gate computation error, policy violation

**Rules:**
- ✅ Evaluate admission gate only
- ✅ Return verdict (ALLOW/REVIEW/BLOCK)
- ✅ Provide explainable reason
- ❌ **MUST NOT** override verdict
- ❌ **MUST NOT** bypass gate
- ❌ **MUST NOT** create trajectory if BLOCK

**Module:** `gate/` GateCore

**Reference:** `docs/GATECORE_SPEC.md`

---

### PHASE 5: Working Memory Control

**Purpose:** WM Controller orchestration

**Input Contract:**
```python
@dataclass
class Trajectory:
    states: List[EPS8State]       # State history (immutable)
    trace_id: str                 # Trace identifier
    source_modality: str          # Input modality
    timestamp: float              # Creation timestamp
    debug_lineage: Dict[str, Any] # Debug information
```

**Output Contract:**
```python
@dataclass
class WMControllerOutput:
    navigation_decision: str      # "CREATE_NEW_SN" | "EXTEND_PATH" | "RECALL_SN" | ...
    modulated_eps8: EPS8State     # Context-modulated state
    resonance_scores: Dict[str, float]  # Memory resonance scores
    trajectory: Trajectory        # Updated trajectory
    trace_id: str                # Trace identifier
```

**Error Contract:**
- **On Error:** ABORT cycle, LOG error, CONTINUE to next input
- **Error Types:** Invalid trajectory, memory query failure, routing error

**Rules:**
- ✅ Gate control (pass/block)
- ✅ Routing (where to go next)
- ✅ Context modulation (minor energy adjustment)
- ✅ Memory resonance invocation
- ✅ Navigation decision
- ❌ **MUST NOT** create new energy formulas
- ❌ **MUST NOT** modify kernel output
- ❌ **MUST NOT** write memory directly
- ❌ **MUST NOT** override safety rules

**Module:** `runtime/wm_controller.py`

**Reference:** `docs/WM_CONTROLLER_SPEC.md`

---

### PHASE 6: Reasoning

**Purpose:** Structural reasoning

**Input Contract:**
```python
@dataclass
class ReasoningInput:
    trajectory: Trajectory              # From WM Controller only
    wm_decision_hint: Optional[str]     # Informational only
    context: Dict[str, Any]              # Informational only
    trace_id: str                       # Trace identifier
```

**Output Contract:**
```python
@dataclass
class ReasoningOutput:
    structure_type: Literal[
        "graph",
        "plan",
        "tree",
        "simulation"
    ]
    structure: Any                     # Graph/Plan/Tree structure
    assumptions: List[str]             # Structural assumptions
    constraints: List[str]             # Structural constraints
    meta: Dict[str, Any]               # Non-semantic metadata
    trace_id: str                     # Trace identifier
```

**Error Contract:**
- **On Error:** RAISE exception, DO NOT continue
- **Error Types:** Malformed trajectory, missing context, unsupported structure type

**Rules:**
- ✅ Create structure only (graph, plan, tree, simulation)
- ✅ Link causal relations
- ✅ Simulate alternatives
- ❌ **MUST NOT** modify trajectory
- ❌ **MUST NOT** change energy
- ❌ **MUST NOT** make decisions
- ❌ **MUST NOT** call Kernel
- ❌ **MUST NOT** use thresholds
- ❌ **MUST NOT** optimize outcome

**Module:** `reasoning/` modules

**Reference:** `docs/REASONING_MODULE_SPEC.md`

---

### PHASE 7: Decision

**Purpose:** Final decision

**Input Contract:**
```python
@dataclass
class DecisionInput:
    trajectory: Trajectory              # Current trajectory
    reasoning_output: ReasoningOutput  # Reasoning structure
    wm_output: WMControllerOutput      # WM Controller output
    trace_id: str                       # Trace identifier
```

**Output Contract:**
```python
@dataclass
class DecisionOutput:
    decision: Literal["ALLOW", "REVIEW", "BLOCK"]
    reason: str                         # Explainable reason
    metrics: Dict[str, float]           # Decision metrics
    action_hint: Optional[str]          # Action hint (if ALLOW)
    trace_id: str                       # Trace identifier
```

**Error Contract:**
- **On Error:** BLOCK verdict, LOG error, NO action
- **Error Types:** Invalid input, decision computation error, policy violation

**Rules:**
- ✅ Evaluate final decision gate
- ✅ Return verdict (ALLOW/REVIEW/BLOCK)
- ✅ Provide explainable reason
- ❌ **MUST NOT** override GateCore verdict
- ❌ **MUST NOT** bypass safety rules
- ❌ **MUST NOT** create action if BLOCK

**Module:** `gate/` DecisionGate

**Reference:** `docs/GATECORE_SPEC.md`

---

### PHASE 8: Action / Output

**Purpose:** Execute action

**Input Contract:**
```python
@dataclass
class ActionInput:
    decision: DecisionOutput            # Decision result
    trajectory: Trajectory              # Current trajectory
    reasoning_output: ReasoningOutput  # Reasoning structure
    trace_id: str                       # Trace identifier
```

**Output Contract:**
```python
@dataclass
class ActionOutput:
    action_type: str                    # "text" | "motor" | "agent"
    output_data: Any                    # Action output data
    success: bool                       # Action success flag
    trace_id: str                       # Trace identifier
    timestamp: float                     # Action timestamp
```

**Error Contract:**
- **On Error:** Return error in ActionOutput, LOG error
- **Error Types:** Action execution failure, invalid output, external system error

**Rules:**
- ✅ Execute action only if ALLOW
- ✅ Return action output
- ✅ Set success flag
- ❌ **MUST NOT** execute if BLOCK
- ❌ **MUST NOT** retry on error
- ❌ **MUST NOT** fallback action

**Module:** `action/` modules

**Reference:** `docs/LLM_INTERFACE_SPEC.md` (if using LLM)

---

### PHASE 9: Post-Processing

**Purpose:** Logging, audit, metrics

**Input Contract:**
```python
@dataclass
class PostProcessInput:
    trajectory: Trajectory              # Complete trajectory
    action_output: ActionOutput        # Action output
    trace_id: str                       # Trace identifier
    timestamp: float                     # Processing timestamp
    phase_results: Dict[str, Any]      # Results from all phases (optional)
```

**Output Contract:**
```python
@dataclass
class PostProcessOutput:
    logged: bool                        # Logging success
    audited: bool                       # Audit trail success
    metrics_collected: bool             # Metrics collection success
    trace_id: str                       # Trace identifier
```

**Error Contract:**
- **On Error:** LOG error, CONTINUE (non-blocking)
- **Error Types:** Logging failure, audit failure, metrics collection failure

**Rules:**
- ✅ Log execution (non-blocking)
- ✅ Store audit trail (non-blocking)
- ✅ Collect metrics (non-blocking)
- ✅ Trigger memory consolidation (async)
- ❌ **MUST NOT** block execution
- ❌ **MUST NOT** modify trajectory
- ❌ **MUST NOT** change action output

**Module:** `runtime/post_processor.py`

---

## 🔒 Contract Enforcement

### Input Validation

Runtime Loop **MUST** validate all inputs:

1. **Type Check:** Verify data types match contract
2. **Range Check:** Verify numeric ranges
3. **Required Fields:** Verify all required fields present
4. **Immutable Check:** Verify immutability constraints

**On Validation Failure:**
- ABORT cycle
- LOG error
- CONTINUE to next input

### Output Validation

Runtime Loop **MUST** validate all outputs:

1. **Type Check:** Verify data types match contract
2. **Range Check:** Verify numeric ranges
3. **Required Fields:** Verify all required fields present
4. **Contract Compliance:** Verify contract rules

**On Validation Failure:**
- ABORT cycle
- LOG error
- CONTINUE to next input

### Error Handling

Runtime Loop **MUST** handle all errors:

1. **Catch All Exceptions:** No unhandled exceptions
2. **Log All Errors:** Complete error logging
3. **Abort Cycle:** Current cycle aborted
4. **Continue Loop:** Continue to next input

**Error Handling Contract:**
- ✅ All errors are logged
- ✅ All errors abort current cycle
- ✅ All errors allow loop to continue
- ❌ **MUST NOT** retry on error
- ❌ **MUST NOT** auto-correct errors
- ❌ **MUST NOT** bypass error handling

---

## 📋 Contract Checklist

### For Each Phase

- [ ] Input contract defined
- [ ] Output contract defined
- [ ] Error contract defined
- [ ] Data structures defined
- [ ] Validation rules defined
- [ ] Error handling rules defined
- [ ] Immutability rules defined
- [ ] Isolation rules defined

### For Runtime Loop

- [ ] All inputs validated
- [ ] All outputs validated
- [ ] All errors handled
- [ ] All contracts enforced
- [ ] All violations logged

---

## 🛡️ Contract Violations

### Violation Types

1. **Type Violation:** Wrong data type
2. **Range Violation:** Value out of range
3. **Required Field Violation:** Missing required field
4. **Immutability Violation:** Modified immutable data
5. **Isolation Violation:** Cross-layer access
6. **Error Handling Violation:** Unhandled error

### Violation Response

**On Contract Violation:**
1. ABORT current cycle
2. LOG violation (with details)
3. CONTINUE to next input
4. NO auto-correction
5. NO fallback

---

## 📊 Contract Examples

### Example 1: Valid Flow

```
PHASE 1: Input Intake
  Input: external_input
  Output: RawInputEnvelope ✓

PHASE 2: Sensory Adaptation
  Input: RawInputEnvelope ✓
  Output: OriginPack ✓

PHASE 3: Perception Boundary
  Input: OriginPack ✓
  Output: EnergeticState ✓

PHASE 4: Trajectory Admission
  Input: EnergeticState ✓
  Output: AdmissionResult (ALLOW) ✓

PHASE 5: Working Memory Control
  Input: Trajectory ✓
  Output: WMControllerOutput ✓

PHASE 6: Reasoning
  Input: ReasoningInput ✓
  Output: ReasoningOutput ✓

PHASE 7: Decision
  Input: DecisionInput ✓
  Output: DecisionOutput (ALLOW) ✓

PHASE 8: Action / Output
  Input: ActionInput ✓
  Output: ActionOutput ✓

PHASE 9: Post-Processing
  Input: PostProcessInput ✓
  Output: PostProcessOutput ✓
```

### Example 2: Contract Violation

```
PHASE 3: Perception Boundary
  Input: OriginPack ✓
  Output: EnergeticState (H = 1.5) ✗  # Range violation (H must be [0, 1])
  
  → ABORT cycle
  → LOG error: "Range violation: H = 1.5 (must be [0, 1])"
  → CONTINUE to next input
```

### Example 3: Error Handling

```
PHASE 4: Trajectory Admission
  Input: EnergeticState ✓
  Error: GateCore computation error
  
  → ABORT cycle
  → LOG error: "GateCore computation error: ..."
  → CONTINUE to next input
```

---

## 🔗 Related Specifications

- **RUNTIME_LOOP_SPEC.md:** Runtime Loop execution mechanism
- **WM_CONTROLLER_SPEC.md:** WM Controller contracts
- **GATECORE_SPEC.md:** GateCore contracts
- **PERCEPTION_BOUNDARY_SPEC.md:** Perception contracts
- **REASONING_MODULE_SPEC.md:** Reasoning contracts
- **KERNEL_BOUNDARY_SPEC.md:** Kernel contracts
- **BASE-2_DATA_CONTRACTS.md:** Base data contracts

---

## 📝 Summary

**Runtime Contract = Interface Contract + Execution Contract + Error Contract**

**Key Rules:**
1. ✅ All phases have strict input/output contracts
2. ✅ All contracts are validated
3. ✅ All violations are logged
4. ✅ All errors abort cycle
5. ✅ All cycles continue to next input

**Runtime Loop enforces contracts, does not interpret them.**

---

## Status

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Contract definitions finalized  
**Last Updated:** 2024-12

