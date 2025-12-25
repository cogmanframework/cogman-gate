/**
 * Cogman Kernel - C ABI / Stable Interface
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Stable C API for FFI boundary
 * 
 * This file provides a stable C API for language bindings (Python, etc.)
 */

#ifndef COGMAN_KERNEL_API_HPP
#define COGMAN_KERNEL_API_HPP

#ifdef __cplusplus
#include <cstdint>
#else
#include <stdint.h>
#endif

#ifdef __cplusplus
extern "C" {
#endif

// Error code type (C-compatible)
typedef uint32_t ErrorCode;

// C-compatible structs (no C++ features)

/**
 * EPS-8 State (C-compatible)
 */
typedef struct {
    double I;
    double P;
    double S;
    double H;
    double F;
    double A;
    double S_a;
    double theta;
} EPS8State;

/**
 * Energy State (C-compatible)
 */
typedef struct {
    double delta_E_psi;
    double E_reflex;
    double delta_E_psi_theta;
    double E_mind;
    double E_coherence;
    double E_neural;
    double E_bind;
    double E_mem;
    int verdict;  // 0=ALLOW, 1=REVIEW, 2=BLOCK
} EnergyState;

/**
 * Decision Parameters (C-compatible)
 */
typedef struct {
    int rule_fail;  // 0=false, 1=true
    double E_mu_restrict_min;
    double E_mu_restrict_max;
    double H_threshold;
    double D_traj_threshold;
} DecisionParams;

/**
 * Core Metrics (C-compatible)
 */
typedef struct {
    double E_mu;
    double H;
    double D;
    double S;
    double T;
    double V;
} CoreMetrics;

/**
 * Decision Bands (C-compatible)
 */
typedef struct {
    double D_max;
    double H_max;
    double V_max;
    double E_mu_accept_min;
    double E_mu_accept_max;
    double E_mu_caution_min;
    double E_mu_caution_max;
    double E_mu_restrict_max;
    char context[64];
    char version[16];
} DecisionBands;

/**
 * Decision Input (C-compatible)
 */
typedef struct {
    CoreMetrics metrics;
    DecisionBands bands;
    double* E_mu_history;  // Array of doubles
    int E_mu_history_size;
    char context[64];
} DecisionInput;

/**
 * Decision Result (C-compatible)
 */
typedef struct {
    int verdict;  // 0=ALLOW, 1=REVIEW, 2=BLOCK
    CoreMetrics metrics;
    int rule_fail;  // 0=false, 1=true
    char** reasons;  // Array of C strings
    int reasons_count;
    char protocol[32];
    char context[64];
} DecisionResult;

// C API Functions

/**
 * Get last error code (for C API error handling)
 * Returns error code from last operation
 */
uint32_t cogman_get_last_error();

/**
 * Get last error message (for C API error handling)
 * Returns error message string (valid until next operation)
 */
const char* cogman_get_last_error_message();

/**
 * Compute energy projection (EPS-8 computation)
 * Returns 0 on success, non-zero on error
 */
int cogman_energy_projection(
    const EPS8State* state,
    const double* neural_components,  // [dopamine, serotonin, oxytocin, adrenaline, cortisol]
    double theta_phase,
    double E_pred,
    const DecisionParams* decision_params,
    EnergyState* output
);

/**
 * Compute decision gate (CORE-9 basic)
 */
int cogman_decision_gate(
    const DecisionParams* params,
    double H_current,
    double D_traj_current
);

/**
 * Validate EPS-8 state
 * Returns 1 if valid, 0 if invalid
 */
int cogman_validate_state(const EPS8State* state);

/**
 * CORE-9 Decision Gate (production spec)
 * Returns 0 on success, non-zero on error
 */
int cogman_core9_evaluate(
    const DecisionInput* input,
    DecisionResult* output
);

/**
 * Free decision result (free allocated strings)
 */
void cogman_free_decision_result(DecisionResult* result);

#ifdef __cplusplus
}
#endif

#endif // COGMAN_KERNEL_API_HPP
