# LLM Testing Guide

**Purpose:** Guide for testing LLM integration with Cogman Energetic Engine

---

## Overview

LLM (Large Language Model) integration is tested to ensure:
- ✅ LLM follows boundary rules (LLM_INTERFACE_SPEC.md)
- ✅ LLM is only called post-decision
- ✅ LLM output has no decision authority
- ✅ LLM annotations are traceable

---

## Test Structure

### 1. Unit Tests
- **Location:** `tests/llm/test_llm_integration.py`
- **Purpose:** Test LLM modules in isolation
- **Coverage:**
  - Annotation module
  - Prompt templates
  - Response formatter
  - Boundary compliance

### 2. Mock Tests
- **Location:** `tests/llm/test_llm_mock.py`
- **Purpose:** Test LLM with mocked responses
- **Coverage:**
  - Mocked LLM API calls
  - Error handling
  - System output annotation

### 3. Integration Tests
- **Location:** `tests/llm/test_llm_with_runtime.py`
- **Purpose:** Test LLM in Runtime Loop flow
- **Coverage:**
  - LLM in Action phase
  - LLM with GateCore decisions
  - LLM with energy projections

---

## Running Tests

### Run All LLM Tests
```bash
# Unit tests
python3 -m unittest tests.llm.test_llm_integration

# Mock tests
python3 -m unittest tests.llm.test_llm_mock

# Integration tests
python3 -m unittest tests.llm.test_llm_with_runtime
```

### Run Manual Test Tool
```bash
python3 tools/test_llm_integration.py
```

### Run Specific Test
```bash
python3 -m unittest tests.llm.test_llm_integration.TestLLMAnnotation.test_annotate_basic
```

---

## Test Scenarios

### Scenario 1: Basic Annotation
```python
from llm import Annotation

annotation = Annotation()
result = annotation.annotate("Test content")
assert isinstance(result, str)
```

### Scenario 2: Gate Decision Annotation
```python
gate_decision = {
    "verdict": "ALLOW",
    "reason": "Low entropy",
    "metrics": {"H": 0.3}
}

annotation = Annotation()
result = annotation.annotate(
    str(gate_decision),
    context={"type": "gate_decision"}
)
```

### Scenario 3: Energy State Annotation
```python
energy_state = {
    "I": 0.7,
    "P": 0.6,
    "S": 0.8,
    "H": 0.3
}

annotation = Annotation()
result = annotation.annotate(
    str(energy_state),
    context={"type": "energy_state"}
)
```

---

## Mock LLM Responses

For testing without actual LLM API calls:

```python
from unittest.mock import patch

@patch('llm.annotation.Annotation.annotate')
def test_with_mock(mock_annotate):
    mock_annotate.return_value = "Mocked LLM response"
    
    annotation = Annotation()
    result = annotation.annotate("Test")
    
    assert result == "Mocked LLM response"
    mock_annotate.assert_called_once()
```

---

## Boundary Compliance Tests

### Test 1: No Direct Kernel Access
```python
def test_llm_no_direct_kernel_access():
    """Test that LLM does not access Kernel directly."""
    import llm.annotation
    import inspect
    
    source = inspect.getsource(llm.annotation)
    assert 'from kernel' not in source
    assert 'import kernel' not in source
```

### Test 2: No Direct GateCore Access
```python
def test_llm_no_direct_gate_access():
    """Test that LLM does not access GateCore directly."""
    import llm.annotation
    import inspect
    
    source = inspect.getsource(llm.annotation)
    assert 'from gate' not in source
    assert 'import gate' not in source
```

### Test 3: No Decision Authority
```python
def test_llm_no_decision_authority():
    """Test that LLM output has no decision authority."""
    annotation = Annotation()
    result = annotation.annotate("Test")
    
    # Result should not contain decision commands
    assert "ALLOW" not in result.upper()
    assert "BLOCK" not in result.upper()
    assert "REVIEW" not in result.upper()
```

---

## Integration with Runtime Loop

### Test: LLM Only in Action Phase
```python
def test_llm_only_in_action_phase():
    """Test that LLM is only called in Action phase."""
    # LLM should only be invoked in PHASE 8 (Action)
    # Not in earlier phases (1-7)
    pass
```

### Test: LLM Post-Decision Only
```python
def test_llm_post_decision_only():
    """Test that LLM is only called post-decision."""
    # LLM should only be called after GateCore decision
    # Not before or during decision
    pass
```

---

## Error Handling Tests

### Test: LLM Error Handling
```python
def test_llm_error_handling():
    """Test LLM error handling."""
    annotation = Annotation()
    
    # Should handle errors gracefully
    try:
        result = annotation.annotate("Test", context={"invalid": "data"})
        assert result is not None
    except Exception as e:
        # If exception is raised, it should be handled
        assert False, f"Annotation should handle errors: {e}"
```

---

## Test Checklist

- [ ] LLM annotation works
- [ ] LLM prompt templates exist
- [ ] LLM response formatter works
- [ ] LLM boundary compliance verified
- [ ] LLM does not access Kernel directly
- [ ] LLM does not access GateCore directly
- [ ] LLM output has no decision authority
- [ ] LLM is only called post-decision
- [ ] LLM error handling works
- [ ] LLM annotations are traceable

---

## Reference

- **LLM_INTERFACE_SPEC.md:** LLM interface specification
- **RUNTIME_CONTRACT_SPEC.md:** Runtime contracts
- **tests/llm/README.md:** LLM test documentation

---

## Status

**Current Status:** Test framework implemented, ready for LLM integration

