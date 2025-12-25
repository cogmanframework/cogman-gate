# Kernel ↔ Perceptual Energy Interface Specification

**Version:** v1.0-LOCKED  
**Status:** LOCKED - Interface contract between Kernel and Perceptual Energy Mapping

---

## Overview

เอกสารนี้อธิบาย **interface contract** ระหว่าง:
- **Perceptual Energy Mapping** (Pre-Kernel Layer)
- **Kernel Energy Core** (C++)

---

## What Kernel Guarantees

### ✅ Kernel Accepts

Kernel **รับและประมวลผล** PEU (Perceptual Energy Unit) โดย:

1. **Parameter Validation**
   - ตรวจสอบ range ของ I, P, S, H
   - Validate phase ∈ [0, 2π]
   - Check freq ≥ 0

2. **Type Conversion**
   - PEU → EPS-8 State
   - Mapping: `{I, P, S, H, phase, freq}` → `{I, P, S, H, A, S_a, theta}`

3. **Formula Application**
   - ใช้ CORE-1 ถึง CORE-9 กับ validated parameters
   - ไม่ตีความความหมายของ parameters

4. **Deterministic Output**
   - Same PEU input → same energy output
   - ไม่ขึ้นกับ source ของ PEU

---

## What Kernel Ignores

### ❌ Kernel Does NOT Use

Kernel **ไม่ใช้และไม่สนใจ**:

1. **Semantic Meaning**
   - `phrase` string → ไม่ใช้
   - `role` classification → ไม่ใช้
   - Language information → ไม่ใช้

2. **Confidence Score**
   - `confidence` → ไม่ใช้ในการคำนวณ
   - ใช้เฉพาะ trace/audit

3. **Source Version**
   - `version` → ไม่ใช้ในการคำนวณ
   - ใช้เฉพาะ trace/audit

4. **Heuristic Details**
   - วิธีการ extract phrase → ไม่สนใจ
   - Language-specific logic → ไม่สนใจ
   - Mapping algorithm → ไม่สนใจ

---

## Parameter Mapping

### PEU → EPS-8 State

| PEU Parameter | EPS-8 Field | Mapping Rule |
|-------------|-------------|--------------|
| `I` | `I` | Direct (validate range) |
| `P` | `P` | Direct (validate range) |
| `S` | `S` | Direct (validate range) |
| `H` | `H` | Direct (validate range) |
| `phase` | `theta` | Direct (validate [0, 2π]) |
| `freq` | - | Not used in EPS-8 |
| - | `A` | Derived from I, S (kernel logic) |
| - | `S_a` | Derived from S, H (kernel logic) |
| - | `F` | Set to 0.0 (external force) |

### Derived Fields

```cpp
// Kernel derives A and S_a from PEU parameters
A = f(I, S)      // Awareness from Intensity and Stability
S_a = g(S, H)    // Sub-awareness from Stability and Entropy
```

---

## Validation Rules

### Input Validation (Kernel Side)

```cpp
bool validate_peu(const PEU& peu) {
    // Range checks
    if (peu.I < 0.0 || peu.I > 1.0) return false;
    if (peu.P < -1.0 || peu.P > 1.0) return false;
    if (peu.S < 0.0 || peu.S > 1.0) return false;
    if (peu.H < 0.0 || peu.H > 1.0) return false;
    if (peu.phase < 0.0 || peu.phase > 2*M_PI) return false;
    if (peu.freq < 0.0) return false;
    
    // Role enum check
    if (peu.role not in ["goal", "action", "modifier", "context"]) return false;
    
    return true;
}
```

### Error Handling

- **Invalid Range:** Return error, do not proceed
- **Missing Field:** Use default value (documented)
- **Unknown Role:** Ignore role, proceed with parameters

---

## Trace & Audit

### Kernel Logs

Kernel **บันทึก** (แต่ไม่ใช้):
- PEU `version` → สำหรับ audit
- PEU `trace_id` → สำหรับ lineage
- PEU `confidence` → สำหรับ debugging

### Kernel Does NOT Log
- `phrase` content → ไม่บันทึก (privacy)
- Language information → ไม่บันทึก
- Heuristic details → ไม่บันทึก

---

## Version Compatibility

### PEU Version Tracking

```
PEU {version: "1.0"} → Kernel accepts
PEU {version: "2.0"} → Kernel accepts (if compatible)
PEU {version: "unknown"} → Kernel accepts (with warning)
```

**Kernel ไม่ reject PEU ตาม version**  
**แต่บันทึก version เพื่อ audit**

---

## Interface Guarantees

### Kernel Guarantees

1. ✅ **Same PEU → Same Energy**
   - Deterministic mapping
   - No side effects

2. ✅ **Parameter Validation**
   - Reject invalid ranges
   - Use safe defaults

3. ✅ **No Semantic Dependency**
   - Works with any PEU source
   - Language-agnostic

4. ✅ **Audit Trail**
   - Logs PEU metadata
   - Preserves traceability

### Perceptual Energy Mapping Guarantees

1. ✅ **Valid Range Output**
   - I, P, S, H in valid ranges
   - phase in [0, 2π]

2. ✅ **Version Tagging**
   - Every PEU has version
   - Traceable to extractor

3. ✅ **No Kernel Logic**
   - Does not compute energy
   - Does not call gate

---

## Summary

### Kernel Perspective

**"ฉันรับตัวเลข ฉันคำนวณพลังงาน ฉันไม่สนใจว่าตัวเลขมาจากไหน"**

### Perceptual Energy Mapping Perspective

**"ฉันแปลงสัญญาณเป็นตัวเลข ฉันไม่คำนวณพลังงาน ฉันไม่ตัดสินใจ"**

---

## Reference

- **Perceptual Energy Mapping Spec:** `PERCEPTUAL_ENERGY_MAPPING_SPEC.md`
- **Kernel Core Spec:** `COGMAN_CORE_KERNEL.md`
- **Interface Contract:** `PerceptualEnergyContract.json`

---

**Status:** LOCKED v1.0  
**Last Updated:** 2024

