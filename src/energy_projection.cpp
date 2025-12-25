/**
 * Cogman Kernel - Energy Projection (EPS-8 computation)
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Core energy projection must not be modified without review
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include "cogman_kernel/errors.hpp"

namespace cogman_kernel {

/**
 * Compute energy projection from EPS-8 state
 */
EnergyState compute_energy_projection(
    const EPS8State& state,
    const NeuralComponents& neural,
    double theta_phase,
    double E_pred,
    const DecisionParams& decision_params
) {
    // Validate EPS-8 state
    if (!state.validate()) {
        throw InvalidEPS8StateException("EPS-8 state validation failed");
    }
    
    // Validate theta_phase
    check_nan("theta_phase", theta_phase);
    check_infinity("theta_phase", theta_phase);
    
    // Validate E_pred
    check_nan("E_pred", E_pred);
    check_infinity("E_pred", E_pred);
    
    // Validate decision params thresholds
    check_nan("decision_params.H_threshold", decision_params.H_threshold);
    check_nan("decision_params.D_traj_threshold", decision_params.D_traj_threshold);
    check_range("decision_params.H_threshold", decision_params.H_threshold, 0.0, 1.0);
    check_range_min("decision_params.D_traj_threshold", decision_params.D_traj_threshold, 0.0);
    
    EnergyState energy;
    
    // CORE-1: Energy of Perception
    energy.delta_E_psi = energy_of_perception(state.I, state.P, state.S_a, state.H, true);
    
    // CORE-2: Reflex Energy
    energy.E_reflex = reflex_energy(energy.delta_E_psi, state.A);
    
    // CORE-3: Directional Reflex Energy
    energy.delta_E_psi_theta = directional_reflex_energy(energy.delta_E_psi, theta_phase);
    
    // CORE-4: Cognitive Energy
    energy.E_mind = cognitive_energy(state.I, state.A, state.H);
    
    // CORE-5: Coherence Energy
    energy.E_coherence = coherence_energy(state.S, state.A, state.H);
    
    // CORE-6: Neuro-Energetic Sum
    energy.E_neural = neural_energetic_sum(neural);
    
    // CORE-7: Binding Energy
    energy.E_bind = binding_energy(energy.E_mind, energy.E_neural, energy.E_coherence);
    
    // CORE-8: Memory Encoding Energy
    energy.E_mem = memory_encoding_energy(state.A, energy.E_bind, E_pred);
    
    // CORE-9: Decision Gate
    energy.verdict = decision_gate(decision_params, state.H);
    
    // Validate final energy state
    // Check all energy values for NaN/infinity
    if (std::isnan(energy.delta_E_psi) || std::isinf(energy.delta_E_psi) ||
        std::isnan(energy.E_reflex) || std::isinf(energy.E_reflex) ||
        std::isnan(energy.delta_E_psi_theta) || std::isinf(energy.delta_E_psi_theta) ||
        std::isnan(energy.E_mind) || std::isinf(energy.E_mind) ||
        std::isnan(energy.E_coherence) || std::isinf(energy.E_coherence) ||
        std::isnan(energy.E_neural) || std::isinf(energy.E_neural) ||
        std::isnan(energy.E_bind) || std::isinf(energy.E_bind) ||
        std::isnan(energy.E_mem) || std::isinf(energy.E_mem)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Energy projection resulted in NaN or infinity in one or more energy values");
    }
    
    return energy;
}

} // namespace cogman_kernel

