/**
 * CORE-9 Decision Gate Example (Production Spec)
 * 
 * This example demonstrates the production-ready CORE-9 gate
 * that follows the spec exactly.
 */

#include "cogman_kernel/core9_gate.hpp"
#include <iostream>
#include <iomanip>
#include <vector>

using namespace cogman_kernel;

int main() {
    std::cout << "=== CORE-9 Decision Gate Example ===" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    
    // Create robot_control bands (stricter)
    DecisionBands bands = create_robot_control_bands();
    Core9DecisionGate gate(bands);
    
    // Example 1: ALLOW - All metrics within bounds
    std::cout << "\n--- Example 1: ALLOW ---" << std::endl;
    DecisionInput input1;
    input1.metrics.E_mu = 50.0;  // In accept range [30, 80]
    input1.metrics.H = 0.5;      // Below H_max (0.60)
    input1.metrics.D = 0.25;     // Below D_max (0.30)
    input1.metrics.S = 1.0;      // Safety rule OK
    input1.metrics.T = 0.5;       // Positive trend
    input1.metrics.V = 4.0;       // Below V_max (6.0)
    input1.context = "robot_control";
    
    DecisionResult result1 = gate.evaluate(input1);
    std::cout << "Verdict: " << decision_verdict_to_string(result1.verdict) << std::endl;
    std::cout << "Reason: " << result1.reasons[0] << std::endl;
    std::cout << "\nExplainable Record:\n" << result1.to_explainable_record() << std::endl;
    
    // Example 2: BLOCK - Safety rule failed
    std::cout << "\n--- Example 2: BLOCK (Safety Rule Failed) ---" << std::endl;
    DecisionInput input2;
    input2.metrics.E_mu = 50.0;
    input2.metrics.H = 0.5;
    input2.metrics.D = 0.25;
    input2.metrics.S = 0.0;      // Safety rule FAILED
    input2.metrics.T = 0.5;
    input2.metrics.V = 4.0;
    input2.context = "robot_control";
    
    DecisionResult result2 = gate.evaluate(input2);
    std::cout << "Verdict: " << decision_verdict_to_string(result2.verdict) << std::endl;
    std::cout << "Rule Fail: " << (result2.rule_fail ? "YES" : "NO") << std::endl;
    std::cout << "Reason: " << result2.reasons[0] << std::endl;
    
    // Example 3: BLOCK - Eμ in restrict range
    std::cout << "\n--- Example 3: BLOCK (Eμ Restrict) ---" << std::endl;
    DecisionInput input3;
    input3.metrics.E_mu = 10.0;  // In restrict range (< 15)
    input3.metrics.H = 0.5;
    input3.metrics.D = 0.25;
    input3.metrics.S = 1.0;
    input3.metrics.T = 0.5;
    input3.metrics.V = 4.0;
    input3.context = "robot_control";
    
    DecisionResult result3 = gate.evaluate(input3);
    std::cout << "Verdict: " << decision_verdict_to_string(result3.verdict) << std::endl;
    std::cout << "Reason: " << result3.reasons[0] << std::endl;
    
    // Example 4: REVIEW - High entropy
    std::cout << "\n--- Example 4: REVIEW (High Entropy) ---" << std::endl;
    DecisionInput input4;
    input4.metrics.E_mu = 50.0;
    input4.metrics.H = 0.65;     // Above H_max (0.60)
    input4.metrics.D = 0.25;
    input4.metrics.S = 1.0;
    input4.metrics.T = 0.5;
    input4.metrics.V = 4.0;
    input4.context = "robot_control";
    
    DecisionResult result4 = gate.evaluate(input4);
    std::cout << "Verdict: " << decision_verdict_to_string(result4.verdict) << std::endl;
    std::cout << "Reason: " << result4.reasons[0] << std::endl;
    
    // Example 5: REVIEW - High semantic drift
    std::cout << "\n--- Example 5: REVIEW (High Semantic Drift) ---" << std::endl;
    DecisionInput input5;
    input5.metrics.E_mu = 50.0;
    input5.metrics.H = 0.5;
    input5.metrics.D = 0.35;     // Above D_max (0.30)
    input5.metrics.S = 1.0;
    input5.metrics.T = 0.5;
    input5.metrics.V = 4.0;
    input5.context = "robot_control";
    
    DecisionResult result5 = gate.evaluate(input5);
    std::cout << "Verdict: " << decision_verdict_to_string(result5.verdict) << std::endl;
    std::cout << "Reason: " << result5.reasons[0] << std::endl;
    
    // Example 6: REVIEW - Negative trend AND Eμ in caution
    std::cout << "\n--- Example 6: REVIEW (Negative Trend + Eμ Caution) ---" << std::endl;
    DecisionInput input6;
    input6.metrics.E_mu = 20.0;  // In caution range [15, 30)
    input6.metrics.H = 0.5;
    input6.metrics.D = 0.25;
    input6.metrics.S = 1.0;
    input6.metrics.T = -2.0;     // Negative trend
    input6.metrics.V = 4.0;
    input6.E_mu_history = {25.0, 23.0, 21.0, 20.0};  // Declining
    input6.context = "robot_control";
    
    DecisionResult result6 = gate.evaluate(input6);
    std::cout << "Verdict: " << decision_verdict_to_string(result6.verdict) << std::endl;
    std::cout << "Reason: " << result6.reasons[0] << std::endl;
    std::cout << "Calculated T: " << result6.metrics.T << std::endl;
    
    // Example 7: Different contexts
    std::cout << "\n--- Example 7: Context Comparison ---" << std::endl;
    
    DecisionBands chat_bands = create_chat_bands();
    Core9DecisionGate chat_gate(chat_bands);
    
    DecisionInput input7;
    input7.metrics.E_mu = 50.0;
    input7.metrics.H = 0.65;     // Would be REVIEW in robot_control, but...
    input7.metrics.D = 0.25;
    input7.metrics.S = 1.0;
    input7.metrics.T = 0.5;
    input7.metrics.V = 4.0;
    input7.context = "chat";
    
    DecisionResult result7 = chat_gate.evaluate(input7);
    std::cout << "Context: " << result7.context << std::endl;
    std::cout << "Verdict: " << decision_verdict_to_string(result7.verdict) << std::endl;
    std::cout << "H_max for chat: " << chat_bands.H_max << " (vs robot_control: " 
              << bands.H_max << ")" << std::endl;
    
    return 0;
}

