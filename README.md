# Cogman Gate

## Energetic Decision & Control Infrastructure

**Version:** v2.0-LOCKED  
**Status:** Production-Ready · Deterministic · Non-LLM Core  
**Last Updated:** 2024-12-24  

---

## What This Is (30 seconds)

Cogman Gate is an **AI Runtime Infrastructure that enforces control**

```
AI Model's Request
        ↓
    [GateCore]
        ↓
    ✅ ALLOW / ⚠️ REVIEW / ❌ BLOCK
        ↓
    Runtime Verdict (cannot be overridden)
```

**NOT an AI model** — it's a **control layer that can be enforced**

---

## Why This Exists

### Problems with Current AI Systems

| Problem | Result |
|---------|--------|
| LLM makes decisions | Cannot debug why it did that |
| Boundary is soft | Model can ignore it |
| Not traceable | Audit trail is lost |
| Not reproducible | Same input gives different results |

### Cogman Solves This

✅ Physics-based decision (not neural)  
✅ Gated execution (every action must pass through)  
✅ Fully traceable (can be traced back)  
✅ Deterministic (same input = same output)  

---

## Core Principle: The Gate

```
Input Signal (ε, P, S, H, context)
        ↓
  [Kernel Analysis]
   (9 Canonical Formulas - LOCKED)
        ↓
  [GateCore Decision]
   Energy × Stability × Context Policy
        ↓
  ✅ ALLOW  |  ⚠️ REVIEW  |  ❌ BLOCK
        ↓
  [Runtime Enforcement]
   (no override)
```

**Principle:** Model decides **what's possible** | Runtime decides **what's allowed**

---

## What You Actually Get

### 1️⃣ Locked Physics Kernel (C++)

```cpp
struct EnergyState {
  float I;      // Intensity [0, 1]
  float P;      // Polarity [0, 1]
  float S;      // Stability [0, 1]
  float H;      // Entropy [0, 1]
  // ...
};

// 9 Canonical Formulas
dE = I × P × S × (1 - H)
// + 8 others (LOCKED)
```

**What you get:**
- ✅ 9 verified formulas (unchanged)
- ✅ Deterministic output every nanosecond
- ✅ Reproducible both offline/online
- ✅ Zero hidden heuristics

**What you don't get:**
- ❌ Cannot change formulas
- ❌ Cannot add heuristics
- ❌ Cannot tune parameters yourself

---

### 2️⃣ Decision Gate (CORE-9)

```
┌─ Robot Context ─────┐
│ energy: 52          │
│ stability: 0.7      │
│ entropy: 0.2        │
│ urgency: NORMAL     │
└─────────────────────┘
        ↓
    [GateCore Policy]
    if S < threshold: BLOCK
    elif H > max_entropy: REVIEW
    else: ALLOW (with constraints)
        ↓
┌─ Verdict ───────────┐
│ decision: ALLOW     │
│ reason: #GATE_003   │
│ trace_id: xyz...    │
│ expires_at: T+5ms   │
└─────────────────────┘
```

**What you get:**
- ✅ Deterministic verdict (not probabilistic)
- ✅ Context-aware (robot/finance/chat policies)
- ✅ No neural network (not a black box)
- ✅ Explainable (every decision has a reason code)

**Verdict ≠ Model output:**
```python
# Model says: "Let's try this action"
# Runtime says: "You can't. Gate policy #007 blocks it."
# Model learns: "That boundary is hard."
```

---

### 3️⃣ Python Bridge (Safe Boundary)

```python
from cogman.runtime import GateCore

gate = GateCore(context="robot_control")

# ✅ Allowed
verdict = gate.evaluate(
  energy=52.0,
  stability=0.75,
  entropy=0.2,
  action="move_forward"
)
print(verdict)
# Output: Verdict(decision=ALLOW, reason='#GATE_001', 
#                  expires_at=1734988237.5)

# ❌ Cannot do this
# gate.formulas.I = lambda x: 0  # Would fail at binary level

# ❌ Cannot bypass
# gate.override_decision("ALLOW")  # Runtime won't accept it
```

**Boundary Enforcement:**
- ✅ Python calls kernel ✓
- ❌ Python modifies formulas ✗
- ❌ Python overrides gate ✗
- ❌ Python disables trace ✗

---

### 4️⃣ CLI for Control & Audit

