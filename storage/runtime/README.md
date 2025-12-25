# Runtime Storage

**Purpose:** Snapshot / state dump

## Responsibility

- Store runtime snapshots
- State dumps for recovery
- System state checkpoints
- State restoration

## Structure

### state/
- **Purpose:** Runtime state snapshots
- **Format:** State dump files
- **Access:** Read/write snapshots

## Snapshot Format

```json
{
  "snapshot_id": "uuid",
  "timestamp": 1234567890.0,
  "state": {
    "system_state": {
      "mode": "ENGINEERING_SIM",
      "running": true,
      ...
    },
    "perception_state": {...},
    "memory_state": {...},
    "gate_state": {...}
  },
  "metadata": {
    "version": "2.0.0",
    "uptime": 3600.0
  }
}
```

## Operations

### Create Snapshot
- Capture current system state
- Store snapshot to disk
- Update snapshot index

### Restore Snapshot
- Load snapshot from disk
- Restore system state
- Validate state

### Snapshot Management
- List snapshots
- Delete old snapshots
- Snapshot rotation

## Reference

- runtime/ module
- BASE-2: Data Contracts

