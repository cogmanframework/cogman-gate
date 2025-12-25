/**
 * Cognitive Decision Gate Example
 * 
 * This example demonstrates usage of the Cognitive Decision Gate
 */

#include "cogman_kernel/cognitive_decision_gate.hpp"
#include <iostream>
#include <iomanip>

using namespace cogman_kernel;

int main() {
    std::cout << "=== Cognitive Decision Gate Example ===" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    
    // Create decision gate with default profile
    CognitiveDecisionGate gate("OWNER_STANDARD_V1");
    
    // Example 1: Safe state (ALLOW)
    std::cout << "\n--- Example 1: Safe State ---" << std::endl;
    Snapshot snapshot1;
    snapshot1.I = 0.8;
    snapshot1.P = 0.6;
    snapshot1.S = 0.7;
    snapshot1.H = 0.3;        // Low entropy
    snapshot1.T_psi = 0.4;    // Low temperature
    snapshot1.delta_E_psi = 0.3;  // Small energy change
    snapshot1.E_total = 2.5;
    
    DecisionResult result1 = gate.evaluate_snapshot(snapshot1);
    std::cout << "Decision: " << decision_status_to_string(result1.decision) << std::endl;
    std::cout << "Severity: " << result1.severity << std::endl;
    std::cout << "Reasons:" << std::endl;
    for (const auto& reason : result1.reasons) {
        std::cout << "  - " << reason << std::endl;
    }
    
    // Example 2: High entropy (REVIEW)
    std::cout << "\n--- Example 2: High Entropy ---" << std::endl;
    Snapshot snapshot2;
    snapshot2.I = 0.8;
    snapshot2.P = 0.6;
    snapshot2.S = 0.7;
    snapshot2.H = 0.75;       // High entropy (> 0.65)
    snapshot2.T_psi = 0.5;
    snapshot2.delta_E_psi = 0.4;
    snapshot2.E_total = 2.5;
    
    DecisionResult result2 = gate.evaluate_snapshot(snapshot2);
    std::cout << "Decision: " << decision_status_to_string(result2.decision) << std::endl;
    std::cout << "Severity: " << result2.severity << std::endl;
    std::cout << "Reasons:" << std::endl;
    for (const auto& reason : result2.reasons) {
        std::cout << "  - " << reason << std::endl;
    }
    
    // Example 3: Critical state (BLOCK)
    std::cout << "\n--- Example 3: Critical State ---" << std::endl;
    Snapshot snapshot3;
    snapshot3.I = 0.8;
    snapshot3.P = -0.8;       // Very negative
    snapshot3.S = 0.2;        // Low stability
    snapshot3.H = 0.9;        // Very high entropy
    snapshot3.T_psi = 0.9;    // High temperature
    snapshot3.delta_E_psi = 1.5;  // Large energy change
    snapshot3.E_total = 2.5;
    
    DecisionResult result3 = gate.evaluate_snapshot(snapshot3);
    std::cout << "Decision: " << decision_status_to_string(result3.decision) << std::endl;
    std::cout << "Severity: " << result3.severity << std::endl;
    std::cout << "Reasons:" << std::endl;
    for (const auto& reason : result3.reasons) {
        std::cout << "  - " << reason << std::endl;
    }
    
    // Example 4: Custom thresholds
    std::cout << "\n--- Example 4: Custom Thresholds ---" << std::endl;
    CognitiveDecisionGate custom_gate("CUSTOM_PROFILE");
    auto& thresholds = custom_gate.get_thresholds();
    thresholds.H_max_allow = 0.7;  // More permissive
    thresholds.H_max_review = 0.9;
    
    DecisionResult result4 = custom_gate.evaluate_snapshot(snapshot2);
    std::cout << "Decision: " << decision_status_to_string(result4.decision) << std::endl;
    std::cout << "Profile: " << result4.standard_profile << std::endl;
    
    return 0;
}

