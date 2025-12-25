# Reasoning Module Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Structural Reasoning Only  
**Scope:** Post-WM / Pre-Action Logical Structuring  
**Last Updated:** 2024-12

---

## 🎯 Purpose

Reasoning Module has **exactly one responsibility**:

> **Structure relationships of data**  
> NOT thinking  
> NOT deciding  
> NOT evaluating

**Clarification:**
- **Reasoning** = *structuring* (organizing relationships)
- **Decision** = *choosing* (selecting action)
- **Thinking** = *evaluating* (assessing value)

These three **MUST NOT** be mixed.

**Why This Matters:**
This specification prevents Reasoning from becoming a "fake brain" that makes decisions or evaluates outcomes. Reasoning is **structural only**, not cognitive.

---

## 📊 Architectural Position

```
Trajectory (from WM Controller)
    ↓
Reasoning Module
    ↓
Structured Plan / Graph / Hypothesis
    ↓
Decision Module (separate)
```

**Reasoning is NEVER:**
- ❌ Before WM Controller
- ❌ After Decision
- ❌ In Kernel
- ❌ In GateCore

**Reasoning is ALWAYS:**
- ✅ After WM Controller
- ✅ Before Decision
- ✅ Separate from Kernel
- ✅ Separate from GateCore

---

## 🔒 Core Responsibilities (ONLY THESE)

Reasoning Module does **exactly 4 things**:

1. **Create structure** (graph / tree / plan)
2. **Link causal relations** (A → B → C)
3. **Simulate paths** (non-evaluative)
4. **Output "structural alternatives"** (no preference)

**Reasoning Module does NOT:**
- ❌ Decide ALLOW / BLOCK
- ❌ Call GateCore
- ❌ Modify EPS / Energy
- ❌ Create Memory
- ❌ Call Kernel
- ❌ Use thresholds
- ❌ Optimize outcome
- ❌ Score alternatives
- ❌ Infer intent
- ❌ Call LLM directly

**If any of the above occurs → Reasoning Breach**

---

## 🚫 Absolute Prohibitions (HARD LOCK)

Reasoning Module **MUST NOT**:

### Decision Operations
- ❌ Decide ALLOW / BLOCK
- ❌ Call GateCore
- ❌ Override gate verdicts
- ❌ Make safety evaluations

### Energy Operations
- ❌ Modify EPS / Energy
- ❌ Call Kernel
- ❌ Compute energies
- ❌ Adjust energy parameters

### Memory Operations
- ❌ Create Memory
- ❌ Write Memory
- ❌ Modify Memory
- ❌ Access Memory (except read-only queries)

### Evaluation Operations
- ❌ Use thresholds
- ❌ Optimize outcome
- ❌ Score alternatives
- ❌ Rank options
- ❌ Assign probabilities
- ❌ Calculate utilities

### Semantic Operations
- ❌ Infer intent
- ❌ Interpret meaning
- ❌ Classify content
- ❌ Extract entities

### External Operations
- ❌ Call LLM directly
- ❌ Make network calls
- ❌ Access databases
- ❌ Read config files (except structure templates)

---

## 📥 Input Contract (STRICT)

### Allowed Inputs

```python
@dataclass
class ReasoningInput:
    trajectory: Trajectory              # From WM Controller only
    wm_decision_hint: Optional[str]     # Informational only
    context: Dict[str, Any]            # Informational only
    trace_id: str                      # Trace identifier
```

**Rules:**
- ✅ `trajectory` **MUST** come from WM Controller only
- ❌ **MUST NOT** create new trajectory
- ❌ **MUST NOT** modify input trajectory
- ✅ `context` is informational only (no semantic interpretation)
- ✅ `wm_decision_hint` is informational only (not a command)

**Input Validation:**
- ✅ Check for malformed trajectory
- ✅ Check for missing context
- ❌ **MUST NOT** auto-correct or guess

---

## 📤 Output Contract (STRICT)

### ReasoningOutput Structure

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
    trace_id: str                      # Trace identifier
