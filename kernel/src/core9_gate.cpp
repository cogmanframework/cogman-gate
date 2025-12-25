/**
 * 🔒 CORE-9 — Decision Gate Implementation
 * 
 * Version: v1.0-PROD-LOCKED
 * Status: LOCKED (Deterministic / Explainable / Fail-Closed)
 */

#include "cogman_kernel/core9_gate.hpp"
#include "cogman_kernel/errors.hpp"
#include <sstream>
#include <iomanip>
#include <numeric>
#include <algorithm>
#include <cmath>

namespace cogman_kernel {

// Core9DecisionGate Implementation

Core9DecisionGate::Core9DecisionGate(const DecisionBands& bands)
    : bands_(bands) {
}

DecisionResult Core9DecisionGate::evaluate(const DecisionInput& input) {
    // Validate input metrics
    check_nan("metrics.E_mu", input.metrics.E_mu);
    check_nan("metrics.H", input.metrics.H);
    check_nan("metrics.D", input.metrics.D);
    check_nan("metrics.S", input.metrics.S);
    check_nan("metrics.T", input.metrics.T);
    check_nan("metrics.V", input.metrics.V);
    
    check_infinity("metrics.E_mu", input.metrics.E_mu);
    check_infinity("metrics.H", input.metrics.H);
    check_infinity("metrics.D", input.metrics.D);
    check_infinity("metrics.S", input.metrics.S);
    check_infinity("metrics.T", input.metrics.T);
    check_infinity("metrics.V", input.metrics.V);
    
    // Validate ranges
    check_range("metrics.H", input.metrics.H, 0.0, 1.0);
    check_range("metrics.D", input.metrics.D, 0.0, 1.0);
    check_range("metrics.S", input.metrics.S, 0.0, 1.0);
    check_range_min("metrics.E_mu", input.metrics.E_mu, 0.0);  // E_mu typically non-negative
    
    // Validate bands
    if (bands_.D_max < 0.0 || bands_.H_max < 0.0 || bands_.V_max < 0.0) {
        throw GateException(ErrorCode::GATE_INVALID_BANDS,
                           "Decision bands contain invalid negative values");
    }
    
    if (bands_.E_mu_restrict_max >= bands_.E_mu_caution_min ||
        bands_.E_mu_caution_max >= bands_.E_mu_accept_min ||
        bands_.E_mu_accept_max <= bands_.E_mu_accept_min) {
        throw GateException(ErrorCode::GATE_INVALID_BANDS,
                           "Eμ bands are not properly ordered (restrict < caution < accept)");
    }
    
    DecisionResult result;
    result.metrics = input.metrics;
    result.context = input.context;
    result.protocol = "CORE9_v1.0";
    
    const auto& m = input.metrics;
    const auto& b = bands_;
    
    // Validate Eμ history if provided
    if (!input.E_mu_history.empty()) {
        for (size_t i = 0; i < input.E_mu_history.size(); ++i) {
            check_nan("E_mu_history[" + std::to_string(i) + "]", input.E_mu_history[i]);
            check_infinity("E_mu_history[" + std::to_string(i) + "]", input.E_mu_history[i]);
            check_range_min("E_mu_history[" + std::to_string(i) + "]", input.E_mu_history[i], 0.0);
        }
    }
    
    // Calculate T and V from history if available
    double T = m.T;
    double V = m.V;
    
    if (!input.E_mu_history.empty() && input.E_mu_history.size() >= 2) {
        T = calculate_trend(input.E_mu_history);
        V = calculate_variance(input.E_mu_history);
        
        // Validate computed T and V
        check_nan("computed_T", T);
        check_nan("computed_V", V);
        check_infinity("computed_T", T);
        check_infinity("computed_V", V);
        
        result.metrics.T = T;
        result.metrics.V = V;
    }
    
    // Decision Logic (ห้ามแก้ลำดับ)
    
    // 1) IF S == 0 → BLOCK
    if (m.S == 0.0) {
        result.verdict = DecisionVerdict::BLOCK;
        result.rule_fail = true;
        result.reasons.push_back("Safety rule failed (S == 0)");
        return result;
    }
    
    // 2) ELIF Eμ ∈ Restrict → BLOCK
    if (is_E_mu_restrict(m.E_mu, b)) {
        result.verdict = DecisionVerdict::BLOCK;
        result.reasons.push_back(
            format_E_mu_reason("Eμ", m.E_mu, "restrict", b.E_mu_restrict_max)
        );
        return result;
    }
    
    // 3) ELIF H > H_max → REVIEW
    if (m.H > b.H_max) {
        result.verdict = DecisionVerdict::REVIEW;
        result.reasons.push_back(
            format_reason("H", m.H, ">", "H_max", b.H_max, "entropy above threshold")
        );
        return result;
    }
    
    // 4) ELIF D > D_max → REVIEW
    if (m.D > b.D_max) {
        result.verdict = DecisionVerdict::REVIEW;
        result.reasons.push_back(
            format_reason("D", m.D, ">", "D_max", b.D_max, "semantic drift above threshold")
        );
        return result;
    }
    
    // 5) ELIF V > V_max → REVIEW
    if (V > b.V_max) {
        result.verdict = DecisionVerdict::REVIEW;
        result.reasons.push_back(
            format_reason("V", V, ">", "V_max", b.V_max, "variance above threshold")
        );
        return result;
    }
    
    // 6) ELIF T < 0 AND Eμ ∈ Caution → REVIEW
    if (T < 0.0 && is_E_mu_caution(m.E_mu, b)) {
        result.verdict = DecisionVerdict::REVIEW;
        result.reasons.push_back(
            "Negative trend (T < 0) AND Eμ in caution range"
        );
        return result;
    }
    
    // 7) ELSE → ALLOW
    result.verdict = DecisionVerdict::ALLOW;
    result.reasons.push_back("All metrics within safety bounds");
    
    return result;
}

bool Core9DecisionGate::is_E_mu_restrict(double E_mu, const DecisionBands& bands) {
    return E_mu < bands.E_mu_restrict_max;
}

bool Core9DecisionGate::is_E_mu_caution(double E_mu, const DecisionBands& bands) {
    return E_mu >= bands.E_mu_caution_min && E_mu < bands.E_mu_caution_max;
}

bool Core9DecisionGate::is_E_mu_accept(double E_mu, const DecisionBands& bands) {
    return E_mu >= bands.E_mu_accept_min && E_mu <= bands.E_mu_accept_max;
}

double Core9DecisionGate::calculate_trend(const std::vector<double>& history) const {
    if (history.size() < 2) return 0.0;
    
    // Simple linear trend: (last - first) / (size - 1)
    return (history.back() - history.front()) / (history.size() - 1);
}

double Core9DecisionGate::calculate_variance(const std::vector<double>& history) const {
    if (history.size() < 2) return 0.0;
    
    // Calculate mean
    double mean = std::accumulate(history.begin(), history.end(), 0.0) / history.size();
    
    // Calculate variance
    double variance = 0.0;
    for (double value : history) {
        double diff = value - mean;
        variance += diff * diff;
    }
    return variance / history.size();
}

// Helper functions (static, used internally)
std::string Core9DecisionGate::format_reason(const std::string& var_name, double value,
                                             const std::string& op, const std::string& threshold_name,
                                             double threshold_value, const std::string& comment) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(3);
    oss << var_name << "=" << value << " " << op << " " << threshold_name << "=" << threshold_value;
    if (!comment.empty()) {
        oss << " (" << comment << ")";
    }
    return oss.str();
}

