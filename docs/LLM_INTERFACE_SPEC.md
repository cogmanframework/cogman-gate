# LLM Interface Specification

**Version:** v1.0-LOCKED  
**Status:** BOUNDARY LOCKED — Interface Only  
**Scope:** LLM Integration Boundary  
**Last Updated:** 2024-12

---

## 🎯 Purpose (วัตถุประสงค์)

This specification defines the **boundary for Large Language Model (LLM) usage** within Cogman Energetic Engine to:

- ✅ Prevent misinterpretation that LLM is the decision core
- ✅ Prevent bypass of runtime / gate / kernel
- ✅ Support audit, trace, and long-term maintenance
- ✅ Ensure system remains deterministic and auditable

> **LLM is classified as a Peripheral Interface ONLY.  
> It is NOT the Cognitive Core, NOT the Decision System, and NOT the Physics Engine.**

**Why This Matters:**
Without this boundary:
- System becomes LLM-centric (unpredictable)
- Audit trail is broken (LLM decisions are opaque)
- System cannot defend itself (LLM output is not ground truth)
- Long-term maintenance fails (LLM dependencies change)

---

## 🏗️ Design Principle (หลักการออกแบบ)

### Core Principles

1. **LLM ≠ Intelligence Core**
   - Intelligence resides in:
     - ✅ Kernel (C++)
     - ✅ GateCore
     - ✅ WM Controller
     - ✅ Energy & Trajectory System
   - ❌ LLM is NOT the intelligence

2. **LLM = Translator / Annotator / UI Layer**
   - LLM translates between human language and system state
   - LLM annotates system outputs for human consumption
   - LLM provides UI layer for interaction

3. **LLM Output Has No Authority**
   - LLM output does NOT affect system truth
   - LLM output does NOT override decisions
   - LLM output is advisory only

4. **All LLM Usage Must Be Traceable**
   - Every LLM call must be logged
   - Every LLM call must have trace_id
   - Every LLM call must be auditable

---

## ✅ Allowed Capabilities (สิ่งที่ LLM ทำได้)

LLM **MAY ONLY** perform the following:

### 3.1 Annotation & Explanation

**Purpose:** Explain system outputs in human language

**Allowed Operations:**
- ✅ Explain results that have already occurred
- ✅ Summarize trace / trajectory / gate decision
- ✅ Convert technical data → human language
- ✅ Generate human-readable reports

**Examples:**
- "Why was this trajectory blocked?"
- "Summarize GateCore decision"
- "Explain energy projection results"

**Constraints:**
- ❌ **MUST NOT** interpret meaning (only translate)
- ❌ **MUST NOT** generate new decisions
- ❌ **MUST NOT** modify system state

**Input:**
- System outputs (traces, decisions, energy states)
- Non-authoritative snapshots

**Output:**
- Human-readable text
- Explanations
- Summaries

---

### 3.2 Natural Language → Query Plan

**Purpose:** Convert human commands to query plans (NOT execution)

**Allowed Operations:**
- ✅ Parse natural language input
- ✅ Generate query plan structure
- ✅ Identify intent and parameters

**Example:**

**Input (User):**
```
"ดูว่าเมื่อกี้ระบบไม่ให้ทำเพราะอะไร"
```

**LLM Output:**
```json
{
  "intent": "inspect_gate_decision",
  "target": "last_trace",
  "parameters": {
    "trace_id": "trace_abc123"
  },
  "permission_required": true,
  "execution_path": "CLI → WM Controller → GateCore"
}
```

**Execution Flow:**
- LLM generates query plan
- Query plan goes through:
  - ✅ CLI safety checks
  - ✅ WM Controller
  - ✅ GateCore (if needed)
- System executes query plan (NOT LLM)

**Constraints:**
- ❌ **MUST NOT** execute query plan
- ❌ **MUST NOT** bypass safety checks
- ❌ **MUST NOT** directly access system state

---

### 3.3 Labeling / Tagging / Metadata

**Purpose:** Add semantic labels and metadata to system outputs

**Allowed Operations:**
- ✅ Add labels to traces
- ✅ Categorize outputs
- ✅ Add semantic tags
- ✅ Generate metadata

**Constraints:**
- ❌ **MUST NOT** affect energy computation
- ❌ **MUST NOT** affect trajectory
- ❌ **MUST NOT** affect decision
- ❌ **MUST NOT** modify system state

**Output:**
- Labels (advisory only)
- Tags (advisory only)
- Metadata (advisory only)

---

### 3.4 Text Rendering (Post-Decision Only)

**Purpose:** Generate human-readable text after decisions are made

**Allowed Operations:**
- ✅ Generate response text
- ✅ Generate reports
- ✅ Generate explanations
- ✅ Format output for display

**Timing Constraint:**
- ✅ **MUST** occur **AFTER** Action / Decision is confirmed
- ❌ **MUST NOT** occur before decision
- ❌ **MUST NOT** influence decision

**Example Flow:**
1. System makes decision (GateCore)
2. System executes action
3. System confirms completion
4. **THEN** LLM generates response text

**Constraints:**
- ❌ **MUST NOT** generate text before decision
- ❌ **MUST NOT** influence decision with text
- ❌ **MUST NOT** modify system state

