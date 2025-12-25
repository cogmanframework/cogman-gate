/**
 * Gate Policy Loader Example
 * 
 * Demonstrates loading and using GATE_POLICY.yaml
 */

#include "cogman_kernel/gate_policy.hpp"
#include "cogman_kernel/core9_gate.hpp"
#include <iostream>
#include <iomanip>

using namespace cogman_kernel;

int main() {
    std::cout << "=== Gate Policy Loader Example ===" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    
    // Load policy from file
    std::string policy_path = "../../config/gate_profiles.yaml";
    auto policy = GatePolicyLoader::load_from_file(policy_path);
    
    if (!policy) {
        std::cerr << "Error: Failed to load policy from " << policy_path << std::endl;
        std::cerr << "Using default policy..." << std::endl;
        
        // Fallback: create policy programmatically
        policy = std::make_unique<GatePolicy>();
        // ... (would populate with defaults)
    }
    
    if (policy) {
        std::cout << "\nPolicy Metadata:" << std::endl;
        std::cout << "  Name: " << policy->meta.policy_name << std::endl;
        std::cout << "  Version: " << policy->meta.version << std::endl;
        std::cout << "  Status: " << policy->meta.status << std::endl;
        std::cout << "  Fail-Closed: " << (policy->meta.fail_closed ? "YES" : "NO") << std::endl;
        std::cout << "  Explainable: " << (policy->meta.explainable ? "YES" : "NO") << std::endl;
        std::cout << "  Deterministic: " << (policy->meta.deterministic ? "YES" : "NO") << std::endl;
        
        // List available contexts
        std::cout << "\nAvailable Contexts:" << std::endl;
        for (const auto& [name, profile] : policy->contexts) {
            std::cout << "  - " << name << ": " << profile.description << std::endl;
        }
        
        // Use robot_control context
        std::cout << "\n--- Using robot_control Context ---" << std::endl;
        DecisionBands bands = policy->to_decision_bands("robot_control");
        Core9DecisionGate gate(bands);
        
        // Create test input
        DecisionInput input;
        input.metrics.E_mu = 50.0;
        input.metrics.H = 0.5;
        input.metrics.D = 0.25;
        input.metrics.S = 1.0;
        input.metrics.T = 0.5;
        input.metrics.V = 4.0;
        input.context = "robot_control";
        
        DecisionResult result = gate.evaluate(input);
        
        std::cout << "Verdict: " << decision_verdict_to_string(result.verdict) << std::endl;
        std::cout << "Context: " << result.context << std::endl;
        std::cout << "Protocol: " << result.protocol << std::endl;
        std::cout << "\nExplainable Record:\n" << result.to_explainable_record() << std::endl;
        
        // Compare with chat context
        std::cout << "\n--- Comparing with chat Context ---" << std::endl;
        DecisionBands chat_bands = policy->to_decision_bands("chat");
        Core9DecisionGate chat_gate(chat_bands);
        
        input.context = "chat";
        DecisionResult chat_result = chat_gate.evaluate(input);
        
        std::cout << "robot_control: " << decision_verdict_to_string(result.verdict) << std::endl;
        std::cout << "chat: " << decision_verdict_to_string(chat_result.verdict) << std::endl;
        std::cout << "\nrobot_control H_max: " << bands.H_max << std::endl;
        std::cout << "chat H_max: " << chat_bands.H_max << std::endl;
    }
    
    return 0;
}

