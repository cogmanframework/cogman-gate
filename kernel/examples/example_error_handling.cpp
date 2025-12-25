/**
 * Error Handling Example
 * 
 * Demonstrates error handling in Cogman Kernel
 */

#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/errors.hpp"
#include "cogman_kernel/eps8.hpp"
#include <iostream>
#include <iomanip>

using namespace cogman_kernel;

int main() {
    std::cout << "=== Error Handling Example ===" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    
    // Example 1: Invalid range
    std::cout << "\n1. Testing invalid range (H > 1.0):" << std::endl;
    try {
        double result = energy_of_perception(0.8, 0.6, 0.6, 1.5, true); // H = 1.5 (invalid)
        std::cout << "  Result: " << result << std::endl;
    } catch (const InvalidRangeException& e) {
        std::cout << "  ✓ Caught InvalidRangeException: " << e.what() << std::endl;
        std::cout << "  Error Code: " << e.code_string() << " (" << static_cast<int>(e.code()) << ")" << std::endl;
    }
    
    // Example 2: NaN detection
    std::cout << "\n2. Testing NaN detection:" << std::endl;
    try {
        double nan_val = std::nan("");
        double result = energy_of_perception(nan_val, 0.6, 0.6, 0.3, true);
        std::cout << "  Result: " << result << std::endl;
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ Caught InvalidInputException: " << e.what() << std::endl;
        std::cout << "  Error Code: " << e.code_string() << std::endl;
    }
    
    // Example 3: Infinity detection
    std::cout << "\n3. Testing infinity detection:" << std::endl;
    try {
        double inf_val = std::numeric_limits<double>::infinity();
        double result = energy_of_perception(inf_val, 0.6, 0.6, 0.3, true);
        std::cout << "  Result: " << result << std::endl;
    } catch (const InvalidInputException& e) {
        std::cout << "  ✓ Caught InvalidInputException: " << e.what() << std::endl;
        std::cout << "  Error Code: " << e.code_string() << std::endl;
    }
    
    // Example 4: Valid input
    std::cout << "\n4. Testing valid input:" << std::endl;
    try {
        double result = energy_of_perception(0.8, 0.6, 0.6, 0.3, true);
        std::cout << "  ✓ Success: ΔEΨ = " << result << std::endl;
    } catch (const KernelException& e) {
        std::cout << "  ✗ Unexpected error: " << e.what() << std::endl;
    }
    
    // Example 5: Error code enumeration
    std::cout << "\n5. Error code examples:" << std::endl;
    std::cout << "  INVALID_INPUT: " << static_cast<int>(ErrorCode::INVALID_INPUT) << std::endl;
    std::cout << "  INVALID_RANGE: " << static_cast<int>(ErrorCode::INVALID_RANGE) << std::endl;
    std::cout << "  NAN_DETECTED: " << static_cast<int>(ErrorCode::NAN_DETECTED) << std::endl;
    std::cout << "  FORMULA_OVERFLOW: " << static_cast<int>(ErrorCode::FORMULA_OVERFLOW) << std::endl;
    
    return 0;
}

