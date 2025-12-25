# Core Formula Tests

**Purpose:** Formula tests for CORE-1 to CORE-9

## Responsibility

- Test core formulas (CORE-1 to CORE-9)
- Validate input ranges
- Validate output ranges
- Test edge cases
- Test error handling

## Test Coverage

### CORE-1: Energy of Perception (ΔEΨ)
- Test with valid inputs
- Test with edge cases (H=0, H=1, I=0)
- Test with invalid inputs (negative I, H>1)
- Test both variants (|P| vs P)

### CORE-2: Reflex Energy (E_reflex)
- Test with valid inputs
- Test with edge cases (A=0, A=1)
- Test dependency on CORE-1

### CORE-3: Directional Reflex Energy (ΔEΨ_theta)
- Test with valid inputs
- Test phase wrapping
- Test dependency on CORE-1

### CORE-4: Cognitive Energy (E_mind)
- Test with valid inputs
- Test edge cases
- Test output range [0, 1]

### CORE-5: Coherence Energy (E_coherence)
- Test with valid inputs
- Test edge cases
- Test output range [0, 1]

### CORE-6: Neuro-Energetic Sum (E_neural)
- Test with valid inputs
- Test with zero values
- Test interface/placeholder behavior

### CORE-7: Binding Energy (E_bind)
- Test with valid inputs
- Test with zero components
- Test dependencies (CORE-4, CORE-5, CORE-6)

### CORE-8: Memory Encoding Energy (E_mem)
- Test with valid inputs
- Test with zero components
- Test dependencies (CORE-7, E_pred)

### CORE-9: Decision Gate (G_decision)
- Test ALLOW cases
- Test REVIEW cases
- Test BLOCK cases
- Test all decision rules

## Test Framework

### Unit Tests
- Test each formula independently
- Test validation functions
- Test error handling

### Property Tests
- Test bounds (monotonicity, ranges)
- Test invariants
- Test mathematical properties

### Integration Tests
- Test formula dependencies
- Test complete energy computation flow

## Reference

- BASE-3: Formula Registry
- COGMAN_CORE_KERNEL.md

