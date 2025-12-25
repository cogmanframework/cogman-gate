# Inspector Tool

**Purpose:** Trace / state viewer

## Responsibility

- View and inspect system traces
- View and inspect system state
- Debug trajectory flows
- Analyze event sequences

## Features

### Trace Viewer
- Display trace_id and event sequences
- Filter by event type
- Search by trace_id
- Timeline visualization

### State Viewer
- Display current system state (Ψ = { I, P, S, H, F })
- Display energy state
- Display decision parameters
- Display neural components

### Trajectory Inspector
- View trajectory states
- Navigate through trajectory history
- Compare trajectory states
- Analyze trajectory evolution

### Event Inspector
- View event logs
- Filter by event type
- Search by keywords
- Export event data

## Event Types

- `ENERGY_PROJECTED` - Energy computation completed
- `TRAJECTORY_CREATED` - New trajectory created
- `GATE_BLOCKED` - Decision gate blocked
- `GATE_REVIEW` - Decision gate review
- `GATE_ALLOWED` - Decision gate allowed
- `MEMORY_RESONATED` - Memory resonance triggered
- `STATE_UPDATED` - System state updated

## Usage

### View Trace
```bash
inspector view-trace <trace_id>
```

### View State
```bash
inspector view-state <state_id>
```

### View Trajectory
```bash
inspector view-trajectory <trajectory_id>
```

### Search Events
```bash
inspector search-events --type ENERGY_PROJECTED --trace-id <trace_id>
```

## Reference

- BASE-5: Event & Trace System
- BASE-2: Data Contracts (State schema)

