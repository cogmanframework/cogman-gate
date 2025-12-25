# Safety Tests

**Purpose:** Gate / fail-closed tests

## Responsibility

- Test Decision Gate behavior
- Test fail-closed scenarios
- Test safety constraints
- Test boundary conditions

## Test Coverage

### Decision Gate Tests

#### ALLOW Cases
- Normal operation
- Low entropy
- Low trajectory distance
- Eμ outside restrict range

#### REVIEW Cases
- High entropy (H ≥ threshold)
- High trajectory distance (D_traj ≥ threshold)
- Edge cases near thresholds

#### BLOCK Cases
- Rule violation (rule_fail = true)
- Eμ in restrict range
- Multiple blocking conditions

### Fail-Closed Tests

#### Invalid Input
- Invalid state values
- Out-of-range parameters
- NaN/Infinity values
- Missing required fields

#### Error Conditions
- Formula computation errors
- State validation failures
- Memory errors
- System errors

#### Boundary Conditions
- Minimum values
- Maximum values
- Edge cases
- Corner cases

### Safety Constraints

#### H > 0.85 → HOLD
- Test entropy threshold
- Test hold behavior
- Test recovery

#### S < 0.2 → STABILIZE
- Test stability threshold
- Test stabilize behavior
- Test recovery

#### E_total > MAX → DENY
- Test energy threshold
- Test deny behavior
- Test recovery

## Test Framework

### Safety Tests
- Fail-closed behavior
- Error handling
- Recovery mechanisms

### Boundary Tests
- Edge cases
- Corner cases
- Limit conditions

### Stress Tests
- Extreme inputs
- Chaotic inputs
- High load

## Reference

- BASE-1: Canonical Definitions (Gate definition)
- BASE-3: Formula Registry (CORE-9)
- BASE-4: Layer Responsibility Lock
- BASE-6: Legal / Meaning Lock

