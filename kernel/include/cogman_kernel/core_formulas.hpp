/**
 * Cogman Kernel - Core Formulas (DECLARATION)
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Core formulas (CORE-1 to CORE-9) must not be modified without review
 * 
 * This file contains DECLARATIONS for the 9 core formulas.
 * Implementations are in src/core_formulas.cpp
 */

#ifndef COGMAN_KERNEL_CORE_FORMULAS_HPP
#define COGMAN_KERNEL_CORE_FORMULAS_HPP

#include "eps8.hpp"
#include "types.hpp"

namespace cogman_kernel {

// CORE-1: Energy of Perception (ΔEΨ)
double energy_of_perception(double I, double P, double S_a, double H, bool use_absolute = true);

// CORE-2: Reflex Energy (E_reflex)
double reflex_energy(double delta_E_psi, double A);

// CORE-3: Directional Reflex Energy (ΔEΨ_theta)
double directional_reflex_energy(double delta_E_psi, double theta_phase);

// CORE-4: Cognitive Energy (E_mind)
double cognitive_energy(double I, double A, double H);

// CORE-5: Coherence Energy (E_coherence)
double coherence_energy(double S, double A, double H);

// CORE-6: Neuro-Energetic Sum (E_neural)
double neural_energetic_sum(const NeuralComponents& neural);

// CORE-7: Binding Energy (E_bind)
double binding_energy(double E_mind, double E_neural, double E_coherence);

// CORE-8: Memory Encoding Energy (E_mem)
double memory_encoding_energy(double A, double E_bind, double E_pred);

// CORE-9: Decision Gate Verdict (G_decision)
DecisionVerdict decision_gate(const DecisionParams& params, double H_current, double D_traj_current = 0.0);

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_CORE_FORMULAS_HPP

