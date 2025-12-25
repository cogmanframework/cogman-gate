/**
 * 🔒 CORE-9 — Decision Gate (Judge)
 * 
 * Version: v1.0-PROD-LOCKED
 * Status: LOCKED (Deterministic / Explainable / Fail-Closed)
 * 
 * Purpose: อนุญาต / จำกัด / บล็อก ผลลัพธ์หรือคำสั่งของระบบ ก่อน ออกสู่โลกจริง
 * 
 * หลักการบังคับ:
 *   • Deterministic (ผลเหมือนเดิมทุกครั้ง)
 *   • Explainable (อธิบายได้ทุก verdict)
 *   • Fail-Closed (ไม่แน่ใจ = ไม่ปล่อย)
 * 
 * ❌ ไม่เรียนรู้
 * ❌ ไม่ปรับตัวเอง
 * ❌ ไม่ตีความความหมาย
 */

#ifndef COGMAN_KERNEL_CORE9_GATE_HPP
#define COGMAN_KERNEL_CORE9_GATE_HPP

#include "cogman_kernel/types.hpp"
#include <string>
#include <vector>
#include <map>
#include <limits>

namespace cogman_kernel {

/**
 * Core Metrics (สูตรที่อนุญาตให้ใช้)
 */
struct CoreMetrics {
    double E_mu = 0.0;        // Internal readiness / stress index
    double H = 0.0;          // Output entropy (risk / uncertainty) [0, 1]
    double D = 0.0;          // distance(Ein, Eout) - semantic drift (cosine only) [0, 1]
    double S = 1.0;          // safety_rule_score ∈ {0,1} - hard constraint
    double T = 0.0;          // trend(Eμ, window=k) - readiness trend
    double V = 0.0;          // variance(Eμ, window=k) - stability
};

/**
 * Decision Bands (Context-Locked)
 * 
 * ตัวอย่าง robot_control:
 *   D_max: 0.35
 *   H_max_p95: 0.62
 *   Eμ_accept:   [30, 80]
 *   Eμ_caution:  [15, 30)
 *   Eμ_restrict: (-inf, 15)
 *   V_max: 8.0
 */
struct DecisionBands {
    double D_max = 0.35;              // Maximum semantic drift
    double H_max = 0.62;              // Maximum entropy (percentile-based)
    double V_max = 8.0;               // Maximum variance
    
    // Eμ bands
    double E_mu_accept_min = 30.0;
    double E_mu_accept_max = 80.0;
    double E_mu_caution_min = 15.0;
    double E_mu_caution_max = 30.0;
    double E_mu_restrict_max = 15.0;  // (-inf, E_mu_restrict_max)
    
    std::string context = "default";   // robot_control / chat / finance / etc.
    std::string version = "1.0";      // versioned + immutable
};

/**
 * Decision Input (ต้องมีครบ)
 */
struct DecisionInput {
    CoreMetrics metrics;
    DecisionBands bands;
    
    // Optional: for audit/tuning
    std::vector<double> E_mu_history;  // History window for T and V calculation
    std::string context = "default";
};

/**
 * Decision Result (Explainable - บังคับ)
 * 
 * ทุก verdict ต้องมี record เดียวอธิบายได้ครบ
 */
struct DecisionResult {
    DecisionVerdict verdict = DecisionVerdict::ALLOW;
    
    // Metrics used in decision
    CoreMetrics metrics;
    
    // Rules status
    bool rule_fail = false;  // S == 0
    
    // Detailed reasons
    std::vector<std::string> reasons;
    
    // Protocol version
    std::string protocol = "CORE9_v1.0";
    
    // Context
    std::string context = "default";
    
    /**
     * Get explainable record (JSON-like structure)
     */
    std::string to_explainable_record() const;
};

/**
 * 🔒 CORE-9 Decision Gate Class
 * 
 * Decision Logic (ห้ามแก้ลำดับ):
 *   IF S == 0                     → BLOCK
 *   ELIF Eμ ∈ Restrict            → BLOCK
 *   ELIF H > H_max                → REVIEW
 *   ELIF D > D_max                → REVIEW
 *   ELIF V > V_max                → REVIEW
 *   ELIF T < 0 AND Eμ ∈ Caution   → REVIEW
 *   ELSE                          → ALLOW
 */
class Core9DecisionGate {
public:
    /**
     * Constructor with context-specific bands
     */
    explicit Core9DecisionGate(const DecisionBands& bands);
    
    /**
     * Evaluate decision (CORE-9)
     * 
     * @param input Decision input with metrics and bands
     * @return DecisionResult with verdict and explainable record
     */
    DecisionResult evaluate(const DecisionInput& input);
    
    /**
     * Get current bands
     */
    const DecisionBands& get_bands() const { return bands_; }
    
    /**
     * Check if Eμ is in restrict range
     */
    static bool is_E_mu_restrict(double E_mu, const DecisionBands& bands);
    
    /**
     * Check if Eμ is in caution range
     */
    static bool is_E_mu_caution(double E_mu, const DecisionBands& bands);
    
    /**
     * Check if Eμ is in accept range
     */
    static bool is_E_mu_accept(double E_mu, const DecisionBands& bands);

private:
    DecisionBands bands_;
    
    /**
     * Calculate trend from history
     */
    double calculate_trend(const std::vector<double>& history) const;
    
    /**
     * Calculate variance from history
     */
    double calculate_variance(const std::vector<double>& history) const;
    
    /**
     * Format reason string (internal helper)
     */
    static std::string format_reason(const std::string& var_name, double value,
                                     const std::string& op, const std::string& threshold_name,
                                     double threshold_value, const std::string& comment);
    
    /**
     * Format Eμ reason string (internal helper)
     */
    static std::string format_E_mu_reason(const std::string& var_name, double value,
                                           const std::string& band, double threshold);
};

/**
 * Helper: Create default bands for context
 */
DecisionBands create_default_bands(const std::string& context);

/**
 * Helper: Create robot_control bands
 */
DecisionBands create_robot_control_bands();

/**
 * Helper: Create chat bands
 */
DecisionBands create_chat_bands();

/**
 * Helper: Create finance bands
 */
DecisionBands create_finance_bands();

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_CORE9_GATE_HPP

