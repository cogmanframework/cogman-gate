# Runtime Flow Tests

**Purpose:** Flow tests for runtime modules

## Responsibility

- Test flow between runtime modules
- Test state transitions
- Test module interactions
- Test error propagation

## Test Coverage

### Sensory Module
- Test input conversion
- Test feature extraction
- Test SensoryState creation
- Test error handling

### Perception Module
- Test IPSH calculation
- Test Admission Gate (CORE-1)
- Test normalization
- Test validation

### Reasoning Module
- Test structure building
- Test causal graph creation
- Test pattern identification
- Test reasoning structure preparation

### Thinking Module
- Test evaluation
- Test scoring
- Test assessment
- Test E_pred calculation

### Decision Module
- Test decision gate (CORE-9)
- Test routing
- Test decision logging
- Test error handling

### Action Module
- Test output generation
- Test action execution
- Test external interface
- Test error handling

### Controller Module
- Test orchestration
- Test state machine
- Test error recovery
- Test module coordination

## Flow Tests

### Complete Flow
```
sensory → perception → reasoning → thinking → decision → action
```

### Error Flow
```
Error in module → Controller handles → Recovery/Abort
```

### State Machine Tests
```
IDLE → SENSORY → PERCEPTION → ... → ACTION → IDLE
```

## Test Framework

### Integration Tests
- Test complete flow
- Test module interactions
- Test state transitions

### Error Tests
- Test error propagation
- Test error recovery
- Test fail-safe behavior

## Reference

- BASE-4: Layer Responsibility Lock
- BASE-5: Event & Trace System
- runtime/README.md

