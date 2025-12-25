/**
 * Cogman Kernel - Energy Bounds Tests
 * 
 * Version: v2.0-LOCKED
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include <cassert>
#include <cmath>

using namespace cogman_kernel;

int main() {
    // Test bounds validation
    EPS8State state;
    state.I = 0.8;
    state.P = 0.6;
    state.S = 0.7;
    state.H = 0.3;
    state.A = 0.5;
    state.S_a = 0.6;
    
    assert(state.validate());
    
    // Test invalid bounds
    state.H = 1.5; // Invalid
    assert(!state.validate());
    
    return 0;
}

