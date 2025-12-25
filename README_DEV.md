# Cogman Gate - Developer Guide

**Version:** v2.0-LOCKED  
**Status:** Active Development  
**Target Audience:** Developers, Contributors, Maintainers

---

## 📋 Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Build System](#build-system)
4. [Testing](#testing)
5. [Code Style](#code-style)
6. [Architecture Overview](#architecture-overview)
7. [Development Workflow](#development-workflow)
8. [Debugging](#debugging)
9. [Contributing](#contributing)
10. [API Documentation](#api-documentation)

---

## 🚀 Development Setup

### Prerequisites

#### Required
- **C++17** compiler (g++ 7+, clang++ 8+, MSVC 2017+)
- **CMake** 3.10 or higher
- **Python** 3.8 or higher
- **Git** 2.0+

#### Optional (for full development)
- **pytest** 7.0+ (for Python tests)
- **pytest-cov** 4.0+ (for coverage)
- **PyYAML** 6.0+ (for config loading)
- **numpy** 1.20+ (for numerical operations)
- **tabulate** 0.9+ (for CLI table formatting)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd cogman_enegetic_engine

# Install Python dependencies
pip install -r requirements.txt

# Build C++ kernel
cd kernel
mkdir build && cd build
cmake ..
make

# Verify build
./test_core_formulas
./test_input_validation
```

### Environment Variables

```bash
# Optional: Set library path for Python bridge
export COGMAN_KERNEL_LIB_PATH=/path/to/libcogman_kernel.so

# Optional: Set Python path
export PYTHONPATH=$PWD:$PYTHONPATH
```

---

## 📁 Project Structure

```
cogman_gate/
├── kernel/                    # 🦀 C++ Core (IP principal)
│   ├── include/cogman_kernel/
│   │   ├── types.hpp         # Core types (DecisionVerdict, NeuralComponents)
│   │   ├── eps8.hpp          # EPS-8 state definition
│   │   ├── core_formulas.hpp # CORE-1 to CORE-9 declarations
│   │   ├── core9_gate.hpp    # CORE-9 Decision Gate
│   │   ├── kernel_api.hpp    # C ABI interface
│   │   └── errors.hpp        # Error handling
│   ├── src/
│   │   ├── core_formulas.cpp # CORE-1 to CORE-9 implementations
│   │   ├── core9_gate.cpp    # CORE-9 implementation
│   │   ├── energy_projection.cpp
│   │   ├── gate_core.cpp
│   │   ├── kernel_api.cpp    # C API implementation
│   │   ├── errors.cpp
│   │   └── utils.cpp
│   ├── tests/
│   │   ├── test_core_formulas.cpp
│   │   ├── test_input_validation.cpp
│   │   └── test_energy_bounds.cpp
│   ├── examples/
│   │   ├── example_basic.cpp
│   │   ├── example_core9.cpp
│   │   └── example_error_handling.cpp
│   └── CMakeLists.txt
│
├── bridge/                    # 🌉 Python ↔ C++ Bridge
│   ├── kernel_bridge.py      # ctypes wrapper
│   ├── data_marshalling.py   # Data conversion
│   └── error_map.py          # Error code mapping
│
├── runtime/                   # 🕰️ Runtime Loop
│   ├── main_loop.py          # 9-phase execution loop
│   ├── wm_controller.py      # Working Memory Controller
│   ├── post_processor.py     # PHASE 9 post-processing
│   ├── error_handler.py      # Error handling
│   └── trajectory_builder.py # Trajectory construction
│
├── perception/                # 🌊 Pre-Kernel Layer
│   ├── decoder.py            # Packet decoding
│   ├── energy_estimator.py   # IPSH estimation
│   └── phrase_extractor.py  # Text → PEU
│
├── gate/                      # 🚧 Decision Gate
│   ├── gate_policy.py        # Policy loader
│   ├── decision_gate.py       # Decision logic
│   └── gate_trace.py         # Decision tracing
│
├── memory/                    # 🧠 Memory Fields
│   ├── episodic_field.py
│   ├── semantic_field.py
│   ├── procedural_field.py
│   └── identity_field.py
│
├── reasoning/                 # 🧩 Reasoning Module
│   ├── causal_graph.py
│   ├── planner.py
│   └── simulator.py
│
├── action/                    # 🤖 Action Module
│   ├── text_output.py
│   ├── motor_output.py
│   └── agent_controller.py
│
├── llm/                       # 🗣️ LLM Interface
│   ├── annotation.py          # LLM annotation
│   ├── prompt_templates.py
│   └── response_formatter.py
│
├── tests/                     # 🧪 Test Suite
│   ├── core/                  # Core formula tests
│   ├── runtime/               # Runtime tests
│   ├── integration/          # Integration tests
│   ├── safety/               # Safety tests
│   └── llm/                   # LLM tests
│
├── docs/                      # 📘 Documentation
│   ├── COGMAN_CORE_KERNEL.md
│   ├── RUNTIME_LOOP_SPEC.md
│   ├── GATECORE_SPEC.md
│   └── ...
│
└── tools/                     # 🔧 Development Tools
    ├── test_llm_integration.py
    └── log_metrics_tool.py
```

---

## 🔨 Build System

### C++ Kernel Build

```bash
cd kernel
mkdir build && cd build

# Configure
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(nproc)

# Run tests
ctest -V

# Install (optional)
sudo make install
```

### Build Options

```bash
# Debug build
cmake .. -DCMAKE_BUILD_TYPE=Debug

# With tests
cmake .. -DBUILD_TESTS=ON

# With examples
cmake .. -DBUILD_EXAMPLES=ON

# Static library only
cmake .. -DBUILD_SHARED_LIBS=OFF
```

### Python Package

```bash
# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH
```

---

## 🧪 Testing

### C++ Tests

```bash
cd kernel/build

# Run all tests
ctest -V

# Run specific test
./test_core_formulas
./test_input_validation
```

### Python Tests

```bash
# Run all tests
python3 tests/run_tests.py

# Run specific test module
python3 -m unittest tests.runtime.test_runtime_loop
python3 -m unittest tests.llm.test_llm_integration

# Run with coverage
python3 -m pytest tests/ --cov=runtime --cov=gate --cov=memory
```

### Test Categories

- **Core Tests:** `tests/core/` - Formula tests (CORE-1 to CORE-9)
- **Runtime Tests:** `tests/runtime/` - Runtime Loop, WM Controller
- **Integration Tests:** `tests/integration/` - End-to-end tests
- **Safety Tests:** `tests/safety/` - Fail-closed behavior
- **LLM Tests:** `tests/llm/` - LLM integration

### Test Utilities

```python
from tests.test_utils import (
    create_test_eps8_state,
    create_test_trajectory,
    create_test_decision
)
```

---

## 📝 Code Style

### C++ Style

- **Standard:** C++17
- **Naming:** `snake_case` for functions, `PascalCase` for classes
- **Indentation:** 4 spaces
- **Namespace:** `cogman_kernel`

```cpp
namespace cogman_kernel {

class MyClass {
public:
    double compute_energy(double I, double P);
private:
    double threshold_;
};

} // namespace cogman_kernel
```

### Python Style

- **Standard:** PEP 8
- **Naming:** `snake_case` for functions/classes
- **Type Hints:** Required for public APIs
- **Docstrings:** Google style

```python
def compute_energy(I: float, P: float) -> float:
    """
    Compute energy from intensity and polarity.
    
    Args:
        I: Intensity [0, ∞)
        P: Polarity [0, 1]
    
    Returns:
        Computed energy value
    """
    return I * P
```

---

## 🏗️ Architecture Overview

### Core Principles

1. **Kernel is Pure Physics**
   - No semantic awareness
   - Deterministic computation
   - No side effects

2. **Runtime Loop is Orchestrator**
   - Calls modules in order
   - No decision-making
   - No interpretation

3. **GateCore is Safety Layer**
   - Fail-closed behavior
   - Deterministic decisions
   - No learning

4. **Memory is Passive**
   - No authority
   - Read-only queries
   - No trajectory modification

### Data Flow

```
External Input
    ↓
PHASE 1: Input Intake
    ↓
PHASE 2: Sensory Adaptation
    ↓
PHASE 3: Perception Boundary → EPS-8 State
    ↓
PHASE 4: Trajectory Admission (GateCore)
    ↓
PHASE 5: Working Memory Control
    ↓
PHASE 6: Reasoning
    ↓
PHASE 7: Decision
    ↓
PHASE 8: Action / Output
    ↓
PHASE 9: Post-Processing
    ↓
Output
```

### Module Boundaries

- **Kernel:** C++ only, no Python dependencies
- **Bridge:** Python ↔ C++ interface
- **Runtime:** Python orchestration
- **Perception:** Pre-kernel, no Kernel calls
- **Gate:** Decision logic, no Kernel calls
- **Memory:** Passive storage, no authority
- **Reasoning:** Structure only, no decisions
- **LLM:** Post-decision only, no authority

---

## 🔄 Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Run tests
python3 tests/run_tests.py
cd kernel/build && ctest

# Commit
git add .
git commit -m "feat: Add new feature"

# Push
git push origin feature/my-feature
```

### 2. Bug Fix

```bash
# Create bugfix branch
git checkout -b bugfix/fix-issue-123

# Fix bug
# ... fix code ...

# Add test for bug
# ... add test ...

# Run tests
python3 tests/run_tests.py

# Commit
git commit -m "fix: Resolve issue #123"
```

### 3. Testing

```bash
# Run all tests
python3 tests/run_tests.py
cd kernel/build && ctest

# Run specific test
python3 -m unittest tests.runtime.test_runtime_loop

# Check coverage
python3 -m pytest tests/ --cov=runtime --cov-report=html
```

### 4. Documentation

```bash
# Update README
# Update docstrings
# Update specs in docs/
```

---

## 🐛 Debugging

### C++ Debugging

```bash
# Build with debug symbols
cd kernel/build
cmake .. -DCMAKE_BUILD_TYPE=Debug
make

# Run with gdb
gdb ./test_core_formulas
(gdb) break energy_of_perception
(gdb) run
(gdb) print I
(gdb) print P
```

### Python Debugging

```python
# Use pdb
import pdb; pdb.set_trace()

# Or use IDE debugger
# Set breakpoints in IDE
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Error Handling

```python
from runtime.error_handler import RuntimeErrorHandler, ErrorSeverity

error_handler = RuntimeErrorHandler()
try:
    # Code that may fail
    pass
except Exception as e:
    error_handler.handle_error(
        phase="PHASE_4",
        error=e,
        severity=ErrorSeverity.HIGH
    )
```

---

## 🤝 Contributing

### Contribution Guidelines

1. **Follow Architecture**
   - Respect module boundaries
   - Follow specifications
   - Maintain determinism

2. **Write Tests**
   - Unit tests for new code
   - Integration tests for flows
   - Safety tests for gates

3. **Update Documentation**
   - Update README if needed
   - Add docstrings
   - Update specs if contracts change

4. **Code Review**
   - All PRs require review
   - Tests must pass
   - Documentation must be updated

### Commit Messages

Follow conventional commits:

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
chore: Maintenance tasks
```

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit PR
7. Address review comments
8. Merge after approval

---

## 📚 API Documentation

### C++ Kernel API

```cpp
// Energy projection
EnergyState compute_energy_projection(
    const EPS8State& state,
    const NeuralComponents& neural,
    double theta_phase,
    double E_pred,
    const DecisionParams& decision_params
);

// CORE-9 Decision Gate
DecisionResult core9_evaluate(
    const DecisionInput& input
);
```

### Python Bridge API

```python
from bridge import KernelBridge

bridge = KernelBridge()

# Energy projection
energy = bridge.energy_projection(
    eps8_state={'I': 0.8, 'P': 0.6, ...},
    neural_components={'dopamine': 0.4, ...},
    theta_phase=1.5,
    E_pred=0.5,
    decision_params={...}
)

# CORE-9 Decision Gate
result = bridge.core9_evaluate(
    metrics={'E_mu': 50.0, 'H': 0.5, ...},
    bands={...},
    context="robot_control"
)
```

### Runtime Loop API

```python
from runtime import RuntimeLoop, Phase

runtime = RuntimeLoop(
    gatecore=gatecore,
    wm_controller=wm_controller,
    ...
)

runtime.run()  # Start execution loop
runtime.stop()  # Stop execution loop
```

---

## 🔍 Key Specifications

### Core Specifications

- **COGMAN_CORE_KERNEL.md:** 9 LOCKED core formulas
- **RUNTIME_LOOP_SPEC.md:** Runtime Loop execution
- **GATECORE_SPEC.md:** Decision Gate specification
- **KERNEL_BOUNDARY_SPEC.md:** Kernel isolation rules
- **RUNTIME_CONTRACT_SPEC.md:** Runtime contracts
- **LLM_INTERFACE_SPEC.md:** LLM boundary rules

### Module Specifications

- **WM_CONTROLLER_SPEC.md:** WM Controller responsibilities
- **PERCEPTION_BOUNDARY_SPEC.md:** Perception layer rules
- **REASONING_MODULE_SPEC.md:** Reasoning module rules
- **MEMORY_FIELD_SPEC.md:** Memory field rules

---

## 🛠️ Development Tools

### CLI Tools

```bash
# Test LLM integration
python3 tools/test_llm_integration.py

# View logs and metrics
python3 tools/log_metrics_tool.py log list
python3 tools/log_metrics_tool.py metrics stats
```

### Inspection Tools

```bash
# Inspect trajectory
python3 tools/trajectory_inspector.py <trace_id>

# Replay trajectory
python3 tools/replay_engine.py <trace_id>
```

---

## 📊 Code Metrics

### Test Coverage Goals

- **Core Formulas:** 100% coverage
- **Runtime Modules:** 90%+ coverage
- **Integration:** Critical paths 100%
- **Safety:** 100% coverage

### Code Quality

- **Linting:** Follow C++ and Python style guides
- **Type Safety:** Use type hints in Python
- **Error Handling:** All errors must be handled
- **Documentation:** All public APIs documented

---

## 🚨 Common Issues

### Issue: Library Not Found

```bash
# Set library path
export COGMAN_KERNEL_LIB_PATH=/path/to/libcogman_kernel.so

# Or specify in code
from bridge import KernelBridge
bridge = KernelBridge(library_path="/path/to/lib")
```

### Issue: Import Errors

```bash
# Add to PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH

# Or use absolute imports
import sys
sys.path.insert(0, '/path/to/project')
```

### Issue: Build Failures

```bash
# Clean build
cd kernel/build
rm -rf *
cmake ..
make
```

---

## 📖 Additional Resources

- **Architecture:** `docs/ARCHITECTURE.md`
- **Core Formulas:** `docs/COGMAN_CORE_KERNEL.md`
- **Testing Guide:** `tests/README_TESTING.md`
- **Error Handling:** `tests/ERROR_HANDLING_GUIDE.md`
- **LLM Testing:** `docs/LLM_TESTING_GUIDE.md`

---

## 📞 Support

- **Issues:** Open GitHub issue
- **Discussions:** Use GitHub Discussions
- **Documentation:** Check `docs/` directory

---

## 📝 License

See `LICENSE` file for details.

---

## ⚠️ Important Notes

1. **Core Formulas are LOCKED** - Do not modify CORE-1 to CORE-9
2. **Respect Boundaries** - Follow module boundary specifications
3. **Maintain Determinism** - All computations must be deterministic
4. **Test Everything** - Write tests for all new code
5. **Document Changes** - Update documentation with code changes

---

**Last Updated:** 2024-12  
**Maintainer:** Cogman Development Team

