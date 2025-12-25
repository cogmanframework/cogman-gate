# Gate Policy Integration Guide

**Version:** v1.0-PROD-LOCKED

---

## Overview

This guide explains how to integrate `GATE_POLICY.yaml` with the kernel and runtime systems.

---

## File Structure

```
config/
└── gate_profiles.yaml          # GATE_POLICY.yaml (LOCKED)

kernel/
├── include/cogman_kernel/
│   └── gate_policy.hpp         # C++ Policy Loader
├── src/
│   └── gate_policy.cpp         # Implementation
└── examples/
    └── example_policy_loader.cpp

config/
└── gate_policy_loader.py       # Python Policy Loader
```

---

## C++ Integration

### Basic Usage

```cpp
#include "cogman_kernel/gate_policy.hpp"
#include "cogman_kernel/core9_gate.hpp"

// Load policy
auto policy = GatePolicyLoader::load_from_file("config/gate_profiles.yaml");

if (!policy) {
    // Handle error
    return;
}

// Get context-specific bands
DecisionBands bands = policy->to_decision_bands("robot_control");

// Create gate with policy bands
Core9DecisionGate gate(bands);

// Use gate
DecisionInput input;
input.metrics.E_mu = 50.0;
input.metrics.H = 0.5;
input.metrics.D = 0.25;
input.metrics.S = 1.0;
input.context = "robot_control";

DecisionResult result = gate.evaluate(input);
```

### Integration with Runtime

```cpp
class RuntimeGateManager {
    std::unique_ptr<GatePolicy> policy_;
    std::map<std::string, std::unique_ptr<Core9DecisionGate>> gates_;
    
public:
    bool initialize(const std::string& policy_path) {
        policy_ = GatePolicyLoader::load_from_file(policy_path);
        if (!policy_) return false;
        
        // Pre-create gates for all contexts
        for (const auto& [name, profile] : policy_->contexts) {
            DecisionBands bands = policy_->to_decision_bands(name);
            gates_[name] = std::make_unique<Core9DecisionGate>(bands);
        }
        
        return true;
    }
    
    DecisionResult evaluate(const std::string& context, const DecisionInput& input) {
        auto it = gates_.find(context);
        if (it != gates_.end()) {
            return it->second->evaluate(input);
        }
        // Fallback to default
        return DecisionResult();
    }
};
```

---

## Python Integration

### Basic Usage

```python
from config.gate_policy_loader import GatePolicyLoader, create_decision_bands_from_profile

# Load policy
policy = GatePolicyLoader.load_from_file("config/gate_profiles.yaml")

if policy:
    # Get context profile
    profile = policy.get_context("robot_control")
    
    if profile:
        # Convert to bands (for C++ bridge)
        bands = create_decision_bands_from_profile(profile)
        
        # Use with kernel bridge
        from bridge import KernelBridge
        bridge = KernelBridge()
        
        # Evaluate decision
        result = bridge.evaluate_decision(context="robot_control", metrics={...})
```

### Integration with Runtime

```python
class RuntimeGateManager:
    def __init__(self, policy_path: str):
        self.policy = GatePolicyLoader.load_from_file(policy_path)
        self.gates = {}
        
        if self.policy:
            # Pre-create gates for all contexts
            for name, profile in self.policy.contexts.items():
                bands = create_decision_bands_from_profile(profile)
                # Create gate (via bridge)
                self.gates[name] = self._create_gate(bands)
    
    def evaluate(self, context: str, metrics: dict) -> dict:
        if context in self.gates:
            return self.gates[context].evaluate(metrics)
        return {"verdict": "BLOCK", "reason": "Unknown context"}
```

---

## YAML Library Dependency

### Current Status

The C++ implementation currently uses a **placeholder parser** that hardcodes the known contexts. For production use, you need a proper YAML library.

### Recommended: yaml-cpp

**Installation:**

```bash
# Using vcpkg
vcpkg install yaml-cpp

# Or build from source
git clone https://github.com/jbeder/yaml-cpp.git
cd yaml-cpp
mkdir build && cd build
cmake .. -DYAML_BUILD_SHARED_LIBS=ON
make install
```

**Update CMakeLists.txt:**

```cmake
find_package(yaml-cpp REQUIRED)
target_link_libraries(cogman_kernel yaml-cpp)
```

**Update gate_policy.cpp:**

```cpp
#include <yaml-cpp/yaml.h>

bool GatePolicyLoader::parse_yaml(const std::string& yaml_content, GatePolicy& policy) {
    try {
        YAML::Node root = YAML::Load(yaml_content);
        
        // Parse metadata
        if (root["meta"]) {
            auto meta = root["meta"];
            policy.meta.policy_name = meta["policy_name"].as<std::string>();
            policy.meta.version = meta["version"].as<std::string>();
            // ... etc
        }
        
        // Parse contexts
        if (root["contexts"]) {
            for (const auto& context_node : root["contexts"]) {
                std::string name = context_node.first.as<std::string>();
                auto context_data = context_node.second;
                
                ContextProfile profile;
                profile.name = name;
                // ... parse limits, etc.
                
                policy.contexts[name] = profile;
            }
        }
        
        return true;
    } catch (const std::exception& e) {
        return false;
    }
}
```

---

## Policy Validation

### C++

```cpp
auto policy = GatePolicyLoader::load_from_file("config/gate_profiles.yaml");
if (policy && GatePolicyLoader::validate_policy(*policy)) {
    // Policy is valid
} else {
    // Policy is invalid
}
```

### Python

```python
policy = GatePolicyLoader.load_from_file("config/gate_profiles.yaml")
if policy and policy.validate():
    # Policy is valid
else:
    # Policy is invalid
```

---

## Context Switching

```cpp
// Switch context at runtime
DecisionBands robot_bands = policy->to_decision_bands("robot_control");
DecisionBands chat_bands = policy->to_decision_bands("chat");

Core9DecisionGate robot_gate(robot_bands);
Core9DecisionGate chat_gate(chat_bands);

// Use appropriate gate based on current context
std::string current_context = get_current_context();
DecisionResult result = (current_context == "robot_control") 
    ? robot_gate.evaluate(input)
    : chat_gate.evaluate(input);
```

---

## Policy Versioning

The policy includes version information:

```yaml
meta:
  version: v1.0
  status: LOCKED
```

This version is included in every decision result:

```cpp
DecisionResult result = gate.evaluate(input);
// result.protocol = "CORE9_v1.0"
```

---

## Safety & Compliance

### Policy Lock

- Policy is **LOCKED** (v1.0-PROD-LOCKED)
- Changes require formal review
- Version is tracked in decisions

### Audit Trail

Every decision includes:
- Policy version
- Context
- Metrics used
- Verdict and reasons

---

## Next Steps

1. **Integrate yaml-cpp** for full YAML parsing
2. **Add policy caching** for performance
3. **Add policy hot-reload** (if needed)
4. **Add policy validation tests**
5. **Integrate with runtime** gate manager

---

## Reference

- **Policy File:** `config/gate_profiles.yaml`
- **C++ Loader:** `kernel/include/cogman_kernel/gate_policy.hpp`
- **Python Loader:** `config/gate_policy_loader.py`
- **CORE-9 Spec:** `kernel/CORE9_SPEC_COMPLIANCE.md`

