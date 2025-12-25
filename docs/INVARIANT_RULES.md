# Invariant Rules Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED — System Invariants  
**Scope:** System-Wide Invariant Rules  
**Last Updated:** 2024-12

---

## 🎯 Purpose

This specification defines **invariant rules** that **MUST NOT** be violated, regardless of who touches the system.

These rules are:
- ✅ **Non-negotiable** (cannot be bypassed)
- ✅ **System-wide** (apply to all modules)
- ✅ **Enforceable** (can be checked)
- ✅ **Auditable** (can be verified)

**Why This Matters:**
Without invariant rules, the system will drift and break silently. These rules are the **foundation** that prevents system failure.

---

## 🔒 Invariant Categories

### 1. Kernel Invariants

**INV-1: Kernel is pure numeric engine**
- ✅ Kernel **MUST** only compute numeric values
- ❌ Kernel **MUST NOT** interpret semantic meaning
- ❌ Kernel **MUST NOT** make decisions
- ❌ Kernel **MUST NOT** access external resources

**INV-2: Kernel can only be invoked from Runtime**
- ✅ Kernel **MUST** be called via Runtime only
- ❌ Kernel **MUST NOT** be called from CLI
- ❌ Kernel **MUST NOT** be called from Reasoning
- ❌ Kernel **MUST NOT** be called from Memory

**INV-3: Kernel inputs are numeric only**
- ✅ All kernel inputs **MUST** be numeric
- ❌ Kernel **MUST NOT** receive text, tokens, or semantic labels
- ❌ Kernel **MUST NOT** receive memory IDs or reasoning results

**INV-4: Kernel outputs are numeric only**
- ✅ All kernel outputs **MUST** be numeric
- ❌ Kernel **MUST NOT** return decisions, labels, or suggestions

---

### 2. GateCore Invariants

**INV-5: GateCore is final authority**
- ✅ GateCore verdict **MUST** be final
- ❌ GateCore verdict **MUST NOT** be overridden
- ❌ GateCore verdict **MUST NOT** be reinterpreted

**INV-6: GateCore is deterministic**
- ✅ Same input **MUST** produce same output
- ❌ GateCore **MUST NOT** use randomness
- ❌ GateCore **MUST NOT** learn or adapt

**INV-7: GateCore decision order is locked**
- ✅ Decision logic **MUST** follow canonical order
- ❌ Decision order **MUST NOT** be changed
- ❌ Decision order **MUST NOT** be reordered

**INV-8: Safety rule failure always blocks**
- ✅ If S == 0, verdict **MUST** be BLOCK
- ❌ Safety rule failure **MUST NOT** be bypassed
- ❌ Safety rule failure **MUST NOT** be overridden

---

### 3. Memory Invariants

**INV-9: Memory has no authority**
- ✅ Memory **MUST NOT** initiate actions
- ✅ Memory **MUST NOT** make decisions
- ✅ Memory **MUST NOT** override gates
- ✅ Memory **MUST NOT** trigger behavior

**INV-10: Memory is read-only for most modules**
- ✅ Memory **MUST** be read-only for Reasoning
- ✅ Memory **MUST** be read-only for Perception
- ✅ Memory **MUST** be read-only for Kernel
- ✅ Only WM Controller and Consolidation Engine can write

**INV-11: Memory writes are controlled**
- ✅ Memory **MUST NOT** be written during gate evaluation
- ✅ Memory **MUST NOT** be written during kernel computation
- ✅ Memory **MUST NOT** be written during action execution

---

### 4. Perception Invariants

**INV-12: Perception has no semantic interpretation**
- ✅ Perception **MUST NOT** interpret meaning
- ✅ Perception **MUST NOT** classify content
- ✅ Perception **MUST NOT** extract entities
- ✅ Perception **MUST** only extract features and project energy

**INV-13: Perception is deterministic**
- ✅ Same input **MUST** produce same output
- ❌ Perception **MUST NOT** use randomness
- ❌ Perception **MUST NOT** learn or adapt

**INV-14: Perception does not access other layers**
- ✅ Perception **MUST NOT** call Kernel
- ✅ Perception **MUST NOT** call Memory
- ✅ Perception **MUST NOT** call GateCore
- ✅ Perception **MUST NOT** call WM Controller

