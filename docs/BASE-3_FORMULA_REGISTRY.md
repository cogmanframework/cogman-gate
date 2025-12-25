# BASE-3: Formula Registry

**Version:** v1.0-LOCKED  
**Status:** LOCKED — สูตรเป็น First-Class Citizen

---

## Purpose

**สูตรเป็น First-Class Citizen**

**ไม่มีสูตร = ไม่มี logic**  
**ห้ามมีสูตรซ้ำความหมาย**  
**ห้ามสูตรฝังใน code โดยไม่อยู่ registry**

---

## Core Principles

### 📌 Formula First
- ทุกสูตรต้องอยู่ใน registry
- ไม่มีสูตรซ่อนอยู่ใน code
- สูตรต้องมี documentation ครบ

### 📌 Single Source of Truth
- Registry เป็นแหล่งเดียวของสูตร
- Code ต้องอ้างอิงกลับมาที่ registry
- เปลี่ยนสูตร = เปลี่ยน registry

---

## Formula Template

ทุกสูตรต้องมี:

- **Name**: ชื่อสูตร
- **Purpose**: จุดประสงค์
- **Formula**: สมการ
- **Input range**: ช่วงค่าของ input
- **Output range**: ช่วงค่าของ output
- **Dependency**: สูตรที่ต้องใช้ก่อน
- **Usage layer**: Layer ที่ใช้สูตรนี้

---

## Core Formulas (CCK)

### CORE-1: ΔEΨ — Energy of Perception

**Name:** ΔEΨ (Energy of Perception)

**Purpose:**
- ดัชนีพลังงานของการรับรู้
- ใช้ตัดสินว่า "จะเกิด trajectory หรือไม่"
- ป้องกัน noise / hallucination ตั้งแต่ต้น

**Formula:**
```
ΔEΨ = I × |P| × S_a × (1 − H)
```

**Input Range:**
- `I`: [0, ∞)
- `P`: (-∞, ∞)
- `S_a`: [0, 1]
- `H`: [0, 1]

**Output Range:**
- `ΔEΨ`: [0, ∞)

**Dependency:**
- None (foundation formula)

**Used in:**
- Trajectory Builder (Admission Gate)
- Perception Layer

**Status:** LOCKED (Canonical Core)

---

### CORE-2: E_reflex — Reflex Energy

**Name:** E_reflex (Reflex Energy)

**Purpose:**
- พลังงานปฏิกิริยาทันทีหลังการรับรู้
- ใช้กำหนดว่าจะ "ตอบสนองเร็ว" หรือ "รอประมวลผล"

**Formula:**
```
E_reflex = ΔEΨ × (1 + A)
```

**Input Range:**
- `ΔEΨ`: [0, ∞)
- `A`: [0, 1]

**Output Range:**
- `E_reflex`: [0, ∞)

**Dependency:**
- CORE-1 (ΔEΨ)

**Used in:**
- Reflex Layer
- Decision Gate

**Status:** LOCKED (Canonical Core)

---

### CORE-3: ΔEΨ_theta — Directional Reflex Energy

**Name:** ΔEΨ_theta (Directional Reflex Energy)

**Purpose:**
- พลังงาน reflex ที่มีทิศทาง
- ใช้ควบคุมการหันของ reasoning

**Formula:**
```
ΔEΨ_theta = ΔEΨ × theta_phase × 0.2
```

**Input Range:**
- `ΔEΨ`: [0, ∞)
- `theta_phase`: [0, 2π)

**Output Range:**
- `ΔEΨ_theta`: [0, ∞)

**Dependency:**
- CORE-1 (ΔEΨ)

**Used in:**
- Reflex Layer
- Directional Control

**Status:** LOCKED (Canonical Core)

---

### CORE-4: E_mind — Cognitive Energy

**Name:** E_mind (Cognitive Energy)

**Purpose:**
- พลังงานสำหรับการสร้างความหมายและโครงสร้างเชิงเหตุผล
- เกิดหลังการรับรู้ ไม่ใช่ reflex

**Formula:**
```
E_mind = (I + A + (1 − H)) / 3
```

**Input Range:**
- `I`: [0, ∞)
- `A`: [0, 1]
- `H`: [0, 1]

**Output Range:**
- `E_mind`: [0, 1]

**Dependency:**
- None (independent)

**Used in:**
- Cognitive Layer
- Reasoning Layer

**Status:** LOCKED (Canonical Core)

---

### CORE-5: E_coherence — Coherence Energy

**Name:** E_coherence (Coherence Energy)

**Purpose:**
- ระดับความสอดคล้องภายในของระบบ
- ใช้ดูว่าความคิด "แตก" หรือ "รวมตัวดี"

**Formula:**
```
E_coherence = (S + A + (1 − H)) / 3
```

**Input Range:**
- `S`: [0, 1]
- `A`: [0, 1]
- `H`: [0, 1]

**Output Range:**
- `E_coherence`: [0, 1]

**Dependency:**
- None (independent)