---

## ❌ Forbidden Capabilities (สิ่งที่ LLM ห้ามทำเด็ดขาด)

LLM **MUST NOT**:

### 4.1 Energy Computation
- ❌ Compute energy (EPS-8, CORE-1 to CORE-9)
- ❌ Modify energy values
- ❌ Interpret energy meaning
- ❌ Generate energy projections

**Reason:** Energy computation is Kernel's responsibility

---

### 4.2 Kernel Access
- ❌ Call C++ Kernel directly
- ❌ Bypass Kernel boundary
- ❌ Invoke kernel functions
- ❌ Modify kernel state

**Reason:** Kernel is only accessible via Runtime

---

### 4.3 Gate Evaluation
- ❌ Evaluate or override GateCore
- ❌ Make safety decisions
- ❌ Bypass gate checks
- ❌ Modify gate thresholds

**Reason:** GateCore is final authority

---

### 4.4 Trajectory Management
- ❌ Create trajectory
- ❌ Modify trajectory
- ❌ Delete trajectory
- ❌ Bypass trajectory builder

**Reason:** Trajectory is managed by TrajectoryBuilder

---

### 4.5 State Modification
- ❌ Modify EPS-8 state
- ❌ Modify energy state
- ❌ Modify trace state
- ❌ Modify memory state

**Reason:** State modification is controlled by WM Controller

---

### 4.6 Action Execution
- ❌ Trigger action
- ❌ Execute motor command
- ❌ Execute system command
- ❌ Bypass action layer

**Reason:** Actions are executed by Action layer

---

### 4.7 Memory Access
- ❌ Write memory directly
- ❌ Modify memory state
- ❌ Bypass memory controller
- ❌ Access memory without permission

**Reason:** Memory is managed by Memory Controller

---

### 4.8 Runtime Bypass
- ❌ Bypass Runtime Loop
- ❌ Skip execution phases
- ❌ Modify execution order
- ❌ Interrupt execution

**Reason:** Runtime Loop is the only execution path

---

### 4.9 Decision Making
- ❌ Make decisions
- ❌ Override decisions
- ❌ Interpret decisions
- ❌ Generate decisions

**Reason:** Decisions are made by GateCore and WM Controller

---

**Violation Consequence:**
- ✅ Architecture violation
- ✅ System redesign required
- ✅ Cannot be patched

---

## 🔐 Invocation Rules (กฎการเรียกใช้)

### Allowed Callers

LLM **MAY** be called from:

1. **CLI (`cog_cli`)**
   - For user interaction
   - For query plan generation
   - For output rendering

2. **WM Controller (read-only context)**
   - For annotation
   - For explanation
   - For reporting

3. **Output / Reporting Module**
   - For text rendering
   - For report generation
   - For display formatting

---

### Forbidden Callers

LLM **MUST NOT** be called from:

- ❌ Kernel
- ❌ GateCore
- ❌ Memory Field
- ❌ Trajectory Builder
- ❌ Perception / Energy Estimator
- ❌ Reasoning Module
- ❌ Action Module

**Reason:** These modules are core system components and must not depend on LLM

---

## 📊 Data Access Policy

### LLM Data Access Rules

1. **Read-Only Access**
   - ✅ LLM can read snapshots
   - ❌ LLM **MUST NOT** hold state
   - ❌ LLM **MUST NOT** modify data

2. **Data Sanitization**
   - ✅ All data sent to LLM **MUST** be sanitized
   - ✅ All data sent to LLM **MUST** be non-authoritative
   - ✅ All data sent to LLM **MUST** include `trace_id`

3. **Data Format**
   - ✅ Data **MUST** be in canonical format
   - ✅ Data **MUST** be versioned
   - ✅ Data **MUST** be traceable

4. **Data Retention**
   - ✅ LLM output **MUST NOT** be stored as ground truth
   - ✅ LLM output **MUST** be marked as advisory
   - ✅ LLM output **MUST** be logged

---

## 📝 Traceability & Logging

### Logging Requirements

Every LLM call **MUST** be logged with:

```json
{
  "trace_id": "trace_xxxx",
  "llm_task": "annotation | query_plan | rendering | labeling",
  "caller": "CLI | WM_CONTROLLER | OUTPUT_MODULE",
  "input_hash": "sha256_hash_of_input",
  "output_hash": "sha256_hash_of_output",
  "timestamp": "2024-12-01T10:30:00Z",
  "llm_provider": "openai | anthropic | local",
  "model": "gpt-4 | claude-3 | ...",
  "cost": 0.001,
  "latency_ms": 150
}
```

### Traceability Rules

1. **Every LLM call MUST have trace_id**
   - Links LLM call to system trace
   - Enables audit trail

2. **LLM output is advisory only**
   - Not ground truth
   - Not authoritative
   - Not used for decisions

3. **LLM output MUST be validated**
   - Checked for format
   - Checked for safety
   - Checked for compliance

---

## 🔒 Security & Safety

### Security Rules

1. **LLM Output Cannot Trigger Action**
   - ✅ LLM output **MUST NOT** directly trigger actions
   - ✅ LLM output **MUST** go through validation
   - ✅ LLM output **MUST** go through gate checks

