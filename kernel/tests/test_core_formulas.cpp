/**
 * Cogman Kernel - Core Formulas Tests
 * 
 * Version: v2.0-LOCKED
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include <cassert>
#include <cmath>

using namespace cogman_kernel;

int main() {
    // Test CORE-1: Energy of Perception
    {
        double result = energy_of_perception(0.8, 0.6, 0.7, 0.3, true);
        assert(result >= 0.0);
    }
    
    // Test CORE-2: Reflex Energy
    {
        double delta_E_psi = 0.5;
        double result = reflex_energy(delta_E_psi, 0.6);
        assert(result >= 0.0);
    }
    
    // Test CORE-9: Decision Gate
    {
        DecisionParams params;
        params.rule_fail = false;
        params.H_threshold = 0.85;
        params.D_traj_threshold = 0.7;
        
        DecisionVerdict verdict = decision_gate(params, 0.5, 0.3);
        assert(verdict == DecisionVerdict::ALLOW);
    }
    
    return 0;
}

