/**
 * Cogman Kernel - Determinism Tests
 * 
 * Version: v2.0-LOCKED
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include <cassert>
#include <cmath>

using namespace cogman_kernel;

int main() {
    // Test determinism: same inputs → same outputs
    double result1 = energy_of_perception(0.8, 0.6, 0.7, 0.3, true);
    double result2 = energy_of_perception(0.8, 0.6, 0.7, 0.3, true);
    
    assert(std::abs(result1 - result2) < 1e-10);
    
    return 0;
}

