# Kernel Usage Guide

**Version:** v2.0-LOCKED

---

## Building the Kernel

### Prerequisites
- CMake 3.10 or higher
- C++17 compatible compiler (g++, clang++, etc.)

### Build Steps

```bash
cd kernel
mkdir build
cd build
cmake ..
make
```

This will create:
- `libcogman_kernel.a` - Static library
- Test executables in `build/` directory

---

## Basic Usage

### 1. Include Headers

```cpp
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
```

### 2. Basic Energy Computation

```cpp
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include <iostream>

using namespace cogman_kernel;

int main() {
    // Create EPS-8 state
    EPS8State state;
    state.I = 0.8;      // Intensity
    state.P = 0.6;      // Polarity
    state.S = 0.7;      // Stability
    state.H = 0.3;      // Entropy
    state.A = 0.5;      // Awareness
    state.S_a = 0.6;    // Sub-awareness
    
    // Compute CORE-1: Energy of Perception
    double delta_E_psi = energy_of_perception(
        state.I, state.P, state.S_a, state.H, true
    );
    
    std::cout << "ΔEΨ = " << delta_E_psi << std::endl;
    
    return 0;
}
```

### 3. Complete Energy Projection

```cpp
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include <iostream>

using namespace cogman_kernel;

int main() {
    // Create EPS-8 state
    EPS8State state;
    state.I = 0.8;
    state.P = 0.6;
    state.S = 0.7;
    state.H = 0.3;
    state.A = 0.5;
    state.S_a = 0.6;
    state.theta = 1.5;
    
    // Create neural components
    NeuralComponents neural;
    neural.dopamine = 0.4;
    neural.serotonin = 0.5;
    neural.oxytocin = 0.3;
    neural.adrenaline = 0.2;
    neural.cortisol = 0.1;
    
    // Decision parameters
    DecisionParams decision_params;
    decision_params.H_threshold = 0.85;
    decision_params.D_traj_threshold = 0.7;
    
    // Compute energy projection
    EnergyState energy = compute_energy_projection(
        state,
        neural,
        1.5,  // theta_phase
        0.5,  // E_pred
        decision_params
    );
    
    // Print results
    std::cout << "ΔEΨ = " << energy.delta_E_psi << std::endl;
    std::cout << "E_reflex = " << energy.E_reflex << std::endl;
    std::cout << "E_mind = " << energy.E_mind << std::endl;
    std::cout << "E_coherence = " << energy.E_coherence << std::endl;
    std::cout << "E_bind = " << energy.E_bind << std::endl;
    std::cout << "E_mem = " << energy.E_mem << std::endl;
    std::cout << "Verdict: " << decision_verdict_to_string(energy.verdict) << std::endl;
    
    return 0;
}
```

### 4. Using Cognitive Decision Gate

```cpp
#include "cogman_kernel/gate_core.cpp"  // Include implementation
#include <iostream>

using namespace cogman_kernel;

int main() {
    // Create decision gate
    CognitiveDecisionGate gate("OWNER_STANDARD_V1");
    
    // Create snapshot
    Snapshot snapshot;
    snapshot.I = 0.8;
    snapshot.P = 0.6;
    snapshot.S = 0.7;
    snapshot.H = 0.3;
    snapshot.T_psi = 0.5;        // TΨ
    snapshot.delta_E_psi = 0.4;  // ΔEΨ
    snapshot.E_total = 2.5;
    
    // Evaluate snapshot
    DecisionResult result = gate.evaluate_snapshot(snapshot);
    
    // Print decision
    std::cout << "Decision: " << decision_status_to_string(result.decision) << std::endl;
    std::cout << "Severity: " << result.severity << std::endl;
    std::cout << "Reasons:" << std::endl;
    for (const auto& reason : result.reasons) {
        std::cout << "  - " << reason << std::endl;
    }
    
    return 0;
}
```

---

## API Reference

### Core Formulas (CORE-1 to CORE-8)

