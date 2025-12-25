# LLM Integration Tests

**Purpose:** Test LLM integration with Cogman Energetic Engine

---

## Test Structure

```
tests/llm/
├── test_llm_integration.py    # Basic LLM integration tests
├── test_llm_mock.py           # LLM with mocked responses
└── test_llm_with_runtime.py   # LLM in Runtime Loop flow
```

---

## Test Categories

### 1. LLM Integration Tests
- **test_llm_integration.py**
  - Test LLM Annotation
  - Test LLM Prompt Templates
  - Test LLM Response Formatter
  - Test LLM Boundary Compliance

### 2. LLM Mock Tests
- **test_llm_mock.py**
  - Test LLM with mocked responses
  - Test LLM API call mocking
  - Test LLM error handling
  - Test LLM with system outputs

### 3. LLM with Runtime Tests
- **test_llm_with_runtime.py**
  - Test LLM in Runtime Loop flow
  - Test LLM with GateCore decisions
  - Test LLM with energy projection

---

## Running Tests

### Run All LLM Tests
```bash
python3 -m unittest tests.llm.test_llm_integration
python3 -m unittest tests.llm.test_llm_mock
python3 -m unittest tests.llm.test_llm_with_runtime
```

### Run Specific Test
```bash
python3 -m unittest tests.llm.test_llm_integration.TestLLMAnnotation
```

---

## Test Principles

### LLM Boundary Compliance
- ✅ LLM does NOT access Kernel directly
- ✅ LLM does NOT access GateCore directly
- ✅ LLM output has NO decision authority
- ✅ LLM is post-decision only

### LLM Usage Rules
- ✅ LLM annotates system outputs
- ✅ LLM explains gate decisions
- ✅ LLM summarizes energy projections
- ✅ LLM formats responses for humans
- ❌ LLM does NOT make decisions
- ❌ LLM does NOT override gate verdicts
- ❌ LLM does NOT modify system state

---

## Mock LLM Responses

For testing without actual LLM API calls:

```python
from unittest.mock import patch

@patch('llm.annotation.Annotation.annotate')
def test_with_mock(mock_annotate):
    mock_annotate.return_value = "Mocked LLM response"
    # Test with mocked response
```

---

## Reference

- **LLM_INTERFACE_SPEC.md:** LLM interface specification
- **RUNTIME_CONTRACT_SPEC.md:** Runtime contracts
- **ACTION_MODULE_SPEC.md:** Action module specification

---

## Status

**Current Status:** Test framework implemented, ready for LLM integration

