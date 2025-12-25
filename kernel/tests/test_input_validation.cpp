/**
 * Input Validation Tests
 * 
 * Tests comprehensive input validation for all core formulas
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/errors.hpp"
#include "cogman_kernel/eps8.hpp"
#include "cogman_kernel/types.hpp"
#include <iostream>
#include <cmath>
#include <limits>
#include <cassert>

using namespace cogman_kernel;

void test_core1_validation() {
    std::cout << "Testing CORE-1 (Energy of Perception) validation..." << std::endl;
    
    // Test NaN
    try {
        energy_of_perception(std::nan(""), 0.6, 0.6, 0.3, true);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test infinity
    try {
        energy_of_perception(std::numeric_limits<double>::infinity(), 0.6, 0.6, 0.3, true);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ Infinity detection works" << std::endl;
    }
    
    // Test invalid range (H > 1.0)
    try {
        energy_of_perception(0.8, 0.6, 0.6, 1.5, true);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
    
    // Test valid input
    try {
        double result = energy_of_perception(0.8, 0.6, 0.6, 0.3, true);
        assert(!std::isnan(result) && !std::isinf(result));
        std::cout << "  ✓ Valid input works: " << result << std::endl;
    } catch (...) {
        assert(false && "Should not throw for valid input");
    }
}

void test_core2_validation() {
    std::cout << "\nTesting CORE-2 (Reflex Energy) validation..." << std::endl;
    
    // Test NaN
    try {
        reflex_energy(0.5, std::nan(""));
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test invalid range (A > 1.0)
    try {
        reflex_energy(0.5, 1.5);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
}

void test_core3_validation() {
    std::cout << "\nTesting CORE-3 (Directional Reflex Energy) validation..." << std::endl;
    
    // Test NaN
    try {
        directional_reflex_energy(std::nan(""), 1.5);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test extreme theta_phase
    try {
        directional_reflex_energy(0.5, 2000.0);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Extreme value detection works" << std::endl;
    }
}

void test_core4_validation() {
    std::cout << "\nTesting CORE-4 (Cognitive Energy) validation..." << std::endl;
    
    // Test invalid range
    try {
        cognitive_energy(0.8, 0.5, 1.5);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
}

void test_core5_validation() {
    std::cout << "\nTesting CORE-5 (Coherence Energy) validation..." << std::endl;
    
    // Test invalid range
    try {
        coherence_energy(1.5, 0.5, 0.3);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
}

void test_core6_validation() {
    std::cout << "\nTesting CORE-6 (Neural Energetic Sum) validation..." << std::endl;
    
    NeuralComponents neural;
    neural.dopamine = std::nan("");
    
    // Test NaN
    try {
        neural_energetic_sum(neural);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test extreme value
    neural.dopamine = 1e10;
    try {
        neural_energetic_sum(neural);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Extreme value detection works" << std::endl;
    }
}

void test_core7_validation() {
    std::cout << "\nTesting CORE-7 (Binding Energy) validation..." << std::endl;
    
    // Test NaN
    try {
        binding_energy(std::nan(""), 0.5, 0.3);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test extreme value
    try {
        binding_energy(1e15, 0.5, 0.3);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Extreme value detection works" << std::endl;
    }
}

void test_core8_validation() {
    std::cout << "\nTesting CORE-8 (Memory Encoding Energy) validation..." << std::endl;
    
    // Test invalid range (A > 1.0)
    try {
        memory_encoding_energy(1.5, 0.5, 0.3);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
}

void test_core9_validation() {
    std::cout << "\nTesting CORE-9 (Decision Gate) validation..." << std::endl;
    
    DecisionParams params;
    params.H_threshold = 0.85;
    params.D_traj_threshold = 0.7;
    
    // Test NaN
    try {
        decision_gate(params, std::nan(""), 0.5);
        assert(false && "Should have thrown exception");
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ NaN detection works" << std::endl;
    }
    
    // Test invalid range (H > 1.0)
    try {
        decision_gate(params, 1.5, 0.5);
        assert(false && "Should have thrown exception");
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Range validation works" << std::endl;
    }
}

void test_eps8_validation() {
    std::cout << "\nTesting EPS-8 State validation..." << std::endl;
    
    EPS8State state;
    state.I = 0.8;
    state.P = 0.6;
    state.S = 0.7;
    state.H = 0.3;
    state.A = 0.5;
    state.S_a = 0.6;
    state.theta = 1.5;
    
    assert(state.validate() == true);
    std::cout << "  ✓ Valid state passes" << std::endl;
    
    // Test invalid H
    state.H = 1.5;
    assert(state.validate() == false);
    std::cout << "  ✓ Invalid H detected" << std::endl;
    
    // Test NaN
    state.H = 0.3;
    state.I = std::nan("");
    assert(state.validate() == false);
    std::cout << "  ✓ NaN detection works" << std::endl;
}

int main() {
    std::cout << "=== Input Validation Tests ===" << std::endl;
    std::cout << std::endl;
    
    try {
        test_core1_validation();
        test_core2_validation();
        test_core3_validation();
        test_core4_validation();
        test_core5_validation();
        test_core6_validation();
        test_core7_validation();
        test_core8_validation();
        test_core9_validation();
        test_eps8_validation();
        
        std::cout << "\n=== All Validation Tests Passed ===" << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Test failed: " << e.what() << std::endl;
        return 1;
    }
}

