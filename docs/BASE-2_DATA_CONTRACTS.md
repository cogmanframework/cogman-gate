# BASE-2: Data Contracts

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Schema First Design

---

## Purpose

ก่อน code → ต้องรู้ว่า "ข้อมูลหน้าตาเป็นยังไง"

**Schema = สัญญา**  
**Code เปลี่ยนได้ แต่ schema เปลี่ยนต้อง review**

---

## Core Principles

### 📌 Schema First
- กำหนด schema ก่อนเขียน code
- Schema เป็น contract ระหว่าง modules
- Schema ต้อง versioned และ backward compatible

### 📌 Validation
- ทุก input/output ต้อง validate ตาม schema
- Schema violation = system error
- Schema เป็น single source of truth

---

## Data Contracts

### 1. SensoryState

**Purpose:** ข้อมูลจาก sensory input (text, image, audio, etc.)

**Schema:**
```json
{
  "modality": "text|image|audio|sensor|manual",
  "features": {
    "vector": [0.0, 0.0, ...],
    "metadata": {}
  },
  "timestamp": "ISO8601_datetime",
  "source_id": "string",
  "session_id": "string"
}
```

**Fields:**
- `modality`: ประเภทของ input (enum)
- `features`: Feature vector และ metadata
- `timestamp`: เวลาที่รับ input
- `source_id`: Identifier ของ source
- `session_id`: Session identifier

**Constraints:**
- `modality` ต้องเป็นค่าที่กำหนดไว้
- `timestamp` ต้องเป็น valid ISO8601
- `source_id` และ `session_id` ต้องไม่ว่าง

**Usage:**
- Input จาก sensory layer
- ใช้ในการคำนวณ IPSH components
- ใช้ในการสร้าง initial state

---

### 2. EnergeticState (EPS-8)

**Purpose:** สถานะพลังงานของระบบ (Energy Projection System - 8 components)

**Schema:**
```json
{
  "I": 0.0,
  "P": 0.0,
  "S": 0.0,
  "H": 0.0,
  "A": 0.0,
  "S_a": 0.0,
  "E_mu": 0.0,
  "theta": 0.0
}
```

**Fields:**
- `I`: Intensity [I ≥ 0]
- `P`: Polarity [P ∈ ℝ]
- `S`: Stability [0 ≤ S ≤ 1]
- `H`: Entropy/Uncertainty [0 ≤ H ≤ 1]
- `A`: Awareness [0 ≤ A ≤ 1]
- `S_a`: Sub-awareness/Background activation [0 ≤ S_a ≤ 1]
- `E_mu`: Internal Energy Metric [E_mu ∈ ℝ]
- `theta`: Theta phase [0 ≤ theta < 2π]

**Constraints:**
- ทุก field ต้องอยู่ใน range ที่กำหนด
- NaN และ Infinity ไม่ได้รับอนุญาต
- ต้อง validate ก่อนใช้ใน formulas

**Usage:**
- Input สำหรับ Core formulas
- ใช้ในการคำนวณพลังงาน
- ใช้ในการตัดสินใจ

---

### 3. Trajectory

**Purpose:** Physical object ที่เป็นลำดับของ states

**Schema:**
```json
{
  "trace_id": "uuid",
  "state_0": {
    "I": 0.0,
    "P": 0.0,
    "S": 0.0,
    "H": 0.0,
    "A": 0.0,
    "S_a": 0.0
  },
  "states": [
    {
      "timestamp": "ISO8601_datetime",
      "state": {...},
      "energy": {...}
    }
  ],
  "metadata": {
    "created_at": "ISO8601_datetime",
    "origin": "string",
    "tags": []
  }
}
```

**Fields:**
- `trace_id`: Unique identifier (UUID)
- `state_0`: Initial state (S₀)
- `states`: Sequence of states with timestamps
- `metadata`: Additional metadata

