/**
 * Cogman Kernel - Core Formulas (IMPLEMENTATION)
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Core formulas (CORE-1 to CORE-9) must not be modified without review
 * 
 * This file contains IMPLEMENTATIONS for the 9 core formulas.
 * Declarations are in include/cogman_kernel/core_formulas.hpp
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include "cogman_kernel/errors.hpp"
#include <algorithm>
#include <cmath>
#include <limits>

namespace cogman_kernel {

// CORE-1: Energy of Perception (ΔEΨ)
double energy_of_perception(double I, double P, double S_a, double H, bool use_absolute) {
    // Check for NaN and infinity
    check_nan("I", I);
    check_nan("P", P);
    check_nan("S_a", S_a);
    check_nan("H", H);
    
    check_infinity("I", I);
    check_infinity("P", P);
    check_infinity("S_a", S_a);
    check_infinity("H", H);
    
    // Range validation
    check_range_min("I", I, 0.0);
    check_range("S_a", S_a, 0.0, 1.0);
    check_range("H", H, 0.0, 1.0);
    
    double P_value = use_absolute ? std::abs(P) : P;
    double result = I * P_value * S_a * (1.0 - H);
    
    // Check result for NaN/infinity
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW, 
                              "Energy of perception computation resulted in NaN or infinity");
    }
    
    return result;
}

// CORE-2: Reflex Energy (E_reflex)
double reflex_energy(double delta_E_psi, double A) {
    check_nan("delta_E_psi", delta_E_psi);
    check_nan("A", A);
    check_infinity("delta_E_psi", delta_E_psi);
    check_infinity("A", A);
    check_range("A", A, 0.0, 1.0);
    
    double result = delta_E_psi * A;
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Reflex energy computation resulted in NaN or infinity");
    }
    return result;
}

// CORE-3: Directional Reflex Energy (ΔEΨ_theta)
double directional_reflex_energy(double delta_E_psi, double theta_phase) {
    check_nan("delta_E_psi", delta_E_psi);
    check_nan("theta_phase", theta_phase);
    check_infinity("delta_E_psi", delta_E_psi);
    check_infinity("theta_phase", theta_phase);
    
    // theta_phase should be in reasonable range (not strictly [0, 2π] as it can wrap)
    // But check for extreme values that might cause issues
    if (std::abs(theta_phase) > 1000.0) {
        throw InvalidRangeException("theta_phase", theta_phase, -1000.0, 1000.0);
    }
    
    double result = delta_E_psi * std::cos(theta_phase);
    
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Directional reflex energy computation resulted in NaN or infinity");
    }
    
    return result;
}

// CORE-4: Cognitive Energy (E_mind)
double cognitive_energy(double I, double A, double H) {
    check_nan("I", I);
    check_nan("A", A);
    check_nan("H", H);
    check_infinity("I", I);
    check_infinity("A", A);
    check_infinity("H", H);
    check_range_min("I", I, 0.0);
    check_range("A", A, 0.0, 1.0);
    check_range("H", H, 0.0, 1.0);
    
    double result = I * A * (1.0 - H);
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Cognitive energy computation resulted in NaN or infinity");
    }
    return result;
}

// CORE-5: Coherence Energy (E_coherence)
double coherence_energy(double S, double A, double H) {
    check_nan("S", S);
    check_nan("A", A);
    check_nan("H", H);
    check_infinity("S", S);
    check_infinity("A", A);
    check_infinity("H", H);
    check_range("S", S, 0.0, 1.0);
    check_range("A", A, 0.0, 1.0);
    check_range("H", H, 0.0, 1.0);
    
    double result = S * A * (1.0 - H);
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Coherence energy computation resulted in NaN or infinity");
    }
    return result;
}

// CORE-6: Neuro-Energetic Sum (E_neural)
double neural_energetic_sum(const NeuralComponents& neural) {
    // Validate all neural components
    check_nan("neural.dopamine", neural.dopamine);
    check_nan("neural.serotonin", neural.serotonin);
    check_nan("neural.oxytocin", neural.oxytocin);
    check_nan("neural.adrenaline", neural.adrenaline);
    check_nan("neural.cortisol", neural.cortisol);
    
    check_infinity("neural.dopamine", neural.dopamine);
    check_infinity("neural.serotonin", neural.serotonin);
    check_infinity("neural.oxytocin", neural.oxytocin);
    check_infinity("neural.adrenaline", neural.adrenaline);
    check_infinity("neural.cortisol", neural.cortisol);
    
    // Neural components are typically non-negative (concentrations)
    // But allow negative values for flexibility (some models use signed values)
    // Just check for extreme values
    const double max_neural_value = 1e6;  // Reasonable upper bound
    check_range_max("neural.dopamine", std::abs(neural.dopamine), max_neural_value);
    check_range_max("neural.serotonin", std::abs(neural.serotonin), max_neural_value);
    check_range_max("neural.oxytocin", std::abs(neural.oxytocin), max_neural_value);
    check_range_max("neural.adrenaline", std::abs(neural.adrenaline), max_neural_value);
    check_range_max("neural.cortisol", std::abs(neural.cortisol), max_neural_value);
    
    double result = neural.dopamine + neural.serotonin + neural.oxytocin + 
                    neural.adrenaline + neural.cortisol;
    
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Neural energetic sum computation resulted in NaN or infinity");
    }
    
    return result;
}

// CORE-7: Binding Energy (E_bind)
double binding_energy(double E_mind, double E_neural, double E_coherence) {
    check_nan("E_mind", E_mind);
    check_nan("E_neural", E_neural);
    check_nan("E_coherence", E_coherence);
    
    check_infinity("E_mind", E_mind);
    check_infinity("E_neural", E_neural);
    check_infinity("E_coherence", E_coherence);
    
    // Check for extreme values that might cause overflow
    const double max_energy_value = 1e10;  // Reasonable upper bound
    check_range_max("E_mind", std::abs(E_mind), max_energy_value);
    check_range_max("E_neural", std::abs(E_neural), max_energy_value);
    check_range_max("E_coherence", std::abs(E_coherence), max_energy_value);
    
    double result = E_mind + E_neural + E_coherence;
    
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Binding energy computation resulted in NaN or infinity");
    }
    
    return result;
}

// CORE-8: Memory Encoding Energy (E_mem)
double memory_encoding_energy(double A, double E_bind, double E_pred) {
    check_nan("A", A);
    check_nan("E_bind", E_bind);
    check_nan("E_pred", E_pred);
    check_infinity("A", A);
    check_infinity("E_bind", E_bind);
    check_infinity("E_pred", E_pred);
    check_range("A", A, 0.0, 1.0);
    
    double result = A * (E_bind + E_pred);
    if (std::isnan(result) || std::isinf(result)) {
        throw FormulaException(ErrorCode::FORMULA_OVERFLOW,
                              "Memory encoding energy computation resulted in NaN or infinity");
    }
    return result;
}

// CORE-9: Decision Gate Verdict (G_decision)
DecisionVerdict decision_gate(const DecisionParams& params, double H_current, double D_traj_current) {
    // Validate inputs
    check_nan("H_current", H_current);
    check_nan("D_traj_current", D_traj_current);
    check_nan("params.H_threshold", params.H_threshold);
    check_nan("params.D_traj_threshold", params.D_traj_threshold);
    
    check_infinity("H_current", H_current);
    check_infinity("D_traj_current", D_traj_current);
    check_infinity("params.H_threshold", params.H_threshold);
    check_infinity("params.D_traj_threshold", params.D_traj_threshold);
    
    // Validate ranges
    check_range("H_current", H_current, 0.0, 1.0);
    check_range_min("D_traj_current", D_traj_current, 0.0);
    check_range("params.H_threshold", params.H_threshold, 0.0, 1.0);
    check_range_min("params.D_traj_threshold", params.D_traj_threshold, 0.0);
    
    // Rule violation → BLOCK
    if (params.rule_fail) {
        return DecisionVerdict::BLOCK;
    }
    
    // High entropy or high trajectory distance → REVIEW
    if (H_current >= params.H_threshold || D_traj_current >= params.D_traj_threshold) {
        return DecisionVerdict::REVIEW;
    }
    
    // Default → ALLOW
    return DecisionVerdict::ALLOW;
}

} // namespace cogman_kernel