```cpp
// CORE-1: Energy of Perception
double energy_of_perception(double I, double P, double S_a, double H, bool use_absolute = true);

// CORE-2: Reflex Energy
double reflex_energy(double delta_E_psi, double A);

// CORE-3: Directional Reflex Energy
double directional_reflex_energy(double delta_E_psi, double theta_phase);

// CORE-4: Cognitive Energy
double cognitive_energy(double I, double A, double H);

// CORE-5: Coherence Energy
double coherence_energy(double S, double A, double H);

// CORE-6: Neuro-Energetic Sum
double neural_energetic_sum(const NeuralComponents& neural);

// CORE-7: Binding Energy
double binding_energy(double E_mind, double E_neural, double E_coherence);

// CORE-8: Memory Encoding Energy
double memory_encoding_energy(double A, double E_bind, double E_pred);
```

### Decision Gate (CORE-9)

```cpp
// Simple decision gate
DecisionVerdict decision_gate(
    const DecisionParams& params,
    double H_current,
    double D_traj_current = 0.0
);

// Cognitive decision gate (advanced)
class CognitiveDecisionGate {
public:
    explicit CognitiveDecisionGate(const std::string& owner_profile_name = "OWNER_STANDARD_V1");
    DecisionResult evaluate_snapshot(const Snapshot& snapshot);
    EngineeringThresholds& get_thresholds();
};
```

### Energy Projection

```cpp
EnergyState compute_energy_projection(
    const EPS8State& state,
    const NeuralComponents& neural,
    double theta_phase,
    double E_pred,
    const DecisionParams& decision_params
);
```

---

## Data Structures

### EPS8State
```cpp
struct EPS8State {
    double I;      // Intensity [I >= 0]
    double P;      // Polarity [P ∈ ℝ]
    double S;      // Stability [0 <= S <= 1]
    double H;      // Entropy/Uncertainty [0 <= H <= 1]
    double F;      // External Force [F ∈ ℝ]
    double A;      // Awareness [0 <= A <= 1]
    double S_a;    // Sub-awareness [0 <= S_a <= 1]
    double theta;  // Phase angle [theta ∈ ℝ]
    
    bool validate() const;
};
```

### EnergyState
```cpp
struct EnergyState {
    double delta_E_psi;        // CORE-1
    double E_reflex;           // CORE-2
    double delta_E_psi_theta;  // CORE-3
    double E_mind;             // CORE-4
    double E_coherence;        // CORE-5
    double E_neural;           // CORE-6
    double E_bind;             // CORE-7
    double E_mem;              // CORE-8
    DecisionVerdict verdict;   // CORE-9
};
```

### DecisionParams
```cpp
struct DecisionParams {
    bool rule_fail = false;
    double E_mu_restrict_min = -∞;
    double E_mu_restrict_max = +∞;
    double H_threshold = 0.85;
    double D_traj_threshold = 0.7;
};
```

---

## Linking the Library

### CMake (Recommended)

```cmake
# In your CMakeLists.txt
add_subdirectory(kernel)
target_link_libraries(your_target cogman_kernel)
target_include_directories(your_target PRIVATE kernel/include)
```

### Manual Linking

```bash
# Compile your code
g++ -std=c++17 -Ikernel/include your_code.cpp \
    -Lkernel/build -lcogman_kernel \
    -o your_program
```

---

## Testing

Run the test suite:

```bash
cd kernel/build
./test_core_formulas
./test_energy_bounds
./test_determinism
```

---

## Notes

- All formulas are **deterministic** and **reproducible**
- Input validation is performed automatically
- All values are **engineering simulation** only
- No medical or clinical interpretation

---

## Reference

- **Core Formulas:** `include/cogman_kernel/core_formulas.hpp`
- **EPS-8 State:** `include/cogman_kernel/eps8.hpp`
- **Types:** `include/cogman_kernel/types.hpp`
- **Documentation:** `docs/COGMAN_CORE_KERNEL.md`

