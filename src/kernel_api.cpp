/**
 * Cogman Kernel - C ABI / FFI Boundary
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Stable C API for FFI boundary
 */

#include "cogman_kernel/kernel_api.hpp"
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/core9_gate.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include "cogman_kernel/errors.hpp"
#include <cstring>
#include <vector>
#include <string>
#include <mutex>
#include <limits>

// Forward declaration
namespace cogman_kernel {
    EnergyState compute_energy_projection(
        const EPS8State& state,
        const NeuralComponents& neural,
        double theta_phase,
        double E_pred,
        const DecisionParams& decision_params
    );
}

// Thread-safe error storage for C API
namespace {
    std::mutex error_mutex;
    cogman_kernel::ErrorCode last_error = cogman_kernel::ErrorCode::SUCCESS;
    std::string last_error_message;
    
    void set_error(cogman_kernel::ErrorCode code, const std::string& message) {
        std::lock_guard<std::mutex> lock(error_mutex);
        last_error = code;
        last_error_message = message;
    }
    
    void set_error_from_exception(const cogman_kernel::KernelException& e) {
        std::lock_guard<std::mutex> lock(error_mutex);
        last_error = e.code();
        last_error_message = e.full_message();
    }
}

extern "C" {

uint32_t cogman_get_last_error() {
    std::lock_guard<std::mutex> lock(error_mutex);
    return static_cast<uint32_t>(last_error);
}

const char* cogman_get_last_error_message() {
    std::lock_guard<std::mutex> lock(error_mutex);
    return last_error_message.c_str();
}

int cogman_energy_projection(
    const EPS8State* state,
    const double* neural_components,
    double theta_phase,
    double E_pred,
    const DecisionParams* decision_params,
    EnergyState* output
) {
    // Reset error state
    set_error(cogman_kernel::ErrorCode::SUCCESS, "");
    
    if (!state || !neural_components || !decision_params || !output) {
        set_error(cogman_kernel::ErrorCode::INVALID_INPUT, "Null pointer argument");
        return static_cast<int>(cogman_kernel::ErrorCode::INVALID_INPUT);
    }
    
    try {
    
    // Convert C struct to C++ struct
    cogman_kernel::EPS8State cpp_state;
    cpp_state.I = state->I;
    cpp_state.P = state->P;
    cpp_state.S = state->S;
    cpp_state.H = state->H;
    cpp_state.F = state->F;
    cpp_state.A = state->A;
    cpp_state.S_a = state->S_a;
    cpp_state.theta = state->theta;
    
    cogman_kernel::NeuralComponents neural;
    neural.dopamine = neural_components[0];
    neural.serotonin = neural_components[1];
    neural.oxytocin = neural_components[2];
    neural.adrenaline = neural_components[3];
    neural.cortisol = neural_components[4];
    
    cogman_kernel::DecisionParams cpp_params;
    cpp_params.rule_fail = decision_params->rule_fail != 0;
    cpp_params.E_mu_restrict_min = decision_params->E_mu_restrict_min;
    cpp_params.E_mu_restrict_max = decision_params->E_mu_restrict_max;
    cpp_params.H_threshold = decision_params->H_threshold;
    cpp_params.D_traj_threshold = decision_params->D_traj_threshold;
    
    cogman_kernel::EnergyState energy = compute_energy_projection(
        cpp_state, neural, theta_phase, E_pred, cpp_params
    );
    
    // Convert C++ struct to C struct
    output->delta_E_psi = energy.delta_E_psi;
    output->E_reflex = energy.E_reflex;
    output->delta_E_psi_theta = energy.delta_E_psi_theta;
    output->E_mind = energy.E_mind;
    output->E_coherence = energy.E_coherence;
    output->E_neural = energy.E_neural;
    output->E_bind = energy.E_bind;
    output->E_mem = energy.E_mem;
    output->verdict = static_cast<int>(energy.verdict);
    
    return 0; // Success
    
    } catch (const cogman_kernel::KernelException& e) {
        set_error_from_exception(e);
        return static_cast<int>(e.code());
    } catch (const std::exception& e) {
        set_error(cogman_kernel::ErrorCode::SYSTEM_ERROR, std::string("System error: ") + e.what());
        return static_cast<int>(cogman_kernel::ErrorCode::SYSTEM_ERROR);
    } catch (...) {
        set_error(cogman_kernel::ErrorCode::UNKNOWN_ERROR, "Unknown error occurred");
        return static_cast<int>(cogman_kernel::ErrorCode::UNKNOWN_ERROR);
    }
}

int cogman_decision_gate(
    const DecisionParams* params,
    double H_current,
    double D_traj_current
) {
    set_error(cogman_kernel::ErrorCode::SUCCESS, "");
    
    if (!params) {
        set_error(cogman_kernel::ErrorCode::INVALID_INPUT, "Null pointer argument");
        return 2; // BLOCK (fail-closed)
    }
    
    try {
        cogman_kernel::DecisionParams cpp_params;
        cpp_params.rule_fail = params->rule_fail != 0;
        cpp_params.H_threshold = params->H_threshold;
        cpp_params.D_traj_threshold = params->D_traj_threshold;
        
        cogman_kernel::DecisionVerdict verdict = decision_gate(cpp_params, H_current, D_traj_current);
        return static_cast<int>(verdict);
    } catch (const cogman_kernel::KernelException& e) {
        set_error_from_exception(e);
        return 2; // BLOCK on error (fail-closed)
    } catch (const std::exception& e) {
        set_error(cogman_kernel::ErrorCode::SYSTEM_ERROR, std::string("System error: ") + e.what());
        return 2; // BLOCK on error (fail-closed)
    } catch (...) {
        set_error(cogman_kernel::ErrorCode::UNKNOWN_ERROR, "Unknown error occurred");
        return 2; // BLOCK on error (fail-closed)
    }
}

int cogman_validate_state(const EPS8State* state) {
    set_error(cogman_kernel::ErrorCode::SUCCESS, "");
    
    if (!state) {
        set_error(cogman_kernel::ErrorCode::INVALID_INPUT, "Null pointer argument");
        return 0; // Invalid
    }
    
    try {
        cogman_kernel::EPS8State cpp_state;
        cpp_state.I = state->I;
        cpp_state.P = state->P;
        cpp_state.S = state->S;
        cpp_state.H = state->H;
        cpp_state.F = state->F;
        cpp_state.A = state->A;
        cpp_state.S_a = state->S_a;
        cpp_state.theta = state->theta;
        
        return cpp_state.validate() ? 1 : 0;
    } catch (const cogman_kernel::KernelException& e) {
        set_error_from_exception(e);
        return 0; // Invalid
    } catch (...) {
        set_error(cogman_kernel::ErrorCode::UNKNOWN_ERROR, "Unknown error during validation");
        return 0; // Invalid
    }
}

int cogman_core9_evaluate(
    const DecisionInput* input,
    DecisionResult* output
) {
    set_error(cogman_kernel::ErrorCode::SUCCESS, "");
    
    if (!input || !output) {
        set_error(cogman_kernel::ErrorCode::INVALID_INPUT, "Null pointer argument");
        return static_cast<int>(cogman_kernel::ErrorCode::INVALID_INPUT);
    }
    
    try {
    
    // Convert C structs to C++ structs
    cogman_kernel::DecisionBands bands;
    bands.D_max = input->bands.D_max;
    bands.H_max = input->bands.H_max;
    bands.V_max = input->bands.V_max;
    bands.E_mu_accept_min = input->bands.E_mu_accept_min;
    bands.E_mu_accept_max = input->bands.E_mu_accept_max;
    bands.E_mu_caution_min = input->bands.E_mu_caution_min;
    bands.E_mu_caution_max = input->bands.E_mu_caution_max;
    bands.E_mu_restrict_max = input->bands.E_mu_restrict_max;
    bands.context = input->bands.context;
    bands.version = input->bands.version;
    
    cogman_kernel::DecisionInput cpp_input;
    cpp_input.metrics.E_mu = input->metrics.E_mu;
    cpp_input.metrics.H = input->metrics.H;
    cpp_input.metrics.D = input->metrics.D;
    cpp_input.metrics.S = input->metrics.S;
    cpp_input.metrics.T = input->metrics.T;
    cpp_input.metrics.V = input->metrics.V;
    cpp_input.context = input->context;
    
    // Convert Eμ history
    if (input->E_mu_history && input->E_mu_history_size > 0) {
        cpp_input.E_mu_history.assign(
            input->E_mu_history,
            input->E_mu_history + input->E_mu_history_size
        );
    }
    
    // Create gate and evaluate
    cogman_kernel::Core9DecisionGate gate(bands);
    cogman_kernel::DecisionResult result = gate.evaluate(cpp_input);
    
    // Convert C++ result to C result
    // DecisionResult.verdict is DecisionVerdict enum
    output->verdict = static_cast<int>(result.verdict);
    output->metrics.E_mu = result.metrics.E_mu;
    output->metrics.H = result.metrics.H;
    output->metrics.D = result.metrics.D;
    output->metrics.S = result.metrics.S;
    output->metrics.T = result.metrics.T;
    output->metrics.V = result.metrics.V;
    output->rule_fail = result.rule_fail ? 1 : 0;
    
    // Copy reasons (allocate memory)
    output->reasons_count = result.reasons.size();
    if (output->reasons_count > 0) {
        output->reasons = new char*[output->reasons_count];
        for (size_t i = 0; i < result.reasons.size(); ++i) {
            size_t len = result.reasons[i].length();
            output->reasons[i] = new char[len + 1];
            std::strcpy(output->reasons[i], result.reasons[i].c_str());
        }
    } else {
        output->reasons = nullptr;
    }
    
    std::strncpy(output->protocol, result.protocol.c_str(), sizeof(output->protocol) - 1);
    output->protocol[sizeof(output->protocol) - 1] = '\0';
    
    std::strncpy(output->context, result.context.c_str(), sizeof(output->context) - 1);
    output->context[sizeof(output->context) - 1] = '\0';
    
    return 0; // Success
    
    } catch (const cogman_kernel::KernelException& e) {
        set_error_from_exception(e);
        return static_cast<int>(e.code());
    } catch (const std::exception& e) {
        set_error(cogman_kernel::ErrorCode::SYSTEM_ERROR, std::string("System error: ") + e.what());
        return static_cast<int>(cogman_kernel::ErrorCode::SYSTEM_ERROR);
    } catch (...) {
        set_error(cogman_kernel::ErrorCode::UNKNOWN_ERROR, "Unknown error occurred");
        return static_cast<int>(cogman_kernel::ErrorCode::UNKNOWN_ERROR);
    }
}

void cogman_free_decision_result(DecisionResult* result) {
    if (!result) return;
    
    // Free allocated reason strings
    if (result->reasons) {
        for (int i = 0; i < result->reasons_count; ++i) {
            delete[] result->reasons[i];
        }
        delete[] result->reasons;
        result->reasons = nullptr;
        result->reasons_count = 0;
    }
}

} // extern "C"

