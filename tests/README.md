# Test Suite

**Purpose:** Comprehensive test suite for Cogman Energetic Engine

---

## Test Structure

```
tests/
├── core/            # Formula tests (CORE-1 to CORE-9)
├── runtime/         # Flow tests (runtime modules)
├── integration/     # End-to-end tests
└── safety/          # Gate / fail-closed tests
```

---

## Test Categories

### Core Tests
- **Purpose:** Test core formulas
- **Coverage:** CORE-1 to CORE-9
- **Type:** Unit tests, property tests

### Runtime Tests
- **Purpose:** Test runtime flow
- **Coverage:** Module interactions, state transitions
- **Type:** Integration tests, flow tests

### Integration Tests
- **Purpose:** End-to-end system tests
- **Coverage:** Complete system flow, interfaces
- **Type:** End-to-end tests, interface tests

### Safety Tests
- **Purpose:** Safety and fail-closed behavior
- **Coverage:** Decision Gate, error handling, boundaries
- **Type:** Safety tests, boundary tests, stress tests

---

## Test Principles

### Deterministic
- Same inputs → same outputs
- No randomness in core tests
- Reproducible results

### Comprehensive
- Test all formulas
- Test all modules
- Test all flows
- Test edge cases

### Safety-First
- Fail-closed behavior
- Error handling
- Boundary validation

---

## Running Tests

### Core Tests
```bash
cd tests/core
./run_tests
```

### Runtime Tests
```bash
cd tests/runtime
./run_tests
```

### Integration Tests
```bash
cd tests/integration
./run_tests
```

### Safety Tests
```bash
cd tests/safety
./run_tests
```

### All Tests
```bash
cd tests
./run_all_tests
```

---

## Test Coverage Goals

- **Core Formulas:** 100% coverage
- **Runtime Modules:** 90%+ coverage
- **Integration:** Critical paths 100%
- **Safety:** 100% coverage

---

## Reference

- **BASE-1:** Canonical Definitions
- **BASE-2:** Data Contracts
- **BASE-3:** Formula Registry
- **BASE-4:** Layer Responsibility Lock
- **BASE-5:** Event & Trace System
- **BASE-6:** Legal / Meaning Lock

---

## Status

**Development Status:** In Progress  
**Test Framework:** To be implemented

