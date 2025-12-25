/**
 * Gate Policy Loader
 * 
 * Version: v1.0-PROD-LOCKED
 * Status: LOCKED - Policy loading and validation
 * 
 * Loads and validates GATE_POLICY.yaml configuration
 */

#ifndef COGMAN_KERNEL_GATE_POLICY_HPP
#define COGMAN_KERNEL_GATE_POLICY_HPP

#include "cogman_kernel/core9_gate.hpp"
#include <string>
#include <map>
#include <vector>
#include <memory>

namespace cogman_kernel {

/**
 * Policy Metadata
 */
struct PolicyMetadata {
    std::string policy_name = "CORE-9_DECISION_GATE";
    std::string version = "v1.0";
    std::string status = "LOCKED";
    std::string owner = "system_owner";
    std::vector<std::string> decision_modes = {"ALLOW", "REVIEW", "BLOCK"};
    bool fail_closed = true;
    bool explainable = true;
    bool deterministic = true;
};

/**
 * Eμ Bands Structure
 */
struct EMuBands {
    double accept_min = 30.0;
    double accept_max = 80.0;
    double caution_min = 15.0;
    double caution_max = 30.0;
    double restrict_max = 15.0;  // (-inf, restrict_max)
};

/**
 * Context Limits
 */
struct ContextLimits {
    double embedding_distance_max = 0.35;
    double entropy_max_p95 = 0.62;
    EMuBands e_mu_bands;
    double variance_max = 8.0;
    bool negative_trend_review = true;
};

/**
 * Context Profile
 */
struct ContextProfile {
    std::string name;
    std::string description;
    ContextLimits limits;
};

/**
 * Gate Policy
 */
struct GatePolicy {
    PolicyMetadata meta;
    std::map<std::string, ContextProfile> contexts;
    
    /**
     * Get context profile by name
     */
    const ContextProfile* get_context(const std::string& context_name) const;
    
    /**
     * Convert context profile to DecisionBands
     */
    DecisionBands to_decision_bands(const std::string& context_name) const;
    
    /**
     * Validate policy
     */
    bool validate() const;
};

/**
 * Policy Loader
 */
class GatePolicyLoader {
public:
    /**
     * Load policy from YAML file
     * 
     * @param file_path Path to GATE_POLICY.yaml
     * @return GatePolicy or nullptr on error
     */
    static std::unique_ptr<GatePolicy> load_from_file(const std::string& file_path);
    
    /**
     * Load policy from YAML string
     * 
     * @param yaml_content YAML content as string
     * @return GatePolicy or nullptr on error
     */
    static std::unique_ptr<GatePolicy> load_from_string(const std::string& yaml_content);
    
    /**
     * Validate policy structure
     */
    static bool validate_policy(const GatePolicy& policy);
    
private:
    // YAML parsing helpers (implementation depends on YAML library)
    static bool parse_yaml(const std::string& yaml_content, GatePolicy& policy);
};

/**
 * Helper: Create DecisionBands from ContextProfile
 */
DecisionBands create_bands_from_profile(const ContextProfile& profile);

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_GATE_POLICY_HPP