```bash
# Inspect current energy state
$ cogman gate status --context robot_control
energy: 52.3
stability: 0.74
entropy: 0.19
phase: 1.23 rad
coherence: 0.92

# Test decision for hypothetical state
$ cogman gate test \
  --context robot_control \
  --I 0.7 --S 0.8 --H 0.1 \
  --action move_forward
Decision: ALLOW
Reason: #GATE_002
Margin: 0.15 (safety buffer)

# Audit: replay trajectory
$ cogman trace replay trajectory_20241224_154530.json
[...]
decision #14: ALLOW  (t=1234.567)
decision #15: REVIEW (t=1235.123)  ← Policy change triggered
decision #16: BLOCK  (t=1235.456)

# Full audit
$ cogman audit verify runtime_2024-12-24.log
✓ All 1,247 decisions checksum: 0xABCD1234
✓ Zero overrides detected
✓ Zero formula mutations
✓ Trace continuity: OK
```

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              APPLICATION LAYER                   │
│         (Your AI System / Model)                │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   Python Bridge      │
          │  (cogman.runtime)    │
          └──────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Kernel │  │ GateCore  │ Tracer │
    │ (C++)  │  │ (C++)  │  │ (C++) │
    └────┬───┘  └────┬───┘  └────┬───┘
         │           │           │
         └───────┬───┴───┬───────┘
                 │       │
         ┌───────▼───────▼────────┐
         │   Runtime Enforcement  │
         │   (No Escape Hatch)    │
         └────────────────────────┘
                     │
         ┌───────────▼──────────┐
         │   Audit Log / Trace  │
         │   (Immutable)        │
         └──────────────────────┘
```

**Guarantee:** Every action must pass through GateCore before execution

---

## What This Is NOT

| ❌ NOT | Reason |
|-------|--------|
| AGI | It's a runtime control, not intelligence |
| Human-like thinking | It's physics-based formulas, not cognition |
| Human judgment replacement | Humans still need to review audit logs |
| Medical/Psych system | Used for control, not diagnosis |
| General-purpose LLM | It's infrastructure, not a model |

---

## IP & Boundaries (LOCKED)

### What's Locked 🔒

```
┌─────────────────────────────────────┐
│ LOCKED COMPONENTS                   │
├─────────────────────────────────────┤
│ • 9 Canonical Formulas              │
│ • GateCore Decision Logic           │
│ • Kernel Physics (C++)              │
│ • Gate Policy Enforcement Algorithm │
└─────────────────────────────────────┘
```

**Distribution Method:**
- ✅ Binary-first (compiled kernel only)
- ✅ Specs open for audit
- ✅ Runtime behavior is reproducible
- ❌ Source formulas not exposed

---

### What's Open

```
┌─────────────────────────────────────┐
│ OPEN / AUDITABLE COMPONENTS         │
├─────────────────────────────────────┤
│ • CLI Tools                         │
│ • Python Bridge (non-core)          │
│ • Trace & Audit System              │
│ • Documentation (this file)         │
│ • Test Cases                        │
└─────────────────────────────────────┘
```

**Audit Policy:**
- ✅ Infra team can verify traces
- ✅ CTO can audit logs
- ✅ Security team can inspect decisions
- ❌ No team can modify formulas

---

## Quick Start

### Prerequisites
```bash
# C++ compiler (GCC 10+ or Clang 12+)
# Python 3.10+
# CMake 3.16+
```

### Installation

```bash
# Clone repository
git clone https://github.com/cogmanframework/cogman_gate.git
cd cogman_gate

# Install Python dependencies
pip install -r requirements.txt

# Build C++ kernel
cd kernel && mkdir build && cd build
cmake .. && make
cd ../..

# Install runtime (sets up binary)
chmod +x install.sh
./install.sh

# Set environment
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.so"  # Linux
# or
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.dylib"  # macOS
```

**Note:** Cogman Gate is distributed as **infrastructure** (GitHub + Binary), not via PyPI. See [`INSTALL.md`](INSTALL.md) for details.

### First Run

```python
from bridge import KernelBridge

# Initialize bridge
bridge = KernelBridge()

# Evaluate decision via CORE-9
result = bridge.core9_evaluate(
    metrics={'E_mu': 50.0, 'H': 0.2, 'D': 0.1, 'S': 1.0},
    bands={'D_max': 0.35, 'H_max': 0.62, ...},
    context="robot_control"
)

print(f"Decision: {result['verdict']}")        # Output: ALLOW
print(f"Reason: {result['reasons']}")           # Output: ['All metrics within safety bounds']
print(f"Trace ID: {result.get('trace_id')}")   # Output: xyz...
```

### CLI Inspection

```bash
# Check current status
python -m cog_cli.main gate test --context robot_control --E_mu 50 --H 0.2

# Test decision
python -m cog_cli.main gate test \
  --context robot_control \
  --E_mu 50.0 --H 0.2 --D 0.1 --S 1.0

