# CLI Execution Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — CLI Execution Boundaries  
**Scope:** CLI Tool Execution Rules  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This specification ensures that CLI:
- ✅ Is an **operator console**
- ✅ Is an **inspection tool**
- ✅ Is a **controlled execution trigger**
- ❌ Is **NOT** an execution engine

**Why This Matters:**
If CLI is not locked, tools, scripts, and engineers will bypass runtime without realizing it, causing semantic contamination of the entire system.

---

## 🔒 CLI Role Definition

**CLI = Supervisor Interface**

**CLI can do:**
- ✅ Inspect (read-only)
- ✅ Replay (deterministic)
- ✅ Simulate (dry-run)
- ✅ Validate config
- ✅ Submit execution request

**CLI MUST NOT:**
- ❌ Call kernel directly
- ❌ Create trajectory directly
- ❌ Write memory directly
- ❌ Override gate
- ❌ Inject EPS8 directly
- ❌ Bypass runtime

---

## 📥 CLI → System Contract

### CLIRequest Structure

```python
@dataclass
class CLIRequest:
    command: str                 # Command name
    args: Dict[str, Any]         # Command arguments
    mode: Literal[
        "inspect",               # Read-only inspection
        "simulate",              # Dry-run (no kernel)
        "execute"                # Full execution (via runtime)
    ]
    trace_id: Optional[str]      # Trace ID (if replaying)
    user_id: Optional[str]       # User identifier
    timestamp: float             # Request timestamp
```

**Rules:**
- ✅ All CLI operations **MUST** use `CLIRequest`
- ✅ All requests **MUST** be validated
- ✅ All requests **MUST** be logged

---

## 🚧 Execution Lock Rule

**CLI NEVER executes logic**  
**CLI ONLY sends request**  
**Runtime decides execution**

**Data Flow:**
```
CLI
    ↓ (CLIRequest)
Runtime.submit(request)
    ↓
GateCore (if execute mode)
    ↓
WM Controller
    ↓
Runtime Loop
    ↓
Kernel (if allowed)
```

**CLI never calls kernel directly.**

---

## ✅ Allowed CLI Commands

| Command Type | Allowed | Notes |
|--------------|---------|-------|
| **inspect** | ✅ | Read-only (no execution) |
| **replay** | ✅ | Deterministic (replay existing trace) |
| **simulate** | ✅ | Dry-run (NO kernel, NO memory write) |
| **execute** | ⚠️ | Must pass Gate + Runtime |
| **kernel** | ❌ | Forbidden (direct kernel call) |
| **force** | ❌ | Forbidden (bypass gate) |
| **bypass** | ❌ | Forbidden (bypass runtime) |

### Command Details

#### inspect
- ✅ Read-only operations
- ✅ No execution
- ✅ No kernel calls
- ✅ No memory writes

**Example:**
```bash
cog_cli memory inspect --field episodic
cog_cli trace view --trace-id abc123
```

#### replay
- ✅ Deterministic replay
- ✅ Uses existing trace
- ✅ No new execution
- ✅ No kernel calls (uses cached results)

**Example:**
```bash
cog_cli replay --log-file trajectory.log
```

#### simulate
- ✅ Dry-run mode
- ✅ **NO kernel calls**
- ✅ **NO memory writes**
- ✅ **NO side effects**
- ✅ Uses cached/mock data

**Example:**
```bash
cog_cli run --simulate --input input.json
```

#### execute
- ⚠️ Full execution
- ⚠️ **MUST** pass GateCore
- ⚠️ **MUST** go through Runtime
- ⚠️ **MUST** have trace_id

**Example:**
```bash
cog_cli run --execute --input input.json
```

---

## 🚫 Hard Lock: CLI Safety Guard

### CLISafety Class

```python
class CLISafety:
    """
    CLI safety guard.
    Prevents forbidden operations.
    """
    
    FORBIDDEN_COMMANDS = [
        "kernel",
        "energy_raw",
        "force_execute",
        "bypass_gate",
        "bypass_runtime",
        "inject_eps8",
        "write_memory",
        "override_gate",
        "direct_kernel"
    ]
    
    FORBIDDEN_MODES = [
        "force",
        "bypass",
        "direct"
    ]
    
    def validate(self, request: CLIRequest) -> None:
        """
        Validate CLI request.
        
        Raises:
            CLIViolation: If request violates rules
        """
        # Guard 1: Forbidden commands
        if request.command in self.FORBIDDEN_COMMANDS:
            raise CLIViolation(
                f"Forbidden CLI command: {request.command}"
            )
        
        # Guard 2: Forbidden modes
        if request.mode in self.FORBIDDEN_MODES:
            raise CLIViolation(
                f"Forbidden CLI mode: {request.mode}"
            )
        
        # Guard 3: Execute mode validation
        if request.mode == "execute":
            if not request.trace_id:
                raise CLIViolation(
                    "trace_id required for execute mode"
                )
        
        # Guard 4: Log request
        self._log_request(request)
```

