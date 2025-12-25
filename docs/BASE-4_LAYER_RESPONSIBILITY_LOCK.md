# BASE-4: Layer Responsibility Lock

**Version:** v1.0-LOCKED  
**Status:** LOCKED — Boundary Discipline

---

## Purpose

วาง "กฎเหล็ก" ของแต่ละ layer ตั้งแต่วันแรก

**นี่คือสิ่งที่ทำให้:**
- ระบบไม่เละ
- ทีมไม่เถียง
- IP แข็ง

---

## Core Principles

### 📌 Single Responsibility
- แต่ละ layer มีหน้าที่เดียว
- Layer ไม่ทำหน้าที่ของ layer อื่น
- Boundary ชัดเจน

### 📌 No Leakage
- Logic ไม่รั่วไหลข้าม layer
- Data flow ชัดเจน
- Interface เป็น contract

---

## Layer Responsibility Matrix

| Layer | CAN DO | CANNOT DO | Interface |
|-------|--------|-----------|-----------|
| **Sensory** | • รับ input<br>• แปลงเป็น features<br>• ส่งต่อ state | ❌ ห้ามคิด<br>❌ ห้ามตัดสิน<br>❌ ห้ามรู้ความหมาย | → EnergeticState |
| **Encoder** | • แปลง features → IPSH<br>• Normalize data<br>• Validate input | ❌ ห้ามตัดสิน<br>❌ ห้ามรู้ความหมาย<br>❌ ห้ามเขียน trajectory | → EnergeticState |
| **Core** | • คำนวณพลังงาน<br>• ใช้สูตร CORE-1 ถึง CORE-9<br>• ส่งต่อ energy | ❌ ห้ามรู้ความหมาย<br>❌ ห้ามตัดสินใจ<br>❌ ห้ามเรียนรู้ | → EnergyState |
| **Gate** | • ตรวจสอบ constraints<br>• ตัดสิน ALLOW/REVIEW/BLOCK<br>• Log decision | ❌ ห้ามเรียนรู้<br>❌ ห้ามปรับ threshold<br>❌ ห้ามรู้ความหมาย | → GateVerdict |
| **Memory** | • เก็บ patterns<br>• Recall by resonance<br>• Decay over time | ❌ ห้ามคิด<br>❌ ห้ามตัดสิน<br>❌ ห้ามสร้าง trajectory | → MemoryPattern |
| **LLM** | • Generate text<br>• Process language<br>• Return response | ❌ ห้ามเขียน trajectory<br>❌ ห้ามแก้ Core formulas<br>❌ ห้ามตัดสิน Gate | → TextResponse |
| **Trajectory Builder** | • สร้าง trajectory<br>• จัดการ state sequence<br>• Track evolution | ❌ ห้ามคิดเอง<br>❌ ห้ามตัดสิน<br>❌ ห้ามรู้ความหมาย | → Trajectory |

---

## Detailed Layer Rules

### Sensory Layer

**Responsibility:**
- รับ input จาก external sources
- แปลงเป็น feature vectors
- ส่งต่อเป็น EnergeticState

**CAN DO:**
- ✅ รับ text, image, audio, sensor data
- ✅ Extract features
- ✅ Normalize input
- ✅ Add metadata (timestamp, source_id)

**CANNOT DO:**
- ❌ ห้ามคิดหรือ reasoning
- ❌ ห้ามตัดสินใจ
- ❌ ห้ามรู้ความหมายของ input
- ❌ ห้ามสร้าง trajectory

**Interface:**
- Input: Raw data (text, image, audio, etc.)
- Output: `SensoryState` → `EnergeticState`

---

### Encoder Layer

**Responsibility:**
- แปลง features → IPSH components
- Validate และ normalize
- ส่งต่อเป็น EnergeticState

**CAN DO:**
- ✅ แปลง features → I, P, S, H
- ✅ Calculate A, S_a
- ✅ Validate ranges
- ✅ Normalize values

**CANNOT DO:**
- ❌ ห้ามตัดสินใจ
- ❌ ห้ามรู้ความหมาย
- ❌ ห้ามเขียน trajectory
- ❌ ห้ามแก้ Core formulas

**Interface:**
- Input: `SensoryState`
- Output: `EnergeticState`

---

### Core Layer