# View logs
python3 tools/log_metrics_tool.py log list --limit 10
```

---

## Core Specifications (Complete Reference)

| Spec File | Purpose |
|-----------|---------|
| [`GATECORE_SPEC.md`](docs/GATECORE_SPEC.md) | Gate decision authority & verdict types |
| [`RUNTIME_CONTRACT_SPEC.md`](docs/RUNTIME_CONTRACT_SPEC.md) | What can call what, when, how |
| [`KERNEL_INVOCATION_SPEC.md`](docs/KERNEL_INVOCATION_SPEC.md) | Exactly how kernel is invoked |
| [`TRACE_LIFECYCLE_SPEC.md`](docs/TRACE_LIFECYCLE_SPEC.md) | Full traceability guarantee |
| [`MEMORY_FIELD_SPEC.md`](docs/MEMORY_FIELD_SPEC.md) | Passive memory only (no learning) |
| [`KERNEL_BOUNDARY_SPEC.md`](docs/KERNEL_BOUNDARY_SPEC.md) | Kernel isolation rules |

---

## Who This Is For

### ✅ You Should Use This If You're

- 🏢 Building **AI infrastructure** that needs hard boundaries
- 🤖 Running **robotics / automation** that can't fail silently
- 💰 Managing **financial systems** with regulatory requirements
- 🔒 Operating **safety-critical AI** (autonomous vehicles, industrial)
- 👥 Leading **infra / platform teams** that "don't want AI to break"

### ❌ You Should NOT Use This If You

- Want a general LLM chatbot → Use OpenAI API instead
- Need human-like reasoning → Use traditional ML instead
- Want to modify core logic → Not an option by design
- Expect fast feature iterations → This is locked for stability

---

## Troubleshooting & Support

### Q: "Gate rejected my decision. Why?"
**A:** Check trace:
```bash
python -m cog_cli.main trace view --trace-id <id>
# Output: Policy #GATE_004 blocks when S < 0.6 and context=robot_control
```

### Q: "Can I modify the kernel formulas?"
**A:** No. This is intentional. The locked kernel is the **trust boundary**.

### Q: "What if I disagree with a gate decision?"
**A:** 
1. Review policy: Check `config/gate_profiles.yaml`
2. Request policy change: Submit to **Policy Review Board**
3. Policy update is **audited and logged**

### Q: "How do I debug if something goes wrong?"
**A:**
```bash
# View logs
python3 tools/log_metrics_tool.py log list --limit 100

# View metrics
python3 tools/log_metrics_tool.py metrics stats

# Check kernel bridge
python -m bridge.test_basic
```

---

## Performance Characteristics

```
Operation              Latency          Notes
────────────────────────────────────────────────
gate.evaluate()        < 100 μs         Per decision
Kernel computation     < 50 μs          9 formulas, C++
Decision logging       < 10 μs          Async write
Trace checkpoint       < 1 ms           Every 1000 decisions
────────────────────────────────────────────────
```

**Throughput:**
- ✅ ~10,000 decisions/second (single thread)
- ✅ Linear scaling with CPU cores
- ✅ No GC pauses (C++ kernel)

---

## License & IP Protection

**License:** MIT (see [`LICENSE`](LICENSE) file)

```
LOCKED COMPONENTS:
  • Kernel source (C++): Core formulas locked
  • Formulas: 9 canonical (LOCKED)
  • Core logic: Deterministic by design
  
DISTRIBUTED:
  • Compiled kernel (.so / .dylib / .dll)
  • Python bindings
  • CLI tools
  • Documentation

AUDIT RIGHTS:
  • Your security team: Full audit access
  • Customers (enterprise): Upon contract
  • Open-source community: Binary signatures only
```

---

## Contact & Support

- **Engineering Issues:** [GitHub Issues](https://github.com/cogmanframework/cogman_gate/issues)
- **Security Audit:** security@example.com
- **Policy Requests:** policy-review@example.com
- **Licensing Questions:** sales@example.com

---

## Changelog

### v2.0 (Current)
- ✅ Stable kernel formulas (LOCKED)
- ✅ GateCore decision system (CORE-9)
- ✅ Full trace & audit
- ✅ Python bridge
- ✅ CLI tools

### v1.9
- ⚠️ Deprecated (use v2.0)

---

## Final Word

This system does **not decide for you**.

It decides whether your system is **allowed to act**.

That's the difference.

---

**Maintained by:** Cogman Engineering Team  
**Last Verified:** 2024-12-24  
**Status:** ✅ Production (All systems nominal)
