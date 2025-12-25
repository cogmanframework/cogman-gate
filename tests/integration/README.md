# Integration Tests

**Purpose:** End-to-end tests

## Responsibility

- Test complete system end-to-end
- Test external interfaces
- Test data flow
- Test system behavior

## Test Coverage

### End-to-End Flow
```
External Input → Adapters → Runtime → Core → Decision → Action → External Output
```

### Interface Tests
- FFI (C++ ↔ Python)
- REST API
- gRPC services
- SDK

### Data Flow Tests
- Schema validation
- Data transformation
- State persistence
- Trace generation

### System Behavior Tests
- Complete processing flow
- Memory integration
- Trajectory creation
- Decision making

## Test Scenarios

### Scenario 1: Text Input → Decision
1. Text input via adapter
2. Process through runtime
3. Compute energy
4. Make decision
5. Generate response

### Scenario 2: Image Input → Decision
1. Image input via adapter
2. Process through runtime
3. Compute energy
4. Make decision
5. Generate response

### Scenario 3: Memory Recall
1. Input triggers memory recall
2. Resonance matching
3. Memory retrieved
4. Used in processing

### Scenario 4: Trajectory Creation
1. Input passes Admission Gate
2. Trajectory created
3. States appended
4. Trajectory persisted

## Test Framework

### End-to-End Tests
- Complete system flow
- Real-world scenarios
- Performance tests

### Interface Tests
- API contract tests
- Schema validation tests
- Error handling tests

## Reference

- BASE-2: Data Contracts
- BASE-4: Layer Responsibility Lock
- BASE-5: Event & Trace System