**Responsibility:**
- คำนวณพลังงานตามสูตร CORE-1 ถึง CORE-9
- ส่งต่อ energy values

**CAN DO:**
- ✅ ใช้สูตร CORE-1 ถึง CORE-9
- ✅ คำนวณพลังงาน
- ✅ Validate inputs
- ✅ Return energy values

**CANNOT DO:**
- ❌ ห้ามรู้ความหมาย
- ❌ ห้ามตัดสินใจ
- ❌ ห้ามเรียนรู้
- ❌ ห้ามแก้สูตร

**Interface:**
- Input: `EnergeticState`
- Output: `EnergyState`

---

### Gate Layer

**Responsibility:**
- ตรวจสอบ constraints
- ตัดสิน ALLOW/REVIEW/BLOCK
- Log decision

**CAN DO:**
- ✅ ตรวจสอบ rule violations
- ✅ ตรวจสอบ Eμ range
- ✅ ตรวจสอบ H และ D_traj
- ✅ ตัดสินและ log

**CANNOT DO:**
- ❌ ห้ามเรียนรู้
- ❌ ห้ามปรับ threshold (ต้องกำหนดล่วงหน้า)
- ❌ ห้ามรู้ความหมาย
- ❌ ห้ามแก้ Core formulas

**Interface:**
- Input: `EnergyState`, `DecisionParams`
- Output: `GateVerdict`

---

### Memory Layer

**Responsibility:**
- เก็บ patterns เป็น attractor states
- Recall by resonance
- Decay over time

**CAN DO:**
- ✅ เก็บ episodic/semantic/procedural memory
- ✅ Recall by resonance matching
- ✅ Apply decay
- ✅ Consolidate (episodic → semantic)

**CANNOT DO:**
- ❌ ห้ามคิดเอง
- ❌ ห้ามตัดสินใจ
- ❌ ห้ามสร้าง trajectory
- ❌ ห้ามรู้ความหมาย

**Interface:**
- Input: `EnergyState`, `MemoryPattern`
- Output: `MemoryPattern`, `ResonanceScore`

---

### LLM Layer

**Responsibility:**
- Generate text
- Process language
- Return response

**CAN DO:**
- ✅ Generate text from prompts
- ✅ Process language
- ✅ Return text response

**CANNOT DO:**
- ❌ ห้ามเขียน trajectory
- ❌ ห้ามแก้ Core formulas
- ❌ ห้ามตัดสิน Gate
- ❌ ห้ามรู้ internal state

**Interface:**
- Input: `TextPrompt`
- Output: `TextResponse`

---

### Trajectory Builder Layer

**Responsibility:**
- สร้าง trajectory
- จัดการ state sequence
- Track evolution

**CAN DO:**
- ✅ สร้าง trajectory จาก state_0
- ✅ Append states
- ✅ Track evolution
- ✅ Manage trace_id

**CANNOT DO:**
- ❌ ห้ามคิดเอง
- ❌ ห้ามตัดสินใจ
- ❌ ห้ามรู้ความหมาย
- ❌ ห้ามแก้ Core formulas

**Interface:**
- Input: `EnergeticState`, `EnergyState`
- Output: `Trajectory`

---

## Boundary Violations

### ❌ Common Violations

1. **Sensory → Core**: Sensory layer คำนวณพลังงานเอง
2. **Core → Gate**: Core layer ตัดสินใจเอง
3. **Gate → Memory**: Gate layer เขียน memory เอง
4. **Memory → Trajectory**: Memory layer สร้าง trajectory เอง
5. **LLM → Core**: LLM layer แก้ Core formulas

### ✅ Correct Flow

```
Sensory → Encoder → Core → Gate → Trajectory
                ↓
            Memory (passive)
                ↓
            LLM (external)
```

---

## Enforcement

### Code Level
- Interface contracts
- Type checking
- Compile-time constraints

### Runtime Level
- Validation checks
- Boundary assertions
- Error logging

### Review Level
- Code review checklist
- Architecture review
- Design review

---

## Version History

- **v1.0-LOCKED**: Initial layer responsibility lock

---

## Notes

- **Lock Status**: LOCKED — Layer boundaries must not be violated
- **Review Process**: ต้องผ่าน architecture review ก่อนแก้ไข
- **Impact**: Boundary violations กระทบทั้งระบบ

