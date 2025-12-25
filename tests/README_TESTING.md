# Testing Guide

**Purpose:** Guide for running and writing tests

---

## Test Structure

```
tests/
├── core/              # Core formula tests (C++)
├── runtime/           # Runtime module tests (Python)
│   ├── test_runtime_loop.py
│   ├── test_wm_controller.py
│   ├── test_gate_integration.py
│   └── test_error_handling.py
├── integration/       # Integration tests
│   └── test_full_flow.py
├── safety/            # Safety tests
│   └── test_fail_closed.py
├── test_utils.py      # Test utilities
└── run_tests.py       # Test runner
```

---

## Running Tests

### Run All Tests
```bash
python3 tests/run_tests.py
```

### Run Specific Test Module
```bash
python3 -m pytest tests/runtime/test_runtime_loop.py -v
python3 -m pytest tests/runtime/test_wm_controller.py -v
python3 -m pytest tests/runtime/test_gate_integration.py -v
python3 -m pytest tests/integration/test_full_flow.py -v
python3 -m pytest tests/safety/test_fail_closed.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=runtime --cov=gate --cov=memory --cov=reasoning --cov=action
```

---

## Test Categories

### Runtime Tests
- **test_runtime_loop.py**: Runtime Loop phase execution
- **test_wm_controller.py**: WM Controller functionality
- **test_gate_integration.py**: Gate integration
- **test_error_handling.py**: Error handling

### Integration Tests
- **test_full_flow.py**: Complete system flow

### Safety Tests
- **test_fail_closed.py**: Fail-closed behavior

---

## Test Utilities

### create_test_eps8_state()
Create test EPS-8 state dictionary.

### create_test_trajectory()
Create test trajectory.

### create_test_decision()
Create test decision.

### create_test_reasoning_output()
Create test reasoning output.

---

## Error Handling Tests

### Test Error Propagation
- Errors in phases should abort cycle
- Errors should be logged
- Errors should not break Runtime Loop

### Test Fail-Closed Behavior
- Safety rule failure → BLOCK
- High entropy → REVIEW
- Invalid input → Error handling

---

## Writing New Tests

### Test Template
```python
import unittest
from runtime import RuntimeLoop

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_feature(self):
        """Test feature."""
        # Test implementation
        pass
    
    def test_error_handling(self):
        """Test error handling."""
        # Test error scenarios
        pass

if __name__ == "__main__":
    unittest.main()
```

---

## Test Coverage Goals

- **Runtime Modules**: 90%+ coverage
- **Integration**: Critical paths 100%
- **Safety**: 100% coverage
- **Error Handling**: All error paths tested

---

## Status

**Current Status:** Test framework implemented, tests in progress