**Used in:**
- Coherence Layer
- Binding Energy

**Status:** LOCKED (Canonical Core)

---

### CORE-6: E_neural — Neuro-Energetic Sum

**Name:** E_neural (Neuro-Energetic Sum)

**Purpose:**
- ผลรวมพลังงานเชิงระบบประสาท (เชิงสัญลักษณ์)
- Interface/placeholder ที่สามารถ implement ได้หลายแบบ

**Formula:**
```
E_neural = dopamine + serotonin + oxytocin + adrenaline + cortisol
```

**Input Range:**
- `dopamine`: [0, ∞)
- `serotonin`: [0, ∞)
- `oxytocin`: [0, ∞)
- `adrenaline`: [0, ∞)
- `cortisol`: [0, ∞)

**Output Range:**
- `E_neural`: [0, ∞)

**Dependency:**
- None (interface)

**Used in:**
- Neural Layer
- Binding Energy

**Status:** LOCKED (Canonical Core - Interface)

---

### CORE-7: E_bind — Binding Energy

**Name:** E_bind (Binding Energy)

**Purpose:**
- พลังงานการเชื่อมโยงระหว่างการรับรู้ + ความคิด + สถานะระบบ
- ใช้ก่อนการบันทึกความจำ

**Formula:**
```
E_bind = E_mind × E_neural × E_coherence
```

**Input Range:**
- `E_mind`: [0, ∞)
- `E_neural`: [0, ∞)
- `E_coherence`: [0, ∞)

**Output Range:**
- `E_bind`: [0, ∞)

**Dependency:**
- CORE-4 (E_mind)
- CORE-6 (E_neural)
- CORE-5 (E_coherence)

**Used in:**
- Binding Layer
- Memory Encoding

**Status:** LOCKED (Canonical Core)

---

### CORE-8: E_mem — Memory Encoding Energy

**Name:** E_mem (Memory Encoding Energy)

**Purpose:**
- พลังงานที่ใช้ตัดสินว่าควรบันทึกความจำหรือไม่

**Formula:**
```
E_mem = A × E_bind × E_pred
```

**Input Range:**
- `A`: [0, 1]
- `E_bind`: [0, ∞)
- `E_pred`: [0, ∞)

**Output Range:**
- `E_mem`: [0, ∞)

**Dependency:**
- CORE-7 (E_bind)
- E_pred (external)

**Used in:**
- Memory Layer
- Encoding Decision

**Status:** LOCKED (Canonical Core)

---

### CORE-9: G_decision — Decision Gate Verdict

**Name:** G_decision (Decision Gate Verdict)

**Purpose:**
- ผลลัพธ์การตัดสินใจเชิงวิศวกรรม
- ไม่มีการเรียนรู้สด
- ตรวจสอบได้ ย้อนรอยได้

**Formula:**
```
Logic:
  IF rule_fail → BLOCK
  IF Eμ ∈ restrict → BLOCK
  IF H high OR D_traj high → REVIEW
  ELSE → ALLOW
```

**Input Range:**
- `rule_fail`: boolean
- `Eμ`: (-∞, ∞)
- `restrict`: [restrict_min, restrict_max]
- `H`: [0, 1]
- `D_traj`: [0, ∞)

**Output Range:**
- `decision`: {ALLOW, REVIEW, BLOCK}

**Dependency:**
- Eμ (external)
- H (from state)
- D_traj (external)

**Used in:**
- Decision Gate
- Safety Layer

**Status:** LOCKED (Canonical Core)

---

## Formula Dependency Graph

```
CORE-1: ΔEΨ
  ├─→ CORE-2: E_reflex
  └─→ CORE-3: ΔEΨ_theta

CORE-4: E_mind
CORE-5: E_coherence
CORE-6: E_neural
  │
  └─→ CORE-7: E_bind
        │
        └─→ CORE-8: E_mem

CORE-9: G_decision (uses Eμ, H, D_traj)
```

---

## Formula Rules

### Rule 1: No Hidden Formulas
- ทุกสูตรต้องอยู่ใน registry
- ห้ามมีสูตรซ่อนอยู่ใน code
- Code ต้องอ้างอิงกลับมาที่ registry

### Rule 2: No Duplicate Meanings
- ห้ามมีสูตรซ้ำความหมาย
- ถ้าต้องการ variant ต้องระบุชัดเจน
- ต้องมี justification สำหรับ variant

### Rule 3: Formula First
- กำหนดสูตรก่อนเขียน code
- Code เป็น implementation ของสูตร
- เปลี่ยนสูตร = เปลี่ยน registry ก่อน

---

## Version History

- **v1.0-LOCKED**: Initial formula registry (9 core formulas)

---

## Notes

- **Lock Status**: LOCKED — Formula changes require review
- **Review Process**: ต้องผ่าน formal review ก่อนแก้ไข
- **Impact**: Formula changes กระทบทั้งระบบ
- **Reference**: ดูรายละเอียดใน `COGMAN_CORE_KERNEL.md`

