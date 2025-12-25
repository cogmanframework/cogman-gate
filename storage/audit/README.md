# Audit Storage

**Purpose:** Trace / lineage / replay

## Responsibility

- Store audit traces
- Track data lineage
- Enable replay functionality
- Audit trail for compliance

## Structure

### trace_map/
- **Purpose:** Trace mapping storage
- **Format:** Trace index files
- **Access:** Read/write trace maps

### lineage/
- **Purpose:** Data lineage storage
- **Format:** Lineage graph files
- **Access:** Read/write lineage

## Trace Format

```json
{
  "trace_id": "uuid",
  "timestamp": 1234567890.0,
  "event_type": "ENERGY_PROJECTED",
  "event_data": {...},
  "parent_trace_id": "uuid",
  "child_trace_ids": ["uuid", ...],
  "lineage": {
    "source": "sensory",
    "transformations": [
      {
        "module": "perception",
        "timestamp": 1234567890.0
      }
    ],
    "sink": "action"
  }
}
```

## Lineage Format

```json
{
  "data_id": "uuid",
  "lineage": {
    "sources": ["uuid", ...],
    "transformations": [
      {
        "module": "perception",
        "operation": "energy_projection",
        "timestamp": 1234567890.0
      }
    ],
    "sinks": ["uuid", ...]
  }
}
```

## Operations

### Store Trace
- Store trace event
- Update trace map
- Update lineage

### Query Trace
- Query by trace_id
- Query by event_type
- Query by time range

### Replay Trace
- Load trace from storage
- Replay trace events
- Validate replay

### Lineage Query
- Query data lineage
- Trace data flow
- Find data sources/sinks

## Reference

- BASE-5: Event & Trace System
- tools/replay_engine.py