**Constraints:**
- `trace_id` ต้องเป็น valid UUID
- `state_0` ต้องเป็น valid EnergeticState
- `states` เป็น append-only (immutable sequence)
- `metadata.created_at` ต้องไม่ว่าง

**Usage:**
- ใช้ในการติดตาม evolution
- ใช้ในการ recall memory
- ใช้ในการทำ resonance matching

---

### 4. GateVerdict

**Purpose:** ผลลัพธ์จาก Decision Gate

**Schema:**
```json
{
  "decision": "ALLOW|REVIEW|BLOCK",
  "reason": [
    "rule_fail",
    "E_mu_in_restrict",
    "H_high",
    "D_traj_high"
  ],
  "metrics": {
    "E_mu": 0.0,
    "H": 0.0,
    "D_traj": 0.0,
    "rule_fail": false
  },
  "timestamp": "ISO8601_datetime",
  "trace_id": "uuid"
}
```

**Fields:**
- `decision`: Decision verdict (enum)
- `reason`: Array of reasons (why this decision)
- `metrics`: Metrics used in decision
- `timestamp`: When decision was made
- `trace_id`: Associated trajectory ID

**Constraints:**
- `decision` ต้องเป็น ALLOW, REVIEW, หรือ BLOCK
- `reason` array ต้องไม่ว่างถ้า decision ≠ ALLOW
- `metrics` ต้องมีค่าที่ใช้ในการตัดสินใจ
- `timestamp` ต้องเป็น valid ISO8601

**Usage:**
- Output จาก Decision Gate
- ใช้ในการควบคุม flow
- ใช้ในการ audit และ debug

---

## Schema Versioning

### Version Format
```
v<major>.<minor>.<patch>
```

### Rules
- **Major version**: Breaking changes (require migration)
- **Minor version**: New fields (backward compatible)
- **Patch version**: Bug fixes (backward compatible)

### Migration
- Schema changes ต้องมี migration plan
- ต้องรองรับ backward compatibility
- ต้องมี deprecation period

---

## Validation

### Input Validation
- ทุก input ต้อง validate ตาม schema
- Schema violation = reject with error
- Error message ต้องชัดเจน

### Output Validation
- ทุก output ต้อง validate ตาม schema
- Schema violation = system error
- ต้อง log และ alert

---

## Examples

### Example 1: SensoryState
```json
{
  "modality": "text",
  "features": {
    "vector": [0.1, 0.2, 0.3],
    "metadata": {
      "length": 10,
      "language": "en"
    }
  },
  "timestamp": "2025-01-10T12:00:00Z",
  "source_id": "user_input_001",
  "session_id": "session_abc123"
}
```

### Example 2: EnergeticState
```json
{
  "I": 0.8,
  "P": 0.6,
  "S": 0.7,
  "H": 0.3,
  "A": 0.5,
  "S_a": 0.6,
  "E_mu": 0.4,
  "theta": 1.5
}
```

### Example 3: Trajectory
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "state_0": {
    "I": 0.8,
    "P": 0.6,
    "S": 0.7,
    "H": 0.3,
    "A": 0.5,
    "S_a": 0.6
  },
  "states": [],
  "metadata": {
    "created_at": "2025-01-10T12:00:00Z",
    "origin": "sensory_input",
    "tags": ["initial"]
  }
}
```

### Example 4: GateVerdict
```json
{
  "decision": "ALLOW",
  "reason": [],
  "metrics": {
    "E_mu": 0.3,
    "H": 0.3,
    "D_traj": 0.2,
    "rule_fail": false
  },
  "timestamp": "2025-01-10T12:00:01Z",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Version History

- **v1.0-LOCKED**: Initial data contracts

---

## Notes

- **Lock Status**: LOCKED — Schema changes require review
- **Review Process**: ต้องผ่าน technical review ก่อนแก้ไข
- **Impact**: Schema changes กระทบทั้งระบบ

