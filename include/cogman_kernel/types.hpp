/**
 * Cogman Kernel - Core Types
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Core types must not be modified without review
 */

#ifndef COGMAN_KERNEL_TYPES_HPP
#define COGMAN_KERNEL_TYPES_HPP

namespace cogman_kernel {

enum class DecisionVerdict {
    ALLOW,
    REVIEW,
    BLOCK
};

inline const char* decision_verdict_to_string(DecisionVerdict verdict) {
    switch (verdict) {
        case DecisionVerdict::ALLOW: return "ALLOW";
        case DecisionVerdict::REVIEW: return "REVIEW";
        case DecisionVerdict::BLOCK: return "BLOCK";
        default: return "UNKNOWN";
    }
}

struct NeuralComponents {
    double dopamine = 0.0;
    double serotonin = 0.0;
    double oxytocin = 0.0;
    double adrenaline = 0.0;
    double cortisol = 0.0;
};

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_TYPES_HPP

