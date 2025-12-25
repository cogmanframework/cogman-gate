# Error Handling Guide

**Purpose:** Guide for error handling in Cogman Energetic Engine

---

## Error Handling Architecture

### C++ Kernel
- **Location:** `kernel/include/cogman_kernel/errors.hpp`
- **Error Codes:** Enum `ErrorCode` (1xxx-9xxx)
- **Exceptions:** `KernelException` and derived classes
- **Validation:** `check_nan()`, `check_infinity()`, `check_range()`

### Python Runtime
- **Location:** `runtime/error_handler.py`
- **Error Handler:** `RuntimeErrorHandler` class
- **Error Severity:** `ErrorSeverity` enum (LOW, MEDIUM, HIGH, CRITICAL)
- **Error History:** Tracked for analysis

---

## Error Handling Rules

### Runtime Loop
- **On Error:** ABORT current cycle, LOG error, CONTINUE to next input
- **Forbidden:** Retry, fallback, auto-correction, heuristic bypass

### GateCore
- **On Error:** BLOCK verdict, LOG error, NO release
- **Forbidden:** Override, bypass, reinterpret

### Memory
- **On Error:** Return empty result, LOG warning, NO exception
- **Forbidden:** Crash, modify state, write invalid data

### Reasoning
- **On Error:** RAISE exception, DO NOT continue
- **Forbidden:** Fallback, auto-resolution, heuristic guessing

### Action
- **On Error:** Return error in ActionOutput, LOG error
- **Forbidden:** Retry, fallback action, silent failure

---

## Error Types

### Input Validation Errors (1xxx)
- `INVALID_INPUT` (1000)
- `INVALID_RANGE` (1001)
- `INVALID_STATE` (1002)
- `NAN_DETECTED` (1004)
- `INFINITY_DETECTED` (1005)

### State Errors (2xxx)
- `INVALID_EPS8_STATE` (2000)
- `INVALID_ENERGY_STATE` (2001)
- `STATE_OUT_OF_RANGE` (2002)

### Formula Errors (3xxx)
- `FORMULA_INVALID_INPUT` (3000)
- `FORMULA_DIVISION_BY_ZERO` (3001)
- `FORMULA_OVERFLOW` (3002)
- `FORMULA_UNDERFLOW` (3003)

### Gate Errors (4xxx)
- `GATE_INVALID_INPUT` (4000)
- `GATE_INVALID_BANDS` (4001)
- `GATE_INVALID_METRICS` (4002)

### System Errors (9xxx)
- `SYSTEM_ERROR` (9000)
- `UNKNOWN_ERROR` (9999)

---

## Error Handling Examples

### C++ Kernel
```cpp
try {
    double result = energy_of_perception(I, P, S_a, H);
} catch (const InvalidInputException& e) {
    // Handle invalid input
} catch (const FormulaException& e) {
    // Handle formula error
}
```

### Python Runtime
```python
from runtime import RuntimeErrorHandler, ErrorSeverity

error_handler = RuntimeErrorHandler()

try:
    # Runtime Loop operation
    pass
except Exception as e:
    result = error_handler.handle_error(
        phase="PHASE_4",
        error=e,
        severity=ErrorSeverity.HIGH
    )
    # ABORT cycle, CONTINUE to next
```

---

## Testing Error Handling

### Test Error Propagation
```python
def test_error_propagation(self):
    """Test that errors propagate correctly."""
    # Test error handling
    pass
```

### Test Fail-Closed
```python
def test_fail_closed(self):
    """Test fail-closed behavior."""
    # Test that errors cause safe shutdown
    pass
```

---

## Status

**Current Status:** Error handling implemented for Kernel and Runtime

