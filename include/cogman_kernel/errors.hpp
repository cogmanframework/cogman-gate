/**
 * Cogman Kernel - Error Handling
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Error handling must not be modified without review
 * 
 * Provides exception classes, error codes, and error handling utilities
 */

#ifndef COGMAN_KERNEL_ERRORS_HPP
#define COGMAN_KERNEL_ERRORS_HPP

#include <stdexcept>
#include <string>
#include <cstdint>

namespace cogman_kernel {

/**
 * Error Codes
 */
enum class ErrorCode : std::uint32_t {
    // Success
    SUCCESS = 0,
    
    // Input validation errors (1xxx)
    INVALID_INPUT = 1000,
    INVALID_RANGE = 1001,
    INVALID_STATE = 1002,
    INVALID_PARAMETER = 1003,
    NAN_DETECTED = 1004,
    INFINITY_DETECTED = 1005,
    
    // State errors (2xxx)
    INVALID_EPS8_STATE = 2000,
    INVALID_ENERGY_STATE = 2001,
    STATE_OUT_OF_RANGE = 2002,
    
    // Formula errors (3xxx)
    FORMULA_INVALID_INPUT = 3000,
    FORMULA_DIVISION_BY_ZERO = 3001,
    FORMULA_OVERFLOW = 3002,
    FORMULA_UNDERFLOW = 3003,
    
    // Gate errors (4xxx)
    GATE_INVALID_INPUT = 4000,
    GATE_INVALID_BANDS = 4001,
    GATE_INVALID_METRICS = 4002,
    
    // Memory errors (5xxx)
    MEMORY_ALLOCATION_FAILED = 5000,
    MEMORY_ACCESS_VIOLATION = 5001,
    
    // System errors (9xxx)
    SYSTEM_ERROR = 9000,
    UNKNOWN_ERROR = 9999
};

/**
 * Convert error code to string
 */
inline const char* error_code_to_string(ErrorCode code) {
    switch (code) {
        case ErrorCode::SUCCESS: return "SUCCESS";
        case ErrorCode::INVALID_INPUT: return "INVALID_INPUT";
        case ErrorCode::INVALID_RANGE: return "INVALID_RANGE";
        case ErrorCode::INVALID_STATE: return "INVALID_STATE";
        case ErrorCode::INVALID_PARAMETER: return "INVALID_PARAMETER";
        case ErrorCode::NAN_DETECTED: return "NAN_DETECTED";
        case ErrorCode::INFINITY_DETECTED: return "INFINITY_DETECTED";
        case ErrorCode::INVALID_EPS8_STATE: return "INVALID_EPS8_STATE";
        case ErrorCode::INVALID_ENERGY_STATE: return "INVALID_ENERGY_STATE";
        case ErrorCode::STATE_OUT_OF_RANGE: return "STATE_OUT_OF_RANGE";
        case ErrorCode::FORMULA_INVALID_INPUT: return "FORMULA_INVALID_INPUT";
        case ErrorCode::FORMULA_DIVISION_BY_ZERO: return "FORMULA_DIVISION_BY_ZERO";
        case ErrorCode::FORMULA_OVERFLOW: return "FORMULA_OVERFLOW";
        case ErrorCode::FORMULA_UNDERFLOW: return "FORMULA_UNDERFLOW";
        case ErrorCode::GATE_INVALID_INPUT: return "GATE_INVALID_INPUT";
        case ErrorCode::GATE_INVALID_BANDS: return "GATE_INVALID_BANDS";
        case ErrorCode::GATE_INVALID_METRICS: return "GATE_INVALID_METRICS";
        case ErrorCode::MEMORY_ALLOCATION_FAILED: return "MEMORY_ALLOCATION_FAILED";
        case ErrorCode::MEMORY_ACCESS_VIOLATION: return "MEMORY_ACCESS_VIOLATION";
        case ErrorCode::SYSTEM_ERROR: return "SYSTEM_ERROR";
        case ErrorCode::UNKNOWN_ERROR: return "UNKNOWN_ERROR";
        default: return "UNKNOWN_ERROR_CODE";
    }
}

/**
 * Base exception class for Cogman Kernel
 */
class KernelException : public std::runtime_error {
public:
    explicit KernelException(ErrorCode code, const std::string& message)
        : std::runtime_error(message), code_(code) {}
    
    explicit KernelException(ErrorCode code, const char* message)
        : std::runtime_error(message), code_(code) {}
    
    ErrorCode code() const noexcept { return code_; }
    