```

**Output Rules:**
- ✅ Structure only (graph, plan, tree, simulation)
- ✅ Assumptions (structural preconditions)
- ✅ Constraints (structural requirements)
- ❌ **MUST NOT** include verdict
- ❌ **MUST NOT** include score
- ❌ **MUST NOT** include preference
- ❌ **MUST NOT** include recommendation

**What Output IS:**
- ✅ Structural relationships
- ✅ Causal chains
- ✅ Temporal sequences
- ✅ Constraint mappings

**What Output IS NOT:**
- ❌ Decision verdict
- ❌ Preference ranking
- ❌ Probability distribution
- ❌ Utility scores
- ❌ Semantic interpretation

---

## 🧩 Allowed Reasoning Types

### 7.1 Causal Graph

**Structure:**
```
A → B → C
```

**Rules:**
- ✅ Causal relationships only
- ✅ No weights
- ✅ No probabilities
- ✅ No utilities
- ✅ No semantic labels

**Example:**
```python
# ✅ ALLOWED
graph = {
    "nodes": ["A", "B", "C"],
    "edges": [
        ("A", "B"),
        ("B", "C")
    ]
}
```

**Forbidden:**
```python
# ❌ FORBIDDEN
graph = {
    "A": {"weight": 0.7, "probability": 0.8}  # Evaluation
}
```

---

### 7.2 Temporal Plan

**Structure:**
```
Step 1 → Step 2 → Step 3
```

**Rules:**
- ✅ Temporal sequence only
- ✅ No "should" or "good" labels
- ✅ No preference ranking
- ✅ No optimization

**Example:**
```python
# ✅ ALLOWED
plan = {
    "steps": [
        {"id": 1, "action": "A"},
        {"id": 2, "action": "B"},
        {"id": 3, "action": "C"}
    ],
    "order": "sequential"
}
```

**Forbidden:**
```python
# ❌ FORBIDDEN
plan = {
    "steps": [
        {"id": 1, "action": "A", "score": 0.9},  # Evaluation
        {"id": 2, "action": "B", "preferred": True}  # Preference
    ]
}
```

---

### 7.3 Constraint Mapping

**Structure:**
```
Action X requires {C1, C2}
```

**Rules:**
- ✅ Structural constraints only
- ✅ Precondition mapping
- ❌ **MUST NOT** evaluate suitability
- ❌ **MUST NOT** assess feasibility

**Example:**
```python
# ✅ ALLOWED
constraints = {
    "action_X": {
        "requires": ["C1", "C2"],
        "preconditions": ["P1", "P2"]
    }
}
```

**Forbidden:**
```python
# ❌ FORBIDDEN
constraints = {
    "action_X": {
        "feasibility": 0.8,  # Evaluation
        "suitability": "high"  # Assessment
    }
}
```

---

### 7.4 Counterfactual Simulation (Structural Only)

**Structure:**
```
If A then B
If A' then B'
```

**Rules:**
- ✅ Structural simulation only
- ✅ No selection
- ✅ No judgment
- ✅ No preference

**Example:**
```python
# ✅ ALLOWED
simulations = [
    {"condition": "A", "consequence": "B"},
    {"condition": "A'", "consequence": "B'"}
]
```

**Forbidden:**
```python
# ❌ FORBIDDEN
simulations = [
    {"condition": "A", "consequence": "B", "better": True},  # Judgment
    {"condition": "A'", "consequence": "B'", "chosen": False}  # Selection
]
```

---

## 🔗 Relationship with Other Modules

| Module | Relationship | Access Pattern |
|--------|--------------|----------------|
| **WM Controller** | Receives trajectory | One-way (WM → Reasoning) |
| **Decision** | Provides structure | One-way (Reasoning → Decision) |
| **GateCore** | ❌ No access | Reasoning does not call GateCore |
| **Kernel** | ❌ No access | Reasoning does not call Kernel |
| **Memory** | ❌ No write | Reasoning reads memory only (if needed) |

**Data Flow:**
```
WM Controller
    ↓ (trajectory)
Reasoning Module
    ↓ (structure)
Decision Module
```

**Rules:**
- ✅ One-way dependency only
- ❌ Reasoning **MUST NOT** call WM Controller
- ❌ Reasoning **MUST NOT** call GateCore
- ❌ Reasoning **MUST NOT** call Kernel
- ❌ Reasoning **MUST NOT** write Memory

---

## 🔄 Determinism Requirement

Reasoning Module **MUST** be:
- ✅ Deterministic (same input → same output)
- ✅ Reproducible (no randomness)
- ✅ Stateless (no memory between calls)
- ✅ Side-effect free (no state modification)

**Guarantee:**
```
Same input → Same structure
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

Reasoning Module **MAY** raise errors for:
- ✅ Malformed trajectory
- ✅ Missing context
- ✅ Unsupported structure type
- ✅ Invalid constraint mapping

### Error Handling Rules

**On Error:**
- ✅ **RAISE** exception immediately
- ✅ **DO NOT** continue
- ✅ **DO NOT** fallback decision
- ✅ **DO NOT** auto resolution
- ✅ **DO NOT** heuristic guessing

**Forbidden:**
- ❌ Fallback decision
- ❌ Auto resolution
- ❌ Heuristic guessing
- ❌ Default structure

**Example:**
```python
# ✅ CORRECT
if not trajectory:
    raise ValueError("Empty trajectory")

# ❌ FORBIDDEN
if not trajectory:
    trajectory = default_trajectory  # Auto-resolution
    return default_structure  # Fallback
```

