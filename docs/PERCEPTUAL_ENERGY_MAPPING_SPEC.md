# 📘 Perceptual Energy Mapping Specification

**(PhraseExtractor / Pre-Kernel Layer)**

**Version:** v1.0 – LOCKED  
**Status:** Canonical / Production-Safe  
**Scope:** Text → Energetic Parameters  
**Layer:** Perception (Pre-Kernel)

---

## 0) Lock Meaning (สำคัญมาก)

เอกสารนี้อธิบาย **Perceptual Energy Mapping**  
ซึ่งเป็น **Conceptual / Engineering Analogy**  
**ไม่ใช่สมองจริง ไม่ใช่ฟิสิกส์จริง และไม่ใช่จิตวิทยาคลินิก**

- ❌ **ไม่ใช่** AI reasoning
- ❌ **ไม่ใช่** decision making
- ❌ **ไม่ใช่** physics simulation
- ✅ **เป็น** signal → parameter mapping

---

## 1) Purpose (วัตถุประสงค์)

**Perceptual Energy Mapping** มีหน้าที่:

แปลง raw signal (text)  
→ energetic parameters (I, P, S, H, phase, freq)  
เพื่อป้อนเข้าสู่ Kernel Energy Formulas

### ใช้เพื่อ
- เตรียมข้อมูลสำหรับ ΔEΨ / CORE formulas
- แยก perception ออกจาก computation
- ทำให้ kernel เป็น math-only และ audit-safe

### ไม่ใช้เพื่อ
- ตัดสินใจ
- คำนวณสูตรพลังงานหลัก
- อธิบายความหมายเชิงมนุษย์

---

## 2) Position in Architecture

```
[Sensory Input]
      ↓
[Perceptual Energy Mapping]   ← (THIS SPEC)
      ↓
[Kernel Energy Core (C++)]
      ↓
[Gate / Reasoning / Action]
```

⚠️ **Layer นี้ ต้องอยู่ก่อน Kernel เสมอ**

---

## 3) Input / Output Contract

### 3.1 Input

```json
{
  "type": "text",
  "content": "string (raw text)",
  "language": "auto | th | en | ..."
}
```

- ไม่ require grammar correctness
- ไม่ require tokenization มาตรฐาน
- ไม่ normalize ความหมาย

---

### 3.2 Output (PEU – Perceptual Energy Unit)

```json
{
  "phrase": "string",
  "I": 0.0–1.0,
  "P": -1.0–+1.0,
  "S": 0.0–1.0,
  "H": 0.0–1.0,
  "phase": 0–2π,
  "freq": "float (Hz)",
  "role": "goal | action | modifier | context",
  "confidence": 0.0–1.0
}
```

**Output นี้ ยังไม่ใช่ energy จริง**  
เป็นเพียง parameter set สำหรับ kernel

---

## 4) Energetic Parameters Definition (Canonical)

### I — Intensity

ความแรงของสัญญาณที่รับรู้

- ขึ้นกับ: ความยาว, emphasis markers, action/goal words
- ❌ **ไม่ใช่** emotional intensity ของมนุษย์

---

### P — Polarity

ทิศทางเชิงบวก/ลบของสัญญาณ

- ประเมินจาก keyword polarity
- ถ้าไม่พบ → bias บวกเล็กน้อย
- ใช้เพื่อ absolute / sign handling ใน kernel

---

### S — Stability

ความสม่ำเสมอของ pattern

- common words → stable
- phrase ยาวเกิน → ลด stability
- ใช้เพื่อกรอง noise

---

### H — Entropy

ความไม่แน่นอนของสัญญาณ

- unique ratio
- single token → entropy สูง
- ใช้เป็น risk indicator เท่านั้น

---

### phase (θ)

มุมเฟสเชิงนามธรรม

- deterministic
- derived จาก content hash
- ❌ **ไม่ใช่** neural oscillation จริง

---

### freq

semantic rhythm (Hz)

- ใช้เพื่อ grouping / resonance
- ไม่เกี่ยวกับเวลาในโลกจริง

---

## 5) Phrase Boundary Detection (Non-Grammar)

**PhraseExtractor ไม่ใช้ grammar parser**

ใช้หลักการ:
- energy accumulation
- continuity
- boundary markers
- max phrase length

ออกแบบเพื่อรองรับ **ภาษาไม่มี space** (เช่น Thai)

---

## 6) Role Classification (Soft Semantic)

**Role มีไว้เพื่อ:**
- weighting
- grouping
- debug / trace

| Role | ความหมายเชิงระบบ |
|------|------------------|
| goal | intention marker |
| action | execution hint |
| modifier | intensity / quality |
| context | background |

❌ **role ไม่ใช้ตัดสินใจ**

---

## 7) Constraints (ห้ามละเมิด)

### ❌ Forbidden
- คำนวณ ΔEΨ
- เรียก Gate
- ตัดสิน ALLOW / BLOCK
- เขียน memory
- อ้างอิง physiology

### ✅ Allowed
- heuristic
- language-aware logic
- approximate mapping
- replaceable implementation

---

## 8) Determinism & Audit Policy

| คุณสมบัติ | สถานะ |
|---------|-------|
| deterministic | ⚠️ partial |
| traceable | ✅ |
| explainable | ✅ |
| reproducible | ✅ (same version) |

**ความไม่ deterministic ถูกจำกัดไว้เฉพาะ pre-kernel**

---

## 9) Versioning Policy
- PhraseExtractor ต้องมี version
- Parameter scaling เปลี่ยน → bump version
- Kernel ต้องรู้ source version ของ PEU

---

## 10) Security / IP Boundary
- Layer นี้ **ไม่ใช่ IP หลัก**
- Kernel formulas คือ **IP หลัก**
- สามารถ open-source layer นี้ได้โดยไม่กระทบ core

---

## 11) Summary (ฟันธง)

**PhraseExtractor = Perceptual Energy Mapper**  
**NOT Energy Engine**  
**NOT Decision Logic**  
**NOT Intelligence**

มันคือ:
- ตัวแปลงสัญญาณ → ตัวเลข
- ตัวเตรียมข้อมูล → สูตร
- ตัวกัน kernel จาก language & heuristic

---

## Reference

- **Kernel Spec:** `docs/COGMAN_CORE_KERNEL.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **Layer Responsibility:** `docs/BASE-4_LAYER_RESPONSIBILITY_LOCK.md`

---

**Status:** LOCKED v1.0  
**Last Updated:** 2024

