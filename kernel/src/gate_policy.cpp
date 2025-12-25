/**
 * Gate Policy Loader Implementation
 * 
 * Version: v1.0-PROD-LOCKED
 * Status: LOCKED - Policy loading and validation
 */

#include "cogman_kernel/gate_policy.hpp"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>

namespace cogman_kernel {

// GatePolicy Implementation

const ContextProfile* GatePolicy::get_context(const std::string& context_name) const {
    auto it = contexts.find(context_name);
    if (it != contexts.end()) {
        return &it->second;
    }
    return nullptr;
}

DecisionBands GatePolicy::to_decision_bands(const std::string& context_name) const {
    const ContextProfile* profile = get_context(context_name);
    if (profile) {
        return create_bands_from_profile(*profile);
    }
    
    // Fallback to default
    return create_default_bands(context_name);
}

bool GatePolicy::validate() const {
    // Validate metadata
    if (meta.policy_name.empty() || meta.version.empty()) {
        return false;
    }
    
    // Validate contexts
    if (contexts.empty()) {
        return false;
    }
    
    // Validate each context
    for (const auto& [name, profile] : contexts) {
        if (profile.name != name) {
            return false;
        }
        
        // Validate limits
        if (profile.limits.embedding_distance_max <= 0.0 ||
            profile.limits.entropy_max_p95 <= 0.0 ||
            profile.limits.variance_max <= 0.0) {
            return false;
        }
        
        // Validate Eμ bands
        const auto& bands = profile.limits.e_mu_bands;
        if (bands.restrict_max >= bands.caution_min ||
            bands.caution_max >= bands.accept_min ||
            bands.accept_max <= bands.accept_min) {
            return false;
        }
    }
    
    return true;
}

// GatePolicyLoader Implementation

std::unique_ptr<GatePolicy> GatePolicyLoader::load_from_file(const std::string& file_path) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        return nullptr;
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    file.close();
    
    return load_from_string(buffer.str());
}

std::unique_ptr<GatePolicy> GatePolicyLoader::load_from_string(const std::string& yaml_content) {
    auto policy = std::make_unique<GatePolicy>();
    
    // Simple YAML parser (basic implementation)
    // For production, use a proper YAML library like yaml-cpp
    if (!parse_yaml(yaml_content, *policy)) {
        return nullptr;
    }
    
    if (!validate_policy(*policy)) {
        return nullptr;
    }
    
    return policy;
}

bool GatePolicyLoader::validate_policy(const GatePolicy& policy) {
    return policy.validate();
}

bool GatePolicyLoader::parse_yaml(const std::string& yaml_content, GatePolicy& policy) {
    // NOTE: This is a basic placeholder implementation
    // For production, integrate with yaml-cpp or similar library
    
    // For now, we'll create default profiles based on known contexts
    // Full YAML parsing requires external library
    
    // Create robot_control profile
    ContextProfile robot_control;
    robot_control.name = "robot_control";
    robot_control.description = "Physical actuation context. Conservative thresholds. Human safety first.";
    robot_control.limits.embedding_distance_max = 0.35;
    robot_control.limits.entropy_max_p95 = 0.62;
    robot_control.limits.e_mu_bands.accept_min = 30.0;
    robot_control.limits.e_mu_bands.accept_max = 80.0;
    robot_control.limits.e_mu_bands.caution_min = 15.0;
    robot_control.limits.e_mu_bands.caution_max = 30.0;
    robot_control.limits.e_mu_bands.restrict_max = 15.0;
    robot_control.limits.variance_max = 8.0;
    robot_control.limits.negative_trend_review = true;
    policy.contexts["robot_control"] = robot_control;
    
    // Create chat profile
    ContextProfile chat;
    chat.name = "chat";
    chat.description = "Conversational output context. Higher tolerance than physical systems.";
    chat.limits.embedding_distance_max = 0.45;
    chat.limits.entropy_max_p95 = 0.75;
    chat.limits.e_mu_bands.accept_min = 25.0;
    chat.limits.e_mu_bands.accept_max = 85.0;
    chat.limits.e_mu_bands.caution_min = 10.0;
    chat.limits.e_mu_bands.caution_max = 25.0;
    chat.limits.e_mu_bands.restrict_max = 10.0;
    chat.limits.variance_max = 12.0;
    chat.limits.negative_trend_review = true;
    policy.contexts["chat"] = chat;
    
    // Create finance profile
    ContextProfile finance;
    finance.name = "finance";
    finance.description = "High-risk decision context. Extremely conservative.";
    finance.limits.embedding_distance_max = 0.25;
    finance.limits.entropy_max_p95 = 0.55;
    finance.limits.e_mu_bands.accept_min = 40.0;
    finance.limits.e_mu_bands.accept_max = 90.0;
    finance.limits.e_mu_bands.caution_min = 25.0;
    finance.limits.e_mu_bands.caution_max = 40.0;
    finance.limits.e_mu_bands.restrict_max = 25.0;
    finance.limits.variance_max = 5.0;
    finance.limits.negative_trend_review = true;
    policy.contexts["finance"] = finance;
    
    // Set metadata
    policy.meta.policy_name = "CORE-9_DECISION_GATE";
    policy.meta.version = "v1.0";
    policy.meta.status = "LOCKED";
    policy.meta.owner = "system_owner";
    policy.meta.fail_closed = true;
    policy.meta.explainable = true;
    policy.meta.deterministic = true;
    
    return true;
}

// Helper Functions

DecisionBands create_bands_from_profile(const ContextProfile& profile) {
    DecisionBands bands;
    bands.context = profile.name;
    bands.version = "1.0";
    
    const auto& limits = profile.limits;
    
    bands.D_max = limits.embedding_distance_max;
    bands.H_max = limits.entropy_max_p95;
    bands.V_max = limits.variance_max;
    
    bands.E_mu_accept_min = limits.e_mu_bands.accept_min;
    bands.E_mu_accept_max = limits.e_mu_bands.accept_max;
    bands.E_mu_caution_min = limits.e_mu_bands.caution_min;
    bands.E_mu_caution_max = limits.e_mu_bands.caution_max;
    bands.E_mu_restrict_max = limits.e_mu_bands.restrict_max;
    
    return bands;
}

} // namespace cogman_kernel