---

### 5. Reasoning Invariants

**INV-15: Reasoning does not decide**
- ✅ Reasoning **MUST NOT** make decisions
- ✅ Reasoning **MUST NOT** call GateCore
- ✅ Reasoning **MUST NOT** evaluate or score
- ✅ Reasoning **MUST** only structure relationships

**INV-16: Reasoning output has no verdict**
- ✅ Reasoning output **MUST NOT** include verdict
- ✅ Reasoning output **MUST NOT** include score
- ✅ Reasoning output **MUST NOT** include preference
- ✅ Reasoning output **MUST** be structure only

**INV-17: Reasoning does not access Kernel**
- ✅ Reasoning **MUST NOT** call Kernel
- ✅ Reasoning **MUST NOT** modify energy
- ✅ Reasoning **MUST NOT** compute energies

---

### 6. Runtime Invariants

**INV-18: Runtime phases execute in order**
- ✅ Phases **MUST** execute in canonical order
- ❌ Phases **MUST NOT** be skipped
- ❌ Phases **MUST NOT** be reordered
- ❌ Phases **MUST NOT** be reversed

**INV-19: Runtime is deterministic**
- ✅ Same input sequence **MUST** produce same execution
- ❌ Runtime **MUST NOT** use randomness
- ❌ Runtime **MUST NOT** learn or adapt

**INV-20: Runtime does not interpret meaning**
- ✅ Runtime **MUST NOT** interpret semantic meaning
- ✅ Runtime **MUST NOT** make decisions
- ✅ Runtime **MUST** only orchestrate modules

---

### 7. CLI Invariants

**INV-21: CLI does not execute logic**
- ✅ CLI **MUST NOT** call Kernel directly
- ✅ CLI **MUST NOT** create trajectory directly
- ✅ CLI **MUST NOT** write memory directly
- ✅ CLI **MUST** only send requests to Runtime

**INV-22: CLI does not bypass Runtime**
- ✅ CLI **MUST NOT** bypass Runtime
- ✅ CLI **MUST NOT** bypass GateCore
- ✅ CLI **MUST NOT** bypass WM Controller

**INV-23: CLI does not modify trace state**
- ✅ CLI **MUST NOT** modify trace state
- ✅ CLI **MUST NOT** create trace
- ✅ CLI **MUST NOT** close trace

---

### 8. Trace Invariants

**INV-24: trace_id is immutable**
- ✅ `trace_id` **MUST NOT** change after creation
- ✅ `trace_id` **MUST** be unique
- ✅ `trace_id` **MUST** be used for all operations

**INV-25: Kernel invocation implies ACTIVE state**
- ✅ Kernel **MUST NOT** be called for non-ACTIVE traces
- ✅ All kernel calls **MUST** be logged in trace

**INV-26: Trace lifecycle log is append-only**
- ✅ Lifecycle log **MUST NOT** be modified
- ✅ Lifecycle log **MUST NOT** be deleted
- ✅ Lifecycle log **MUST** be append-only

**INV-27: INVALID trace cannot be archived**
- ✅ INVALID traces **MUST NOT** be archived
- ✅ INVALID traces **MUST** be logged for audit

---

### 9. Energy Variable Invariants

**INV-28: EPS-8 state is validated before kernel**
- ✅ EPS-8 state **MUST** be validated before kernel call
- ❌ Invalid EPS-8 state **MUST NOT** reach kernel

**INV-29: Energy values are finite**
- ✅ All energy values **MUST** be finite (no NaN, no infinity)
- ❌ NaN or infinity **MUST NOT** propagate through system

**INV-30: Energy variables have canonical domains**
- ✅ All energy variables **MUST** be in canonical domains
- ❌ Out-of-range values **MUST NOT** be accepted

---

### 10. System-Wide Invariants

**INV-31: No semantic leakage**
- ✅ Semantic meaning **MUST NOT** enter Kernel
- ✅ Semantic meaning **MUST NOT** enter Perception
- ✅ Semantic meaning **MUST NOT** enter Memory

**INV-32: No bypass of safety gates**
- ✅ Safety gates **MUST NOT** be bypassed
- ✅ GateCore **MUST NOT** be overridden
- ✅ Safety rules **MUST NOT** be ignored