std::string Core9DecisionGate::format_E_mu_reason(const std::string& var_name, double value,
                                                   const std::string& band, double threshold) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(3);
    oss << var_name << "=" << value << " in " << band << " range (< " << threshold << ")";
    return oss.str();
}

// DecisionResult Implementation

std::string DecisionResult::to_explainable_record() const {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(3);
    
    oss << "{\n";
    oss << "  \"verdict\": \"" << decision_verdict_to_string(verdict) << "\",\n";
    oss << "  \"metrics\": {\n";
    oss << "    \"Eμ\": " << metrics.E_mu << ",\n";
    oss << "    \"H\": " << metrics.H << ",\n";
    oss << "    \"D\": " << metrics.D << ",\n";
    oss << "    \"S\": " << metrics.S << ",\n";
    oss << "    \"T\": " << metrics.T << ",\n";
    oss << "    \"V\": " << metrics.V << "\n";
    oss << "  },\n";
    oss << "  \"rules\": " << (rule_fail ? "[\"failed\"]" : "[\"ok\"]") << ",\n";
    oss << "  \"reason\": \"" << (reasons.empty() ? "N/A" : reasons[0]) << "\",\n";
    oss << "  \"protocol\": \"" << protocol << "\",\n";
    oss << "  \"context\": \"" << context << "\"\n";
    oss << "}";
    
    return oss.str();
}

// Helper Functions

DecisionBands create_default_bands(const std::string& context) {
    DecisionBands bands;
    bands.context = context;
    bands.version = "1.0";
    // Default values from spec
    bands.D_max = 0.35;
    bands.H_max = 0.62;
    bands.V_max = 8.0;
    bands.E_mu_accept_min = 30.0;
    bands.E_mu_accept_max = 80.0;
    bands.E_mu_caution_min = 15.0;
    bands.E_mu_caution_max = 30.0;
    bands.E_mu_restrict_max = 15.0;
    return bands;
}

DecisionBands create_robot_control_bands() {
    DecisionBands bands = create_default_bands("robot_control");
    // Robot control specific: stricter
    bands.D_max = 0.30;
    bands.H_max = 0.60;
    bands.V_max = 6.0;
    return bands;
}

DecisionBands create_chat_bands() {
    DecisionBands bands = create_default_bands("chat");
    // Chat specific: more permissive
    bands.D_max = 0.40;
    bands.H_max = 0.70;
    bands.V_max = 10.0;
    return bands;
}

DecisionBands create_finance_bands() {
    DecisionBands bands = create_default_bands("finance");
    // Finance specific: very strict
    bands.D_max = 0.25;
    bands.H_max = 0.55;
    bands.V_max = 5.0;
    return bands;
}

} // namespace cogman_kernel

