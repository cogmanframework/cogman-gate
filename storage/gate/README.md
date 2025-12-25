# Gate Storage

**Purpose:** Decision log (ALLOW/REVIEW/BLOCK)

## Responsibility

- Store decision gate verdicts
- Log all gate decisions
- Audit trail for decisions
- Decision statistics

## Structure

### verdicts/
- **Purpose:** Decision verdict storage
- **Format:** Decision log files
- **Access:** Append-only writes, read-only queries

## Decision Format

```json
{
  "decision_id": "uuid",
  "timestamp": 1234567890.0,
  "verdict": "ALLOW|REVIEW|BLOCK",
  "state": {
    "H": 0.3,
    "D_traj": 0.2,
    ...
  },
  "params": {
    "H_threshold": 0.85,
    "D_traj_threshold": 0.7,
    ...
  },
  "reason": "Low entropy",
  "trace_id": "uuid"
}
```

## Operations

### Log Decision
- Append decision to log
- Include state and parameters
- Include reason

### Query Decisions
- Query by verdict type
- Query by time range
- Query by trace_id

### Statistics
- Count decisions by type
- Decision distribution
- Decision trends

## Reference

- gate/ module
- BASE-3: Formula Registry (CORE-9)
- BASE-5: Event & Trace System