2. **LLM Output Must Be Validated**
   - ✅ Format validation
   - ✅ Safety validation
   - ✅ Compliance validation

3. **LLM Output Has No Authority**
   - ✅ LLM output **MUST NOT** override gate
   - ✅ LLM output **MUST NOT** bypass safety
   - ✅ LLM output **MUST NOT** modify system state

4. **LLM Failure Must Not Break System**
   - ✅ If LLM fails, system **MUST** continue
   - ✅ If LLM fails, system **MUST** fallback to non-LLM output
   - ✅ If LLM fails, system **MUST** log error

---

## 🔗 Relationship to Other Specs

### LLM Interface Depends On

- ✅ **WM_CONTROLLER_SPEC.md**
  - LLM may be called from WM Controller (read-only)

- ✅ **TRACE_LIFECYCLE_SPEC.md**
  - All LLM calls must have trace_id

- ✅ **CLI_EXECUTION_SPEC.md**
  - LLM may be called from CLI

---

### LLM Interface Does NOT Dominate

- ✅ **KERNEL_INVOCATION_SPEC.md**
  - LLM cannot call Kernel

- ✅ **GATECORE_SPEC.md**
  - LLM cannot override GateCore

- ✅ **MEMORY_FIELD_SPEC.md**
  - LLM cannot write memory

- ✅ **PERCEPTION_BOUNDARY_SPEC.md**
  - LLM cannot access perception

- ✅ **REASONING_MODULE_SPEC.md**
  - LLM cannot access reasoning

- ✅ **RUNTIME_LOOP_SPEC.md**
  - LLM cannot bypass Runtime Loop

---

## 🛡️ Hard Invariants (MUST HOLD)

These invariants **MUST** hold at all times:

1. **LLM is NOT the intelligence core**
   - Intelligence is in Kernel, GateCore, WM Controller
   - LLM is only an interface layer

2. **LLM output has NO authority**
   - LLM output does not affect decisions
   - LLM output does not override gates
   - LLM output is advisory only

3. **LLM cannot bypass system boundaries**
   - LLM cannot call Kernel
   - LLM cannot bypass Runtime
   - LLM cannot override GateCore

4. **All LLM calls are traceable**
   - Every call has trace_id
   - Every call is logged
   - Every call is auditable

5. **LLM failure does not break system**
   - System continues without LLM
   - System has fallback mechanisms
   - System logs LLM errors

---

## 📋 Audit Checklist

To verify LLM Interface compliance:

### Allowed Capabilities
- [ ] LLM only performs annotation, query plan, labeling, rendering
- [ ] LLM output is advisory only
- [ ] LLM output does not affect system state

### Forbidden Capabilities
- [ ] LLM does not compute energy
- [ ] LLM does not call Kernel
- [ ] LLM does not evaluate GateCore
- [ ] LLM does not manage trajectory
- [ ] LLM does not modify state
- [ ] LLM does not trigger action
- [ ] LLM does not write memory
- [ ] LLM does not bypass Runtime
- [ ] LLM does not make decisions

### Invocation Rules
- [ ] LLM only called from CLI, WM Controller, Output Module
- [ ] LLM not called from Kernel, GateCore, Memory, etc.

### Data Access
- [ ] LLM has read-only access
- [ ] Data sent to LLM is sanitized
- [ ] Data sent to LLM includes trace_id

### Traceability
- [ ] All LLM calls are logged
- [ ] All LLM calls have trace_id
- [ ] All LLM calls are auditable

### Security
- [ ] LLM output cannot trigger action
- [ ] LLM output is validated
- [ ] LLM output has no authority
- [ ] LLM failure does not break system

---

## 📋 Summary (LOCKED INTENT)

**LLM is:**
- ✅ Interface tool (translator, annotator, UI layer)
- ✅ Advisory only (no authority)
- ✅ Traceable (all calls logged)
- ✅ Optional (system works without LLM)

**LLM is NOT:**
- ❌ Intelligence core (intelligence is in Kernel/GateCore)
- ❌ Decision system (decisions are in GateCore)
- ❌ Physics engine (physics is in Kernel)
- ❌ Authority (LLM output has no authority)

**This boundary is intentional and must not be expanded.**

**If LLM is removed, the system must continue to function.**

---

## ⚠️ Change Control

**This specification is LOCKED.** Changes require:
1. Architecture approval
2. Safety approval
3. Security approval
4. Version bump
5. Impact analysis (all modules)

**Authority:** Core Team  
**Review Cycle:** Quarterly (or on boundary violation)

**Violation Consequence:**
- Architecture violation
- System redesign required
- Cannot be patched

---

## 🎯 Final Declaration (LOCK)

> **LLM is an interface tool, not an intelligence authority.  
> All truth, decision, and causality remain inside Cogman's deterministic core.  
> This boundary is intentional and must not be expanded.**

**Status:** 🔒 LOCKED  
**Purpose:** Prevent LLM from becoming system authority  
**Authority:** Core Team  
**Enforcement:** Code review + runtime checks + automated tests + audit tools

