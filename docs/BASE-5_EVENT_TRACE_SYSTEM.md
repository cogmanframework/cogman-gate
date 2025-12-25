# BASE-5: Event & Trace System

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Debug-First Design

---

## Purpose

**ถ้าไม่มี trace → ระบบนี้ "ไม่ใช่วิศวกรรม"**

**ต้องมีตั้งแต่แรก**  
**อย่ารอ production ค่อยทำ**  
**คนทำ AI พังตรงนี้เยอะมาก**

---

## Core Principles

### 📌 Trace-First Design
- ทุก flow ต้องมี trace_id
- ทุก event ต้อง log ได้
- ทุก decision ต้องย้อนรอยได้

### 📌 Debug-First
- ระบบต้อง debug ได้ง่าย
- Log ต้อง map กลับสูตรได้
- Trace ต้อง complete

---

## Trace System

### Trace ID

**Format:**
```
<prefix>-<timestamp>-<random>
```

**Example:**
```
traj-20250110-120000-abc123def456
```

**Properties:**
- Unique per trajectory
- Sortable by timestamp
- Human-readable

**Usage:**
- ทุก trajectory ต้องมี trace_id
- ทุก event ต้องอ้างอิง trace_id
- Trace_id ใช้ในการ query logs

---

## Event Types

### Core Events

#### ENERGY_PROJECTED
**When:** หลังคำนวณ IPSH components  
**Data:**
```json
{
  "event": "ENERGY_PROJECTED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "I": 0.8,
    "P": 0.6,
    "S": 0.7,
    "H": 0.3
  }
}
```

#### TRAJECTORY_CREATED
**When:** หลังสร้าง trajectory ใหม่  
**Data:**
```json
{
  "event": "TRAJECTORY_CREATED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "state_0": {...},
    "delta_E_psi": 0.5
  }
}
```

#### TRAJECTORY_EXTENDED
**When:** หลัง append state ใหม่  
**Data:**
```json
{
  "event": "TRAJECTORY_EXTENDED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "state": {...},
    "energy": {...}
  }
}
```

#### GATE_EVALUATED
**When:** หลัง Decision Gate ตัดสิน  
**Data:**
```json
{
  "event": "GATE_EVALUATED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "decision": "ALLOW|REVIEW|BLOCK",
    "reason": [...],
    "metrics": {...}
  }
}
```

#### GATE_BLOCKED
**When:** Decision Gate ตัดสิน BLOCK  
**Data:**
```json
{
  "event": "GATE_BLOCKED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "reason": "rule_fail|E_mu_in_restrict|H_high|D_traj_high",
    "metrics": {...}
  }
}
```

#### MEMORY_RESONATED
**When:** หลัง resonance matching  
**Data:**
```json
{
  "event": "MEMORY_RESONATED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "memory_id": "...",
    "resonance_score": 0.8,
    "type": "episodic|semantic|procedural"
  }
}
```

#### MEMORY_ENCODED
**When:** หลังบันทึก memory  
**Data:**
```json
{
  "event": "MEMORY_ENCODED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "memory_id": "...",
    "E_mem": 0.5,
    "type": "episodic|semantic|procedural"
  }
}
```

#### FORMULA_COMPUTED
**When:** หลังคำนวณสูตร  
**Data:**
```json
{
  "event": "FORMULA_COMPUTED",
  "trace_id": "...",
  "timestamp": "...",
  "data": {
    "formula": "CORE-1|CORE-2|...",
    "inputs": {...},
    "output": 0.5
  }
}
```

---

## Event Schema

### Base Event Schema
```json
{
  "event": "string",
  "trace_id": "uuid",
  "timestamp": "ISO8601_datetime",
  "layer": "sensory|encoder|core|gate|memory|trajectory",
  "data": {}
}
```

### Required Fields
- `event`: Event type (enum)
- `trace_id`: Associated trajectory ID
- `timestamp`: When event occurred
- `layer`: Which layer generated event
- `data`: Event-specific data

---

## Log Format

### Structured Log Format
```
[LEVEL] [TIMESTAMP] [TRACE_ID] [LAYER] [EVENT] [DATA]
```

### Example
```
[INFO] [2025-01-10T12:00:00Z] [traj-abc123] [core] [FORMULA_COMPUTED] {"formula":"CORE-1","output":0.5}
[INFO] [2025-01-10T12:00:01Z] [traj-abc123] [gate] [GATE_EVALUATED] {"decision":"ALLOW"}
```

---

## Trace Query

### Query by Trace ID
```
GET /traces/{trace_id}
```

Returns: Complete trace of events for trajectory

### Query by Event Type
```
GET /events/{event_type}?from={timestamp}&to={timestamp}
```

Returns: All events of type in time range

### Query by Formula
```
GET /formulas/{formula_id}?trace_id={trace_id}
```

Returns: All computations of formula for trajectory

---

## Formula Mapping

### Log → Formula Mapping

ทุก log entry ที่เกี่ยวกับสูตร ต้องมี:
- Formula ID (CORE-1, CORE-2, etc.)
- Input values
- Output value
- Timestamp

### Example
```
[INFO] [2025-01-10T12:00:00Z] [traj-abc123] [core] [FORMULA_COMPUTED] {
  "formula": "CORE-1",
  "inputs": {"I": 0.8, "P": 0.6, "S_a": 0.7, "H": 0.3},
  "output": 0.2352
}
```

---

## Debug Workflow

### Step 1: Find Trace
```
Query: trace_id = "traj-abc123"
```

### Step 2: View Events
```
Events in order:
1. ENERGY_PROJECTED
2. FORMULA_COMPUTED (CORE-1)
3. FORMULA_COMPUTED (CORE-2)
4. TRAJECTORY_CREATED
5. GATE_EVALUATED
```

### Step 3: Verify Formulas
```
For each FORMULA_COMPUTED:
- Check inputs match expected
- Check output matches formula
- Check dependencies satisfied
```

### Step 4: Trace Decision
```
GATE_EVALUATED:
- Check all metrics
- Verify decision logic
- Check reasons
```

---

## Implementation Requirements

### Must Have
- ✅ Unique trace_id per trajectory
- ✅ Event logging for all major operations
- ✅ Formula computation logging
- ✅ Decision logging
- ✅ Structured log format

### Should Have
- ⚠️ Log aggregation
- ⚠️ Query interface
- ⚠️ Visualization tools

### Nice to Have
- 💡 Real-time monitoring
- 💡 Alert system
- 💡 Performance metrics

---

## Version History

- **v1.0-LOCKED**: Initial event & trace system specification

---

## Notes

- **Lock Status**: LOCKED — Trace system must be implemented from start
- **Review Process**: ต้องผ่าน technical review ก่อนแก้ไข
- **Impact**: Trace system กระทบ debugging และ auditing