---

## 🧪 Testing Requirements

### Mandatory Tests

All tests **MUST** verify:

- [ ] Reasoning does not modify trajectory
- [ ] No energy change (EPS unchanged)
- [ ] No decision triggered
- [ ] Output has no score / verdict
- [ ] Identical input → identical structure
- [ ] No side effects
- [ ] No external calls
- [ ] No memory writes

### Test Examples

```python
# Determinism test
def test_determinism():
    input_trajectory = create_test_trajectory()
    output1 = reasoning_module.process(input_trajectory)
    output2 = reasoning_module.process(input_trajectory)
    assert output1 == output2  # Must be identical

# Isolation test
def test_isolation():
    # Verify no imports from other layers
    assert "gate" not in reasoning_module.__imports__
    assert "kernel" not in reasoning_module.__imports__
    assert "memory" not in reasoning_module.__imports__

# No evaluation test
def test_no_evaluation():
    output = reasoning_module.process(trajectory)
    assert "score" not in output
    assert "verdict" not in output
    assert "preference" not in output
```

---

## 🛡️ Security & Safety Rationale

**Reasoning is dangerous when:**
- ❌ It starts choosing (becomes decision-maker)
- ❌ It starts optimizing (becomes evaluator)
- ❌ It starts scoring (becomes judge)

**This spec prevents:**
- ✅ Covert decision logic (hidden in reasoning)
- ✅ Hidden policy injection (policy in structure)
- ✅ Emergent autonomy (reasoning becomes agent)

**Why This Matters:**
If Reasoning makes decisions, the system bypasses GateCore and becomes unsafe.

---

## 🔍 Audit Checklist

Auditor **MUST** confirm:

### Code Inspection
- [ ] No imports from `gate/`
- [ ] No imports from `kernel/`
- [ ] No imports from `memory/` (except read-only)
- [ ] No numeric thresholds
- [ ] No probabilistic scoring
- [ ] No randomness
- [ ] No learning

### Function Inspection
- [ ] No decision-making functions
- [ ] No evaluation functions
- [ ] No scoring functions
- [ ] No optimization functions
- [ ] No memory write functions

### Output Inspection
- [ ] Output has no verdict
- [ ] Output has no score
- [ ] Output has no preference
- [ ] Output is structure only

---

## 📋 Examples

### Example (VALID)

**INPUT:**
```python
trajectory = Trajectory(
    states=[eps8_state_1, eps8_state_2],
    trace_id="abc123"
)
```

**OUTPUT:**
```python
ReasoningOutput(
    structure_type="graph",
    structure={
        "nodes": ["A", "B", "C"],
        "edges": [
            ("A", "B"),
            ("B", "C")
        ]
    },
    assumptions=[
        "Preconditions satisfied",
        "Constraints met"
    ],
    constraints=[
        "Action C requires B",
        "Action B requires A"
    ]
)
```

**Analysis:**
- ✅ Structure only (graph)
- ✅ No verdict
- ✅ No score
- ✅ No preference

---

### Example (INVALID)

**❌ FORBIDDEN OUTPUT:**
```python
# ❌ FORBIDDEN: Evaluation
ReasoningOutput(
    structure_type="plan",
    structure={
        "steps": [
            {"action": "A", "score": 0.9},  # Evaluation
            {"action": "B", "better": True}  # Preference
        ]
    }
)

# ❌ FORBIDDEN: Decision
ReasoningOutput(
    structure_type="graph",
    structure={...},
    verdict="ALLOW"  # Decision
)

# ❌ FORBIDDEN: Probability
ReasoningOutput(
    structure_type="simulation",
    structure={
        "scenarios": [
            {"condition": "A", "probability": 0.7}  # Evaluation
        ]
    }
)
```

---

## 📋 Summary (LOCKED INTENT)

**Reasoning is:**
- ✅ A map (structural relationships)
- ✅ A planner (temporal sequences)
- ✅ A graph builder (causal chains)

**Reasoning is NOT:**
- ❌ Walking (does not execute)
- ❌ Choosing (does not decide)
- ❌ Evaluating (does not assess)

**If Reasoning chooses, the system cheats itself.**

---

## 📚 Related Specifications

- **WM Controller:** `docs/WM_CONTROLLER_SPEC.md`
- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Memory Field Spec:** `docs/MEMORY_FIELD_SPEC.md`
- **Perception Boundary:** `docs/PERCEPTION_BOUNDARY_SPEC.md`

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
- Reasoning breach
- System redesign required
- Cannot be patched

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent Reasoning from becoming a "fake brain"  
**Authority:** Core Team  
**Enforcement:** Code review + automated import checks

