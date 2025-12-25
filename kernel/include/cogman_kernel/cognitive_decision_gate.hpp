/**
 * Cogman Kernel - Cognitive Decision Gate
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Gate logic must not be modified without review
 * 
 * Decision Gate สำหรับ Cognitive-Emotional Physics Engine
 * เกณฑ์ทั้งหมดเป็น "มาตรฐานวิศวกรรม" ที่เจ้าของระบบกำหนด
 * ไม่ใช่มาตรฐานการแพทย์/คลินิก
 */

#ifndef COGMAN_KERNEL_COGNITIVE_DECISION_GATE_HPP
#define COGMAN_KERNEL_COGNITIVE_DECISION_GATE_HPP

#include "cogman_kernel/types.hpp"
#include <string>
#include <vector>

namespace cogman_kernel {

/**
 * Decision Status (matches Python enum)
 */
enum class DecisionStatus {
    ALLOW,
    REVIEW,
    BLOCK
};

/**
 * Engineering Thresholds Structure
 */
struct EngineeringThresholds {
    // ความไม่แน่นอนสูงสุดที่ยอมให้พูดออกมา
    double H_max_allow = 0.65;
    double H_max_review = 0.8;

    // ความเสถียรขั้นต่ำ
    double S_min_allow = 0.5;
    double S_min_review = 0.35;

    // ขอบเขต polarity
    double P_min_allow = -0.4;
    double P_min_review = -0.7;
    double P_max_allow = 1.0;  // บวกจัดได้ แต่จะไปดูร่วมกับ TΨ

    // Emotional temperature
    double T_max_allow = 0.6;
    double T_max_review = 0.85;

    // การเปลี่ยนแปลงพลังงาน
    double DeltaE_abs_max_allow = 0.7;
    double DeltaE_abs_max_review = 1.2;
};

/**
 * Snapshot Structure (input to gate)
 */
struct Snapshot {
    double I = 0.0;
    double P = 0.0;
    double S = 0.0;
    double H = 0.0;
    double T_psi = 0.0;      // TΨ
    double delta_E_psi = 0.0;  // ΔEΨ
    double E_total = 0.0;
};

/**
 * Decision Result Structure
 */
struct DecisionResult {
    DecisionStatus decision = DecisionStatus::ALLOW;
    int severity = 0;  // 0 = ปลอดภัย, 1 = review, 2 = block
    std::vector<std::string> reasons;
    Snapshot snapshot_summary;
    std::string standard_profile = "OWNER_STANDARD_V1";
    std::string note = "This decision is based on ENGINEERING SIMULATION thresholds, "
                       "not clinical diagnosis. Clinical use requires licensed experts.";
};

/**
 * Cognitive Decision Gate Class
 */
class CognitiveDecisionGate {
public:
    explicit CognitiveDecisionGate(const std::string& owner_profile_name = "OWNER_STANDARD_V1");

    /**
     * Evaluate snapshot and return decision
     * 
     * Input: snapshot from engine.get_full_snapshot()
     * Output: DecisionResult with decision + engineering reasons
     */
    DecisionResult evaluate_snapshot(const Snapshot& snapshot);

    /**
     * Get thresholds (for inspection/modification)
     */
    EngineeringThresholds& get_thresholds();
    const EngineeringThresholds& get_thresholds() const;

    /**
     * Get owner profile name
     */
    const std::string& get_owner_profile_name() const;

private:
    std::string owner_profile_name_;
    EngineeringThresholds thresholds_;

    /**
     * Format reason string
     */
    std::string format_reason(const std::string& var_name, double value, 
                              const std::string& op, const std::string& threshold_name, 
                              double threshold_value, const std::string& comment);
};

/**
 * Convert DecisionStatus to DecisionVerdict
 */
DecisionVerdict to_decision_verdict(DecisionStatus status);

/**
 * Convert DecisionStatus to string
 */
const char* decision_status_to_string(DecisionStatus status);

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_COGNITIVE_DECISION_GATE_HPP