**Enforcement:**
- ✅ All CLI requests **MUST** be validated
- ✅ Forbidden commands are **BLOCKED**
- ✅ Violations are **LOGGED**

---

## 🔄 CLI Execution Flow

### Canonical Flow

```
CLI
    ↓ (Build CLIRequest)
CLISafety.validate(request)
    ↓ (If valid)
Runtime.submit(request)
    ↓
GateCore (if execute mode)
    ↓ (If ALLOW)
WM Controller
    ↓
Runtime Loop
    ↓
Kernel (if needed)
    ↓
Action
    ↓
Output
```

**Rules:**
- ✅ CLI **MUST** build `CLIRequest`
- ✅ CLI **MUST** validate via `CLISafety`
- ✅ CLI **MUST** submit to Runtime
- ❌ CLI **MUST NOT** call kernel directly
- ❌ CLI **MUST NOT** bypass Runtime

---

## 🧪 Dry-Run Mode (RECOMMENDED)

### Simulate Mode

```bash
cog_cli run --simulate --input input.json
```

**Guarantees:**
- ✅ **NO kernel** calls
- ✅ **NO memory** writes
- ✅ **NO side effects**
- ✅ Uses cached/mock data
- ✅ Safe for testing

**Use Cases:**
- Testing CLI commands
- Validating input format
- Checking config
- Debugging workflows

---

## 📊 Audit Requirement

Every CLI execution **MUST** log:

```json
{
  "trace_id": "abc123",
  "cli_user": "operator_001",
  "command": "run",
  "mode": "execute",
  "args": {...},
  "allowed": true,
  "violations": [],
  "timestamp": "2024-12-01T10:30:00Z",
  "version": "v1.0"
}
```

**Requirements:**
- ✅ All CLI requests logged
- ✅ All violations logged
- ✅ All executions traced
- ✅ User identification
- ✅ Timestamp precision

---

## 🚫 Forbidden CLI Operations

### Direct Operations
- ❌ **MUST NOT** call kernel directly
- ❌ **MUST NOT** create trajectory directly
- ❌ **MUST NOT** write memory directly
- ❌ **MUST NOT** override gate

### Bypass Operations
- ❌ **MUST NOT** bypass runtime
- ❌ **MUST NOT** bypass gate
- ❌ **MUST NOT** bypass WM Controller

### Injection Operations
- ❌ **MUST NOT** inject EPS8 directly
- ❌ **MUST NOT** inject energy values
- ❌ **MUST NOT** inject decisions

**Detection:**
- Code review
- Runtime monitoring
- Audit logs

---

## 🔍 Audit Checklist

To verify CLI execution compliance:

- [ ] All CLI commands go through `CLISafety`
- [ ] No direct kernel calls from CLI
- [ ] No trajectory creation from CLI
- [ ] No memory writes from CLI
- [ ] No gate overrides from CLI
- [ ] All execute requests have trace_id
- [ ] All requests are logged
- [ ] All violations are blocked
- [ ] Simulate mode has no side effects

---

## 📋 Examples

### Example (VALID)

```bash
# ✅ VALID: Inspect (read-only)
cog_cli memory inspect --field episodic

# ✅ VALID: Simulate (dry-run)
cog_cli run --simulate --input input.json

# ✅ VALID: Execute (via runtime)
cog_cli run --execute --input input.json --trace-id abc123
```

### Example (INVALID)

```bash
# ❌ FORBIDDEN: Direct kernel call
cog_cli kernel compute --I 0.8 --P 0.6

# ❌ FORBIDDEN: Force execution
cog_cli run --force --input input.json

# ❌ FORBIDDEN: Bypass gate
cog_cli run --bypass-gate --input input.json
```

---

## 📋 Summary (LOCKED INTENT)

**CLI is:**
- ✅ Supervisor interface (operator console)
- ✅ Inspection tool (read-only)
- ✅ Execution trigger (controlled)

**CLI is NOT:**
- ❌ Execution engine (does not execute)
- ❌ Decision maker (does not decide)
- ❌ Kernel caller (does not call kernel)

**If CLI bypasses runtime, the system is semantically contaminated.**

---

## 📚 Related Specifications

- **Kernel Invocation:** `docs/KERNEL_INVOCATION_SPEC.md`
- **Runtime Loop:** `docs/RUNTIME_LOOP_SPEC.md`
- **WM Controller:** `docs/WM_CONTROLLER_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`

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
**Purpose:** Prevent CLI from bypassing runtime  
**Authority:** Core Team  
**Enforcement:** Code review + CLI safety guards

