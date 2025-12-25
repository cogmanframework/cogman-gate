# Storage System

**Purpose:** Persistent storage for Cogman Energetic Engine

---

## Storage Structure

```
storage/
├── trajectory/        # Trajectory objects (append-only)
│   ├── raw/          # Raw trajectory data
│   ├── index/        # Trajectory indexes
│   └── stats/        # Trajectory statistics
│
├── memory/           # Backing store for memory/* modules
│   ├── episodic/     # Episodic memory storage
│   ├── semantic/     # Semantic memory storage
│   ├── procedural/   # Procedural memory storage
│   └── identity/      # Identity memory storage
│
├── gate/              # Decision log (ALLOW/REVIEW/BLOCK)
│   └── verdicts/      # Decision verdict storage
│
├── runtime/           # Snapshot / state dump
│   └── state/        # Runtime state snapshots
│
├── audit/             # Trace / lineage / replay
│   ├── trace_map/     # Trace mapping storage
│   └── lineage/       # Data lineage storage
│
└── cache/             # Optional cache (redis / in-mem)
```

---

## Storage Modules

### Trajectory Storage
- **Purpose:** Store trajectory objects (append-only)
- **Features:** Raw data, indexes, statistics
- **Use Cases:** Trajectory persistence, retrieval, analysis

### Memory Storage
- **Purpose:** Backing store for memory modules
- **Features:** Episodic, semantic, procedural, identity storage
- **Use Cases:** Memory persistence, retrieval, consolidation

### Gate Storage
- **Purpose:** Decision log storage
- **Features:** Verdict logging, audit trail
- **Use Cases:** Decision tracking, audit, statistics

### Runtime Storage
- **Purpose:** Snapshot and state dump
- **Features:** System state snapshots, recovery
- **Use Cases:** State checkpointing, recovery, debugging

### Audit Storage
- **Purpose:** Trace and lineage storage
- **Features:** Trace mapping, data lineage, replay
- **Use Cases:** Audit trail, compliance, debugging

### Cache Storage
- **Purpose:** Optional caching layer
- **Features:** In-memory, Redis, file cache
- **Use Cases:** Performance optimization, reduced I/O

---

## Storage Principles

### Append-Only
- Trajectories and decisions are append-only
- Immutable data for audit trail
- No modifications, only additions

### Persistent
- All critical data is persisted
- Survives system restarts
- Reliable storage backend

### Indexed
- Fast retrieval with indexes
- Efficient querying
- Optimized access patterns

### Auditable
- Complete audit trail
- Trace lineage
- Replay capability

---

## Storage Backends

### File System
- **Default:** Local file system
- **Format:** JSON, binary, custom
- **Use Cases:** Development, small-scale

### Database
- **Options:** SQLite, PostgreSQL, etc.
- **Format:** Relational or document
- **Use Cases:** Production, large-scale

### Distributed Storage
- **Options:** S3, HDFS, etc.
- **Format:** Object storage
- **Use Cases:** Cloud, distributed systems

---

## Usage

### Store Trajectory
```python
from storage.trajectory import TrajectoryStorage

storage = TrajectoryStorage()
storage.append(trajectory)
```

### Store Memory
```python
from storage.memory import MemoryStorage

storage = MemoryStorage()
storage.store_episodic(memory)
```

### Store Decision
```python
from storage.gate import GateStorage

storage = GateStorage()
storage.log_verdict(decision)
```

### Create Snapshot
```python
from storage.runtime import RuntimeStorage

storage = RuntimeStorage()
storage.create_snapshot(state)
```

---

## Reference

- **BASE-2:** Data Contracts
- **BASE-5:** Event & Trace System
- **BASE-6:** Legal / Meaning Lock

---

## Status

**Development Status:** In Progress  
**Storage Backend:** To be implemented

