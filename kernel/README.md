# Cogman Kernel

**Version:** v2.0-LOCKED  
**Status:** LOCKED - Core formulas and types must not be modified without review

---

## Overview

Cogman Kernel is the C++ physics core of Cogman Gate. It implements the 9 canonical core formulas (CORE-1 to CORE-9) that form the foundation of the system.

---

## Quick Start

### Build

```bash
cd kernel
mkdir build
cd build
cmake ..
make
```

### Run Examples

```bash
./example_basic
./example_decision_gate
```

### Run Tests

```bash
./test_core_formulas
./test_energy_bounds
./test_determinism
```

---

## Core Formulas

| ID | Formula | Description |
|----|---------|-------------|
| **CORE-1** | ΔEΨ | Energy of Perception |
| **CORE-2** | E_reflex | Reflex Energy |
| **CORE-3** | ΔEΨ_theta | Directional Reflex Energy |
| **CORE-4** | E_mind | Cognitive Energy |
| **CORE-5** | E_coherence | Coherence Energy |
| **CORE-6** | E_neural | Neuro-Energetic Sum |
| **CORE-7** | E_bind | Binding Energy |
| **CORE-8** | E_mem | Memory Encoding Energy |
| **CORE-9** | G_decision | Decision Gate Verdict |

---

## Usage

### Basic Example

```cpp
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"

using namespace cogman_kernel;

// Create state
EPS8State state;
state.I = 0.8;
state.P = 0.6;
state.S = 0.7;
state.H = 0.3;
state.A = 0.5;
state.S_a = 0.6;

// Compute energy
double delta_E_psi = energy_of_perception(state.I, state.P, state.S_a, state.H, true);
```

### Complete Energy Projection

```cpp
EnergyState energy = compute_energy_projection(
    state,
    neural,
    theta_phase,
    E_pred,
    decision_params
);
```

### Cognitive Decision Gate

```cpp
CognitiveDecisionGate gate("OWNER_STANDARD_V1");
Snapshot snapshot = {...};
DecisionResult result = gate.evaluate_snapshot(snapshot);
```

---

## Documentation

- **Usage Guide:** `USAGE.md` - Complete usage guide with examples
- **Build Instructions:** `BUILD.md` - Build instructions
- **Examples:** `examples/` - Example code
- **Tests:** `tests/` - Test suite

---

## Structure

```
kernel/
├── include/cogman_kernel/  # Public headers
│   ├── core_formulas.hpp  # CORE-1 to CORE-9 declarations
│   ├── eps8.hpp           # EPS-8 state definition
│   ├── types.hpp           # Core types
│   ├── kernel_api.hpp      # C ABI interface
│   └── version.hpp         # Version information
├── src/                    # Implementation
│   ├── core_formulas.cpp   # CORE-1 to CORE-8 implementation
│   ├── energy_projection.cpp
│   ├── gate_core.cpp       # CORE-9 + Cognitive Decision Gate
│   ├── kernel_api.cpp      # C ABI implementation
│   └── utils.cpp
├── tests/                   # Test suite
├── examples/                # Usage examples
└── CMakeLists.txt
```

---

## Reference

- **Core Formulas:** `docs/COGMAN_CORE_KERNEL.md`
- **Formula Registry:** `docs/CORE_FORMULA_REGISTRY.md`
- **BASE Specifications:** `docs/BASE-*.md`

---

## Status

**Development Status:** LOCKED  
**Lock Status:** Core formulas and types are LOCKED