    const char* code_string() const noexcept {
        return error_code_to_string(code_);
    }
    
    std::string full_message() const {
        return std::string(code_string()) + ": " + what();
    }

private:
    ErrorCode code_;
};

/**
 * Invalid input exception
 */
class InvalidInputException : public KernelException {
public:
    explicit InvalidInputException(const std::string& message)
        : KernelException(ErrorCode::INVALID_INPUT, message) {}
    
    explicit InvalidInputException(const char* message)
        : KernelException(ErrorCode::INVALID_INPUT, message) {}
};

/**
 * Invalid range exception
 */
class InvalidRangeException : public KernelException {
public:
    explicit InvalidRangeException(const std::string& message)
        : KernelException(ErrorCode::INVALID_RANGE, message) {}
    
    explicit InvalidRangeException(const char* message)
        : KernelException(ErrorCode::INVALID_RANGE, message) {}
    
    InvalidRangeException(const std::string& param_name, double value, 
                         double min_val, double max_val)
        : KernelException(ErrorCode::INVALID_RANGE, 
            param_name + "=" + std::to_string(value) + 
            " out of range [" + std::to_string(min_val) + 
            ", " + std::to_string(max_val) + "]") {}
};

/**
 * Invalid state exception
 */
class InvalidStateException : public KernelException {
public:
    explicit InvalidStateException(const std::string& message)
        : KernelException(ErrorCode::INVALID_STATE, message) {}
    
    explicit InvalidStateException(const char* message)
        : KernelException(ErrorCode::INVALID_STATE, message) {}
};

/**
 * Invalid EPS-8 state exception
 */
class InvalidEPS8StateException : public KernelException {
public:
    explicit InvalidEPS8StateException(const std::string& message)
        : KernelException(ErrorCode::INVALID_EPS8_STATE, message) {}
    
    explicit InvalidEPS8StateException(const char* message)
        : KernelException(ErrorCode::INVALID_EPS8_STATE, message) {}
};

/**
 * Formula computation exception
 */
class FormulaException : public KernelException {
public:
    explicit FormulaException(ErrorCode code, const std::string& message)
        : KernelException(code, message) {}
    
    explicit FormulaException(ErrorCode code, const char* message)
        : KernelException(code, message) {}
};

/**
 * Gate exception
 */
class GateException : public KernelException {
public:
    explicit GateException(ErrorCode code, const std::string& message)
        : KernelException(code, message) {}
    
    explicit GateException(ErrorCode code, const char* message)
        : KernelException(code, message) {}
};

/**
 * Error message formatter
 */
class ErrorFormatter {
public:
    static std::string format_range_error(const std::string& param_name,
                                         double value,
                                         double min_val,
                                         double max_val) {
        return param_name + "=" + std::to_string(value) + 
               " out of range [" + std::to_string(min_val) + 
               ", " + std::to_string(max_val) + "]";
    }
    
    static std::string format_nan_error(const std::string& param_name) {
        return param_name + " is NaN";
    }
    
    static std::string format_infinity_error(const std::string& param_name) {
        return param_name + " is infinity";
    }
    
    static std::string format_validation_error(const std::string& object_name,
                                              const std::string& reason) {
        return "Invalid " + object_name + ": " + reason;
    }
};

/**
 * Check for NaN and throw if found
 */
inline void check_nan(const std::string& param_name, double value) {
    if (std::isnan(value)) {
        throw InvalidInputException(ErrorFormatter::format_nan_error(param_name));
    }
}

/**
 * Check for infinity and throw if found
 */
inline void check_infinity(const std::string& param_name, double value) {
    if (std::isinf(value)) {
        throw InvalidInputException(ErrorFormatter::format_infinity_error(param_name));
    }
}

/**
 * Check range and throw if out of range
 */
inline void check_range(const std::string& param_name, double value,
                       double min_val, double max_val) {
    if (value < min_val || value > max_val) {
        throw InvalidRangeException(param_name, value, min_val, max_val);
    }
}

/**
 * Check range (lower bound only)
 */
inline void check_range_min(const std::string& param_name, double value, double min_val) {
    if (value < min_val) {
        throw InvalidRangeException(param_name, value, min_val, 
                                   std::numeric_limits<double>::max());
    }
}

/**
 * Check range (upper bound only)
 */
inline void check_range_max(const std::string& param_name, double value, double max_val) {
    if (value > max_val) {
        throw InvalidRangeException(param_name, value, 
                                   std::numeric_limits<double>::lowest(), max_val);
    }
}

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_ERRORS_HPP

