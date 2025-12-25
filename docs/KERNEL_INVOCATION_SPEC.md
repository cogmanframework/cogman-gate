# Kernel Invocation Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Kernel Invocation Boundary  
**Scope:** C++ Kernel Invocation Rules  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This specification defines **strict boundaries** for invoking the C++ Kernel.

It ensures that Kernel:
- ❌ Is **NOT** called directly from CLI
- ❌ Is **NOT** called bypassing Gate / Runtime
- ❌ Is **NOT** used as a raw calculator

**Kernel = Pure Physics Executor ONLY**

**Why This Matters:**
Without this boundary, Kernel can be called from anywhere, bypassing safety gates and breaking system architecture.

---

## 🔒 Kernel Invocation Rule (ABSOLUTE)

**✅ Kernel can ONLY be invoked from Runtime**

**❌ Forbidden Invocations:**
- ❌ **MUST NOT** be called from CLI
- ❌ **MUST NOT** be called from Reasoning
- ❌ **MUST NOT** be called from Memory
- ❌ **MUST NOT** be called from Tools / Scripts directly
- ❌ **MUST NOT** be called from Perception
- ❌ **MUST NOT** be called from WM Controller
- ❌ **MUST NOT** be called from GateCore

**Allowed Call Path (唯一):**
```
INPUT
    → Sensory
    → Perception
    → GateCore
    → WorkingMemoryController
    → RuntimeLoop
    → KernelInvocation
    → Cognitive Modules
    → Output
```

**No other path exists.**

---

## 📥 Kernel Interface Contract

### Kernel Input (STRICT)

```python
@dataclass(frozen=True)
class KernelInvocationContext:
    trace_id: str                # REQUIRED
    eps8: EPS8State              # Canonical only
    neural_components: NeuralComponents  # Required
    theta_phase: float           # Required
    E_pred: float                # Required
    decision_params: DecisionParams  # Required
    mode: Literal[
        "maxwell",
        "quantum",
        "einstein",
        "default"
    ] = "default"
    caller: Literal["runtime"]   # MUST be "runtime"
```

**Input Rules:**
- ✅ All inputs are numeric (no strings, no semantic labels)
- ✅ `trace_id` is **REQUIRED** (for audit)
- ✅ `caller` **MUST** be "runtime" (enforced)
- ✅ `eps8` is canonical EPS-8 state only
- ❌ **MUST NOT** include text, tokens, memory IDs, reasoning results

### Kernel Output

```python
@dataclass
class KernelResult:
    energy_state: EnergyState    # All computed energies
    field_state: Optional[np.ndarray]  # Field evolution (if applicable)
    energy_metrics: Dict[str, float]  # Additional metrics
    mode: str                    # Computation mode used
    trace_id: str                # Trace identifier
    timestamp: float             # Computation timestamp
```

**Output Rules:**
- ✅ All outputs are numeric
- ✅ No decisions (only numeric verdict codes)
- ✅ No labels (only numeric values)
- ✅ No text (only numbers)
- ✅ No suggestions (only computed values)

---

## 🛡️ Invocation Guard (MANDATORY)

### KernelInvoker Class

```python
class KernelInvoker:
    """
    Sole authority for kernel invocation.
    Enforces invocation rules.
    """
    
    FORBIDDEN_CALLERS = [
        "cli",
        "reasoning",
        "memory",
        "perception",
        "wm_controller",
        "gatecore",
        "tool",
        "script"
    ]
    
    def invoke(self, ctx: KernelInvocationContext) -> KernelResult:
        """
        Invoke kernel with strict validation.
        
        Raises:
            KernelViolation: If invocation rules are violated
        """
        # Guard 1: Caller validation
        if ctx.caller != "runtime":
            raise KernelViolation(
                f"Kernel can only be invoked by runtime, got: {ctx.caller}"
            )
        
        # Guard 2: Trace ID validation
        if not ctx.trace_id:
            raise KernelViolation("trace_id is required for kernel invocation")
        
        # Guard 3: EPS-8 state validation
        if not ctx.eps8.validate():
            raise KernelViolation("Invalid EPS-8 state")
        
        # Guard 4: Log invocation
        self._log_invocation(ctx)
        
        # Guard 5: Call C++ kernel
        return self._call_cpp_kernel(ctx)
    
    def _call_cpp_kernel(self, ctx: KernelInvocationContext) -> KernelResult:
        """Call C++ kernel via bridge."""
        # Implementation via bridge.kernel_bridge
        pass
```

