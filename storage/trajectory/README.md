# Trajectory Storage

**Purpose:** Trajectory objects (append-only)

## Responsibility

- Store trajectory objects
- Append-only storage (immutable)
- Index trajectories for retrieval
- Track trajectory statistics

## Structure

### raw/
- **Purpose:** Raw trajectory data
- **Format:** JSON, binary, or custom format
- **Access:** Append-only writes, read-only queries

### index/
- **Purpose:** Trajectory indexes for fast retrieval
- **Format:** Index files (B-tree, hash, etc.)
- **Access:** Read/write indexes

### stats/
- **Purpose:** Trajectory statistics
- **Format:** Statistics files
- **Access:** Read/write statistics

## Trajectory Format

```json
{
  "trace_id": "uuid",
  "states": [
    {
      "timestamp": 1234567890.0,
      "state": {
        "I": 0.8,
        "P": 0.6,
        "S": 0.7,
        "H": 0.3,
        "A": 0.5,
        "S_a": 0.6,
        "theta": 1.5
      },
      "energy": {
        "delta_E_psi": 0.5,
        "E_reflex": 0.3,
        ...
      }
    }
  ],
  "metadata": {
    "state_count": 10,
    "duration": 1.5
  }
}
```

## Operations

### Append Trajectory
- Append new state to trajectory
- Update index
- Update statistics

### Query Trajectory
- Query by trace_id
- Query by time range
- Query by state properties

### Statistics
- Count trajectories
- Average trajectory length
- Trajectory distribution

## Reference

- BASE-2: Data Contracts (Trajectory schema)
- BASE-5: Event & Trace System

