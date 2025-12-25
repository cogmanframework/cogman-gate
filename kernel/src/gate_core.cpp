/**
 * Cogman Kernel - Gate Core (G_decision logic - NO MEANING)
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Gate logic must not be modified without review
 * 
 * IMPORTANT: This is a deterministic gate with NO MEANING.
 * It is a pure engineering decision based on thresholds and rules.
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/cognitive_decision_gate.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <iomanip>

namespace cogman_kernel {

// CognitiveDecisionGate Implementation

CognitiveDecisionGate::CognitiveDecisionGate(const std::string& owner_profile_name)
    : owner_profile_name_(owner_profile_name) {
    // Initialize with default thresholds
}

DecisionResult CognitiveDecisionGate::evaluate_snapshot(const Snapshot& snapshot) {
        DecisionResult result;
        result.snapshot_summary = snapshot;
        result.standard_profile = owner_profile_name_;

        const double I = snapshot.I;
        const double P = snapshot.P;
        const double S = snapshot.S;
        const double H = snapshot.H;
        const double T = snapshot.T_psi;
        const double deltaE = snapshot.delta_E_psi;
        const double E_total = snapshot.E_total;

        int severity = 0;  // 0 = ปลอดภัย, 1 = review, 2 = block
        const auto& th = thresholds_;

        // 1) เช็ค H (entropy)
        if (H > th.H_max_review) {
            severity = std::max(severity, 2);
            result.reasons.push_back(format_reason("H", H, ">", "H_max_review", th.H_max_review, 
                                                   "uncertainty too high"));
        } else if (H > th.H_max_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("H", H, ">", "H_max_allow", th.H_max_allow, 
                                                   "uncertainty needs review"));
        }

        // 2) เช็ค S (stability)
        if (S < th.S_min_review) {
            severity = std::max(severity, 2);
            result.reasons.push_back(format_reason("S", S, "<", "S_min_review", th.S_min_review, 
                                                   "stability too low"));
        } else if (S < th.S_min_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("S", S, "<", "S_min_allow", th.S_min_allow, 
                                                   "low stability"));
        }

        // 3) เช็ค P (polarity)
        if (P < th.P_min_review) {
            severity = std::max(severity, 2);
            result.reasons.push_back(format_reason("P", P, "<", "P_min_review", th.P_min_review, 
                                                   "too negative"));
        } else if (P < th.P_min_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("P", P, "<", "P_min_allow", th.P_min_allow, 
                                                   "negative tone, review"));
        } else if (P > th.P_max_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("P", P, ">", "P_max_allow", th.P_max_allow, 
                                                   "over-positive, check bias"));
        }

        // 4) Emotional temperature TΨ
        if (T > th.T_max_review) {
            severity = std::max(severity, 2);
            result.reasons.push_back(format_reason("TΨ", T, ">", "T_max_review", th.T_max_review, 
                                                   "overheated state"));
        } else if (T > th.T_max_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("TΨ", T, ">", "T_max_allow", th.T_max_allow, 
                                                   "high emotional temperature"));
        }

        // 5) การเปลี่ยนแปลงพลังงาน ΔEΨ
        const double abs_deltaE = std::abs(deltaE);
        if (abs_deltaE > th.DeltaE_abs_max_review) {
            severity = std::max(severity, 2);
            result.reasons.push_back(format_reason("|ΔEΨ|", abs_deltaE, ">", 
                                                   "ΔE_abs_max_review", th.DeltaE_abs_max_review, 
                                                   ""));
        } else if (abs_deltaE > th.DeltaE_abs_max_allow) {
            severity = std::max(severity, 1);
            result.reasons.push_back(format_reason("|ΔEΨ|", abs_deltaE, ">", 
                                                   "ΔE_abs_max_allow", th.DeltaE_abs_max_allow, 
                                                   ""));
        }

        // === ตัดสินใจรวม ===
        result.severity = severity;
        if (severity == 2) {
            result.decision = DecisionStatus::BLOCK;
        } else if (severity == 1) {
            result.decision = DecisionStatus::REVIEW;
        } else {
            result.decision = DecisionStatus::ALLOW;
            result.reasons.push_back("All metrics within engineering safety bounds.");
        }

        return result;
    }

EngineeringThresholds& CognitiveDecisionGate::get_thresholds() {
    return thresholds_;
}

const EngineeringThresholds& CognitiveDecisionGate::get_thresholds() const {
    return thresholds_;
}

const std::string& CognitiveDecisionGate::get_owner_profile_name() const {
    return owner_profile_name_;
}

std::string CognitiveDecisionGate::format_reason(const std::string& var_name, double value, 
                                                  const std::string& op, const std::string& threshold_name, 
                                                  double threshold_value, const std::string& comment) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(3);
        oss << var_name << "=" << value << " " << op << " " 
            << threshold_name << "=" << threshold_value;
        if (!comment.empty()) {
            oss << " (" << comment << ")";
        }
        return oss.str();
}

/**
 * Gate core logic (CORE-9) - Legacy function for backward compatibility
 * 
 * This is a deterministic gate with NO MEANING.
 * It is a pure engineering decision based on thresholds and rules.
 */
DecisionVerdict gate_core(const DecisionParams& params, double H_current, double D_traj_current) {
    return decision_gate(params, H_current, D_traj_current);
}

DecisionVerdict to_decision_verdict(DecisionStatus status) {
    switch (status) {
        case DecisionStatus::ALLOW:
            return DecisionVerdict::ALLOW;
        case DecisionStatus::REVIEW:
            return DecisionVerdict::REVIEW;
        case DecisionStatus::BLOCK:
            return DecisionVerdict::BLOCK;
        default:
            return DecisionVerdict::ALLOW;
    }
}

const char* decision_status_to_string(DecisionStatus status) {
    switch (status) {
        case DecisionStatus::ALLOW:
            return "ALLOW";
        case DecisionStatus::REVIEW:
            return "REVIEW";
        case DecisionStatus::BLOCK:
            return "BLOCK";
        default:
            return "UNKNOWN";
    }
}

} // namespace cogman_kernel

