# Memory Storage

**Purpose:** Backing store for memory/* modules

## Responsibility

- Store memory data (episodic, semantic, procedural, identity)
- Persistent storage for memory fields
- Memory retrieval and updates
- Memory consolidation

## Structure

### episodic/
- **Purpose:** Episodic memory storage
- **Format:** Event-based storage
- **Access:** Read/write episodic memories

### semantic/
- **Purpose:** Semantic memory storage
- **Format:** Principle/pattern storage
- **Access:** Read/write semantic memories

### procedural/
- **Purpose:** Procedural memory storage
- **Format:** Action weight storage
- **Access:** Read/write procedural memories

### identity/
- **Purpose:** Identity memory storage
- **Format:** Identity/self storage
- **Access:** Read/write identity memories

## Memory Format

### Episodic Memory
```json
{
  "event_id": "uuid",
  "timestamp": 1234567890.0,
  "event": {
    "type": "perception",
    "data": {...}
  },
  "energy": {
    "E_mem": 0.5,
    ...
  }
}
```

### Semantic Memory
```json
{
  "principle_id": "uuid",
  "principle": "causal_rule",
  "pattern": {...},
  "strength": 0.8,
  "last_accessed": 1234567890.0
}
```

### Procedural Memory
```json
{
  "action": "text_output",
  "weight": 0.7,
  "last_used": 1234567890.0,
  "success_count": 10
}
```

### Identity Memory
```json
{
  "identity": {
    "name": "system",
    "properties": {...}
  },
  "last_updated": 1234567890.0
}
```

## Operations

### Store Memory
- Store episodic/semantic/procedural/identity memory
- Update memory strength
- Update access time

### Retrieve Memory
- Retrieve by query
- Retrieve by resonance
- Retrieve by strength

### Consolidate Memory
- Consolidate memories over time
- Update memory weights
- Remove weak memories

## Reference

- memory/ module
- BASE-2: Data Contracts

