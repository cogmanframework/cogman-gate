# Bridge Module

**Purpose:** C++ <-> Python bridge

---

## Overview

The bridge module provides Python bindings to the C++ kernel using ctypes. It allows Python code to call C++ kernel functions seamlessly.

---

## Features

- **Energy Projection:** Call `cogman_energy_projection()` from Python
- **Decision Gate:** Call `cogman_decision_gate()` from Python
- **CORE-9 Gate:** Call `cogman_core9_evaluate()` from Python
- **State Validation:** Validate EPS-8 states
- **Auto Library Loading:** Automatically finds and loads kernel library

---

## Usage

### Basic Setup

```python
from bridge import KernelBridge

# Initialize bridge (auto-loads library)
bridge = KernelBridge()

# Or specify library path
bridge = KernelBridge(library_path="kernel/build/libcogman_kernel.so")
```

### Energy Projection

```python
eps8_state = {
    'I': 0.8,
    'P': 0.6,
    'S': 0.7,
    'H': 0.3,
    'A': 0.5,
    'S_a': 0.6,
    'theta': 1.5,
}

neural_components = {
    'dopamine': 0.4,
    'serotonin': 0.5,
    'oxytocin': 0.3,
    'adrenaline': 0.2,
    'cortisol': 0.1,
}

decision_params = {
    'rule_fail': False,
    'H_threshold': 0.85,
    'D_traj_threshold': 0.7,
}

energy = bridge.energy_projection(
    eps8_state,
    neural_components,
    theta_phase=1.5,
    E_pred=0.5,
    decision_params=decision_params,
)

print(f"ΔEΨ = {energy['delta_E_psi']}")
print(f"Verdict: {energy['verdict']}")
```

### CORE-9 Decision Gate

```python
from config.gate_policy_loader import GatePolicyLoader
from bridge.data_marshalling import create_decision_bands_from_policy

# Load policy
policy = GatePolicyLoader.load_from_file("config/gate_profiles.yaml")
profile = policy.get_context("robot_control")
bands = create_decision_bands_from_policy(profile)

# Create metrics
metrics = {
    'E_mu': 50.0,
    'H': 0.5,
    'D': 0.25,
    'S': 1.0,
    'T': 0.5,
    'V': 4.0,
}

# Evaluate
result = bridge.core9_evaluate(
    metrics=metrics,
    bands=bands,
    context="robot_control",
    E_mu_history=[45.0, 48.0, 50.0],
)

print(f"Verdict: {result['verdict']}")
print(f"Reasons: {result['reasons']}")
```

### State Validation

```python
eps8_state = {
    'I': 0.8,
    'P': 0.6,
    'S': 0.7,
    'H': 0.3,
    'A': 0.5,
    'S_a': 0.6,
    'theta': 1.5,
}

is_valid = bridge.validate_state(eps8_state)
print(f"State valid: {is_valid}")
```

---

## Library Loading

The bridge automatically searches for the kernel library in:

1. `kernel/build/`
2. `kernel/build/lib/`
3. `/usr/local/lib/`
4. `/usr/lib/`

Library names:
- **macOS:** `libcogman_kernel.dylib` or `libcogman_kernel.a`
- **Linux:** `libcogman_kernel.so` or `libcogman_kernel.a`
- **Windows:** `cogman_kernel.dll` or `cogman_kernel.lib`

---

## Building Shared Library

To build a shared library for Python bindings:

```bash
cd kernel
mkdir build
cd build
cmake .. -DBUILD_SHARED_LIBS=ON
make
```

This creates:
- `libcogman_kernel.so` (Linux)
- `libcogman_kernel.dylib` (macOS)
- `cogman_kernel.dll` (Windows)

---

## Error Handling

```python
from bridge import KernelBridge, KernelError

try:
    bridge = KernelBridge()
    result = bridge.energy_projection(...)
except KernelError as e:
    print(f"Kernel error: {e}")
except FileNotFoundError as e:
    print(f"Library not found: {e}")
except RuntimeError as e:
    print(f"Runtime error: {e}")
```

---

## Data Marshalling

The bridge automatically handles data conversion:

- **Python dict → C struct:** Automatic conversion
- **C struct → Python dict:** Automatic conversion
- **Memory management:** Automatic cleanup

---

## Examples

See `bridge/example_usage.py` for complete examples.

---

## Reference

- **Kernel API:** `kernel/include/cogman_kernel/kernel_api.hpp`
- **C API:** `kernel/src/kernel_api.cpp`
- **Examples:** `bridge/example_usage.py`

---

## Status

**Development Status:** Ready for use  
**Library Loading:** Auto-detection supported  
**Memory Management:** Automatic cleanup