**Enforcement:**
- ✅ All invocations **MUST** go through `KernelInvoker`
- ✅ Direct kernel calls are **FORBIDDEN**
- ✅ Violations are **LOGGED** and **BLOCKED**

---

## 🚫 What Kernel NEVER Receives

Kernel **MUST NEVER** see:

### Semantic Data
- ❌ Text
- ❌ Tokens
- ❌ Semantic labels
- ❌ Intent flags
- ❌ Context names

### System Data
- ❌ Memory IDs
- ❌ Reasoning results
- ❌ Plans
- ❌ User input
- ❌ CLI args

### Policy Data
- ❌ Policy rules
- ❌ Safety levels
- ❌ Domain constraints

**Kernel sees numbers only.**

**Example (Forbidden):**
```python
# ❌ FORBIDDEN
ctx = KernelInvocationContext(
    eps8=eps8_state,
    text="user input",  # Semantic data
    intent="dangerous",  # Semantic label
    caller="cli"  # Forbidden caller
)
```

---

## 📤 What Kernel NEVER Returns

Kernel **MUST NEVER** return:

### Decision Data
- ❌ Decision verdicts (semantic)
- ❌ Boolean verdicts (semantic)
- ❌ Recommendations

### Semantic Data
- ❌ Labels
- ❌ Text
- ❌ Suggestions
- ❌ Interpretations

### System Commands
- ❌ Memory write commands
- ❌ Action triggers
- ❌ State modifications

**Kernel returns:**
- ✅ Field evolution only (numeric)
- ✅ Energy values only (numeric)
- ✅ Numeric codes only (no semantics)

**Example (Forbidden):**
```python
# ❌ FORBIDDEN
result = KernelResult(
    energy_state=energy,
    decision="ALLOW",  # Semantic verdict
    recommendation="proceed"  # Semantic suggestion
)
```

---

## ⚠️ Failure Policy

If Kernel invocation violates spec:

### Violation Handling

1. **Block Execution**
   - ✅ **ABORT** current execution
   - ✅ **DO NOT** proceed

2. **Log Violation**
   - ✅ Log to `storage/audit/kernel_violation.log`
   - ✅ Include full context
   - ✅ Include trace_id

3. **Mark Trace as INVALID**
   - ✅ Set trace status to `INVALID`
   - ✅ Prevent further processing
   - ✅ Flag for audit review

**Example:**
```python
# Violation detected
violation = {
    "trace_id": ctx.trace_id,
    "caller": ctx.caller,
    "violation_type": "forbidden_caller",
    "timestamp": time.time(),
    "context": str(ctx)
}

log_violation(violation)
mark_trace_invalid(ctx.trace_id)
raise KernelViolation("Forbidden kernel invocation")
```

---

## 🏗️ Design Rationale

**Analogy:**
- **Kernel** = CPU / GPU (computation unit)
- **Runtime** = OS (orchestration)
- **WM Controller** = Scheduler (coordination)
- **CLI** = Shell (user interface)

**Rule:**
> Shell must not call CPU directly

**Why:**
- ✅ Prevents bypass of safety gates
- ✅ Ensures proper orchestration
- ✅ Maintains audit trail
- ✅ Preserves system architecture

---

## 🔍 Audit Checklist

To verify kernel invocation compliance:

- [ ] All kernel calls go through `KernelInvoker`
- [ ] No direct kernel calls from CLI
- [ ] No direct kernel calls from Reasoning
- [ ] No direct kernel calls from Memory
- [ ] All invocations have `trace_id`
- [ ] All invocations have `caller="runtime"`
- [ ] All inputs are numeric (no semantic data)
- [ ] All outputs are numeric (no semantic data)
- [ ] Violations are logged and blocked
- [ ] Traces are marked INVALID on violation

---

## 📚 Related Specifications

- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **Runtime Loop:** `docs/RUNTIME_LOOP_SPEC.md`
- **WM Controller:** `docs/WM_CONTROLLER_SPEC.md`
- **CLI Execution:** `docs/CLI_EXECUTION_SPEC.md`

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
**Purpose:** Prevent unauthorized kernel invocation  
**Authority:** Core Team  
**Enforcement:** Code review + runtime guards

