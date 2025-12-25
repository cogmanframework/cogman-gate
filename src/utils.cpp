/**
 * Cogman Kernel - Utility Functions
 * 
 * Version: v2.0-LOCKED
 */

#include "cogman_kernel/eps8.hpp"
#include <algorithm>
#include <cmath>

namespace cogman_kernel {

bool EPS8State::validate() const {
    // Check for NaN
    if (std::isnan(I) || std::isnan(P) || std::isnan(S) || std::isnan(H) ||
        std::isnan(F) || std::isnan(A) || std::isnan(S_a) || std::isnan(theta)) {
        return false;
    }
    
    // Check for infinity
    if (std::isinf(I) || std::isinf(P) || std::isinf(S) || std::isinf(H) ||
        std::isinf(F) || std::isinf(A) || std::isinf(S_a) || std::isinf(theta)) {
        return false;
    }
    
    // Range validation
    // I >= 0
    if (I < 0.0) {
        return false;
    }
    
    // S ∈ [0, 1]
    if (S < 0.0 || S > 1.0) {
        return false;
    }
    
    // H ∈ [0, 1]
    if (H < 0.0 || H > 1.0) {
        return false;
    }
    
    // A ∈ [0, 1]
    if (A < 0.0 || A > 1.0) {
        return false;
    }
    
    // S_a ∈ [0, 1]
    if (S_a < 0.0 || S_a > 1.0) {
        return false;
    }
    
    // P, F, theta can be any real number (no range check)
    
    return true;
}

} // namespace cogman_kernel

