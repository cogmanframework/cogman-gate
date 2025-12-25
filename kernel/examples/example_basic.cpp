/**
 * Basic Kernel Usage Example
 * 
 * This example demonstrates basic usage of the Cogman Kernel
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include <iostream>
#include <iomanip>

using namespace cogman_kernel;

int main() {
    std::cout << "=== Cogman Kernel Basic Example ===" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    
    // 1. Create EPS-8 state
    EPS8State state;
    state.I = 0.8;      // Intensity
    state.P = 0.6;      // Polarity
    state.S = 0.7;      // Stability
    state.H = 0.3;      // Entropy
    state.A = 0.5;      // Awareness
    state.S_a = 0.6;    // Sub-awareness
    state.theta = 1.5;  // Phase angle
    
    // Validate state
    if (!state.validate()) {
        std::cerr << "Error: Invalid state!" << std::endl;
        return 1;
    }
    
    std::cout << "\nEPS-8 State:" << std::endl;
    std::cout << "  I = " << state.I << std::endl;
    std::cout << "  P = " << state.P << std::endl;
    std::cout << "  S = " << state.S << std::endl;
    std::cout << "  H = " << state.H << std::endl;
    std::cout << "  A = " << state.A << std::endl;
    std::cout << "  S_a = " << state.S_a << std::endl;
    
    // 2. Compute individual formulas
    std::cout << "\n=== Core Formulas ===" << std::endl;
    
    // CORE-1: Energy of Perception
    double delta_E_psi = energy_of_perception(state.I, state.P, state.S_a, state.H, true);
    std::cout << "CORE-1: ΔEΨ = " << delta_E_psi << std::endl;
    
    // CORE-2: Reflex Energy
    double E_reflex = reflex_energy(delta_E_psi, state.A);
    std::cout << "CORE-2: E_reflex = " << E_reflex << std::endl;
    
    // CORE-4: Cognitive Energy
    double E_mind = cognitive_energy(state.I, state.A, state.H);
    std::cout << "CORE-4: E_mind = " << E_mind << std::endl;
    
    // CORE-5: Coherence Energy
    double E_coherence = coherence_energy(state.S, state.A, state.H);
    std::cout << "CORE-5: E_coherence = " << E_coherence << std::endl;
    
    // 3. Neural components
    NeuralComponents neural;
    neural.dopamine = 0.4;
    neural.serotonin = 0.5;
    neural.oxytocin = 0.3;
    neural.adrenaline = 0.2;
    neural.cortisol = 0.1;
    
    // CORE-6: Neuro-Energetic Sum
    double E_neural = neural_energetic_sum(neural);
    std::cout << "CORE-6: E_neural = " << E_neural << std::endl;
    
    // 4. Complete energy projection
    std::cout << "\n=== Complete Energy Projection ===" << std::endl;
    
    DecisionParams decision_params;
    decision_params.H_threshold = 0.85;
    decision_params.D_traj_threshold = 0.7;
    
    EnergyState energy = compute_energy_projection(
        state,
        neural,
        state.theta,  // theta_phase
        0.5,          // E_pred
        decision_params
    );
    
    std::cout << "ΔEΨ = " << energy.delta_E_psi << std::endl;
    std::cout << "E_reflex = " << energy.E_reflex << std::endl;
    std::cout << "E_mind = " << energy.E_mind << std::endl;
    std::cout << "E_coherence = " << energy.E_coherence << std::endl;
    std::cout << "E_neural = " << energy.E_neural << std::endl;
    std::cout << "E_bind = " << energy.E_bind << std::endl;
    std::cout << "E_mem = " << energy.E_mem << std::endl;
    
    // 5. Decision gate
    std::cout << "\n=== Decision Gate (CORE-9) ===" << std::endl;
    std::cout << "Verdict: " << decision_verdict_to_string(energy.verdict) << std::endl;
    
    return 0;
}

