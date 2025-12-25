# Cogman Gate - Specifications

**Version:** v1.0-LOCKED  
**Status:** LOCKED — 6 Base Specifications

---

## Overview

เอกสาร 6 ฐาน (BASE) นี้คือ "ของที่ถ้าไม่วางวันนี้ จะเจ็บวันหน้า"

แต่ละฐานเป็น foundation ที่ต้องล็อกก่อนพัฒนาต่อ

---

## The 6 Bases

### BASE-1: Canonical Definitions
**File:** `BASE-1_CANONICAL_DEFINITIONS.md`

**Purpose:** นิยามศูนย์กลางที่ต้องล็อก ไม่งั้นทุกอย่างจะ drift

**Contents:**
- Trajectory definition
- Energy definition
- Memory definition
- Gate definition
- Core vs Interface

**Status:** LOCKED — ห้ามแก้ไขโดยไม่มีการ review

---

### BASE-2: Data Contracts
**File:** `BASE-2_DATA_CONTRACTS.md`

**Purpose:** Schema First Design — ต้องรู้ข้อมูลหน้าตาเป็นยังไงก่อน code

**Contents:**
- SensoryState schema
- EnergeticState (EPS-8) schema
- Trajectory schema
- GateVerdict schema

**Status:** LOCKED — Schema changes require review

---

### BASE-3: Formula Registry
**File:** `BASE-3_FORMULA_REGISTRY.md`

**Purpose:** สูตรเป็น First-Class Citizen

**Contents:**
- CORE-1 ถึง CORE-9 formulas
- Formula dependencies
- Input/output ranges
- Usage layers

**Status:** LOCKED — Formula changes require review

---

### BASE-4: Layer Responsibility Lock
**File:** `BASE-4_LAYER_RESPONSIBILITY_LOCK.md`

**Purpose:** Boundary Discipline — วางกฎเหล็กของแต่ละ layer

**Contents:**
- Layer responsibility matrix
- CAN DO / CANNOT DO rules
- Boundary violations
- Correct flow

**Status:** LOCKED — Layer boundaries must not be violated

---

### BASE-5: Event & Trace System
**File:** `BASE-5_EVENT_TRACE_SYSTEM.md`

**Purpose:** Debug-First Design — ถ้าไม่มี trace → ระบบนี้ "ไม่ใช่วิศวกรรม"

**Contents:**
- Trace ID format
- Event types
- Event schema
- Log format
- Formula mapping

**Status:** LOCKED — Trace system must be implemented from start

---

### BASE-6: Legal / Meaning Lock
**File:** `BASE-6_LEGAL_MEANING_LOCK.md`

**Purpose:** มาตรฐาน & ป้องกันการตีความผิด

**Contents:**
- Disclaimer template
- Mode flag (ENGINEERING_SIM)
- No-clinical assertion
- Terminology lock
- Legal boundaries

**Status:** LOCKED — Legal/meaning boundaries must not be violated

---

## Usage

### Reading Order

1. **BASE-1** - อ่านก่อนเพื่อเข้าใจ definitions
2. **BASE-2** - อ่านเพื่อเข้าใจ data structures
3. **BASE-3** - อ่านเพื่อเข้าใจ formulas
4. **BASE-4** - อ่านเพื่อเข้าใจ layer boundaries
5. **BASE-5** - อ่านเพื่อเข้าใจ trace system
6. **BASE-6** - อ่านเพื่อเข้าใจ legal/meaning boundaries

### Reference

- อ้างอิง BASE documents ใน code comments
- อ้างอิง BASE documents ใน design documents
- อ้างอิง BASE documents ใน reviews

---

## Lock Status

**All BASE documents are LOCKED**

- ห้ามแก้ไขโดยไม่มีการ review
- Review process ต้องเป็น formal
- Changes ต้อง documented และ traceable

---

## Version History

- **v1.0-LOCKED**: Initial 6 base specifications

---

## Notes

- **Foundation**: เอกสารเหล่านี้เป็น foundation ของระบบ
- **Mandatory**: ต้องมีก่อนพัฒนาต่อ
- **Immutable**: ห้ามแก้ไขโดยไม่มีการ review