**INV-33: All operations are traceable**
- ✅ All operations **MUST** have trace_id
- ✅ All operations **MUST** be logged
- ✅ All operations **MUST** be auditable

**INV-34: System is deterministic**
- ✅ Same input **MUST** produce same output
- ❌ System **MUST NOT** use randomness (unless seeded)
- ❌ System **MUST NOT** learn or adapt at runtime

---

## 🔍 Invariant Enforcement

### Enforcement Mechanisms

1. **Code Review**
   - All code changes **MUST** be reviewed for invariant compliance
   - Violations **MUST** be rejected

2. **Runtime Checks**
   - Runtime **MUST** check invariants during execution
   - Violations **MUST** abort execution

3. **Automated Tests**
   - All invariants **MUST** have automated tests
   - Tests **MUST** run on every commit

4. **Audit Tools**
   - Audit tools **MUST** verify invariants
   - Violations **MUST** be logged

---

## 📋 Invariant Checklist

To verify system compliance:

### Kernel Invariants
- [ ] Kernel is pure numeric engine
- [ ] Kernel only invoked from Runtime
- [ ] Kernel inputs are numeric only
- [ ] Kernel outputs are numeric only

### GateCore Invariants
- [ ] GateCore is final authority
- [ ] GateCore is deterministic
- [ ] Decision order is locked
- [ ] Safety rule failure always blocks

### Memory Invariants
- [ ] Memory has no authority
- [ ] Memory is read-only for most modules
- [ ] Memory writes are controlled

### Perception Invariants
- [ ] Perception has no semantic interpretation
- [ ] Perception is deterministic
- [ ] Perception does not access other layers

### Reasoning Invariants
- [ ] Reasoning does not decide
- [ ] Reasoning output has no verdict
- [ ] Reasoning does not access Kernel

### Runtime Invariants
- [ ] Runtime phases execute in order
- [ ] Runtime is deterministic
- [ ] Runtime does not interpret meaning

### CLI Invariants
- [ ] CLI does not execute logic
- [ ] CLI does not bypass Runtime
- [ ] CLI does not modify trace state

### Trace Invariants
- [ ] trace_id is immutable
- [ ] Kernel invocation implies ACTIVE state
- [ ] Trace lifecycle log is append-only
- [ ] INVALID trace cannot be archived

### Energy Variable Invariants
- [ ] EPS-8 state is validated before kernel
- [ ] Energy values are finite
- [ ] Energy variables have canonical domains

### System-Wide Invariants
- [ ] No semantic leakage
- [ ] No bypass of safety gates
- [ ] All operations are traceable
- [ ] System is deterministic

---

## 📋 Summary (LOCKED INTENT)

**These invariants are:**
- ✅ Non-negotiable (cannot be violated)
- ✅ System-wide (apply everywhere)
- ✅ Enforceable (can be checked)
- ✅ Auditable (can be verified)

**If any invariant is violated, the system is broken.**

---

## 📚 Related Specifications

- **Kernel Boundary:** `docs/KERNEL_BOUNDARY_SPEC.md`
- **GateCore Spec:** `docs/GATECORE_SPEC.md`
- **Memory Field Spec:** `docs/MEMORY_FIELD_SPEC.md`
- **Perception Boundary:** `docs/PERCEPTION_BOUNDARY_SPEC.md`
- **Reasoning Module:** `docs/REASONING_MODULE_SPEC.md`
- **Runtime Loop:** `docs/RUNTIME_LOOP_SPEC.md`
- **Kernel Invocation:** `docs/KERNEL_INVOCATION_SPEC.md`
- **CLI Execution:** `docs/CLI_EXECUTION_SPEC.md`
- **Trace Lifecycle:** `docs/TRACE_LIFECYCLE_SPEC.md`

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture approval
2. Safety approval
3. Security approval
4. Version bump
5. Impact analysis (all modules)

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on invariant violation)

**Violation Consequence:**
- System failure
- Architecture violation
- System redesign required
- Cannot be patched

---

**Status:** 🔒 LOCKED  
**Purpose:** Prevent system failure through invariant enforcement  
**Authority:** Core Team  
**Enforcement:** Code review + runtime checks + automated tests + audit tools

