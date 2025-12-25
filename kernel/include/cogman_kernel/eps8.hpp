/**
 * Cogman Kernel - EPS-8 State Definition
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - EPS-8 state definition must not be modified without review
 * 
 * EPS-8: Energetic Perception State (8 dimensions)
 * Ψ = { I, P, S, H, F, A, S_a, theta }
 */

#ifndef COGMAN_KERNEL_EPS8_HPP
#define COGMAN_KERNEL_EPS8_HPP

#include "types.hpp"
#include <limits>

namespace cogman_kernel {

/**
 * EPS-8 State Vector
 * 
 * Ψ = { I, P, S, H, F, A, S_a, theta }
 */
struct EPS8State {
    double I = 0.0;      // Intensity [I >= 0]
    double P = 0.0;      // Polarity [P ∈ ℝ]
    double S = 0.0;      // Stability [0 <= S <= 1]
    double H = 0.0;      // Entropy/Uncertainty [0 <= H <= 1]
    double F = 0.0;      // External Force [F ∈ ℝ]
    double A = 0.0;      // Awareness [0 <= A <= 1]
    double S_a = 0.0;    // Sub-awareness/Background activation [0 <= S_a <= 1]
    double theta = 0.0;  // Phase/Phase angle [theta ∈ ℝ]
    
    // Validate state
    bool validate() const;
};

/**
 * Energy State (result of core formulas)
 */
struct EnergyState {
    double delta_E_psi = 0.0;        // CORE-1: Energy of Perception
    double E_reflex = 0.0;           // CORE-2: Reflex Energy
    double delta_E_psi_theta = 0.0;  // CORE-3: Directional Reflex Energy
    double E_mind = 0.0;             // CORE-4: Cognitive Energy
    double E_coherence = 0.0;        // CORE-5: Coherence Energy
    double E_neural = 0.0;           // CORE-6: Neuro-Energetic Sum
    double E_bind = 0.0;             // CORE-7: Binding Energy
    double E_mem = 0.0;              // CORE-8: Memory Encoding Energy
    DecisionVerdict verdict = DecisionVerdict::ALLOW;  // CORE-9: Decision Gate
};

/**
 * Decision Parameters
 */
struct DecisionParams {
    bool rule_fail = false;
    double E_mu_restrict_min = -std::numeric_limits<double>::max();
    double E_mu_restrict_max = std::numeric_limits<double>::max();
    double H_threshold = 0.85;
    double D_traj_threshold = 0.7;
};

/**
 * Compute energy projection from EPS-8 state
 * 
 * This function computes all core energies (CORE-1 to CORE-9) from an EPS-8 state.
 * 
 * @param state EPS-8 state
 * @param neural Neural components
 * @param theta_phase Theta phase value
 * @param E_pred Predicted energy
 * @param decision_params Decision parameters
 * @return EnergyState with all computed energies and verdict
 */
EnergyState compute_energy_projection(
    const EPS8State& state,
    const NeuralComponents& neural,
    double theta_phase,
    double E_pred,
    const DecisionParams& decision_params
);

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_EPS8_HPP

