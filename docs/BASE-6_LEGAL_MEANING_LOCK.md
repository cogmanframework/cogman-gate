# BASE-6: Legal / Meaning Lock

**Version:** v1.0-LOCKED  
**Status:** LOCKED — มาตรฐาน & ป้องกันการตีความผิด

---

## Purpose

สิ่งนี้ไม่ใช่เรื่องเอกสารอย่างเดียว  
**มันต้องฝังในโครงสร้าง**

**ต้องมี:**
- Disclaimer template (ใช้ซ้ำ)
- Mode flag (ENGINEERING_SIM)
- No-clinical assertion
- Owner-defined thresholds only

---

## Core Principles

### 📌 Language Lock
**ใช้คำว่า:**
- ✅ "Mathematical models inspired by physics"
- ✅ "Engineering simulation"
- ✅ "Abstract energy metrics"

**ห้ามใช้คำว่า:**
- ❌ "simulation / brain / neuron" (ambiguous)
- ❌ "artificial intelligence" (too broad)
- ❌ "cognitive system" (clinical implication)

### 📌 Meaning Lock
- ไม่มีการตีความเชิงแพทย์
- ไม่มีการตีความเชิงจิตวิทยา
- ไม่มีการตีความเชิงจริยธรรม
- Engineering simulation เท่านั้น

---

## Disclaimer Template

### Standard Disclaimer

```
Copyright © 2025 Cogman™ Energetic Intelligence Framework. All Rights Reserved.

⚠️ IMPORTANT LEGAL AND ETHICAL BOUNDARIES

This system is a pure engineering simulation framework based on mathematical 
models inspired by physics. It is NOT classified as a medical device.

DISCLAIMERS:
- No medical diagnosis: This system does not diagnose, treat, or prevent 
  any medical condition.
- No psychological labeling: This system does not label, classify, or 
  evaluate human psychology.
- No human emotion inference: This system does not infer or interpret 
  human emotions.
- No autonomous moral reasoning: This system does not make autonomous 
  moral or ethical decisions.

USAGE REQUIREMENTS:
Clinical, psychiatric, or human-evaluative usage requires:
- Licensed supervisor
- Separate compliance layer
- Proper regulatory approval
- Ethical review board approval

This is a pure engineering simulation framework.
```

---

## Mode Flag

### ENGINEERING_SIM Mode

**Definition:**
Mode flag ที่ระบุว่าระบบทำงานในโหมด engineering simulation เท่านั้น

**Properties:**
- `ENGINEERING_SIM = true` (always)
- ไม่สามารถปิดได้
- ฝังใน code และ configuration

**Usage:**
```cpp
constexpr bool ENGINEERING_SIM = true;

if (!ENGINEERING_SIM) {
    throw std::runtime_error("System must run in ENGINEERING_SIM mode");
}
```

**Enforcement:**
- Compile-time check
- Runtime assertion
- Configuration validation

---

## No-Clinical Assertion

### Assertion Template

```
This system:
- Does NOT simulate biological processes
- Does NOT model neural activity
- Does NOT represent psychological states
- Does NOT make medical or clinical assessments

This system:
- Uses abstract mathematical models
- Applies physics-inspired equations
- Performs engineering simulations
- Processes data deterministically
```

### Code Assertion

```cpp
namespace cck {
    // No-clinical assertion
    static_assert(ENGINEERING_SIM, "System must be in ENGINEERING_SIM mode");
    
    // All formulas are abstract mathematical models
    // No biological or clinical interpretation
}
```

---

## Owner-Defined Thresholds Only

### Threshold Policy

**Rule:**
- Thresholds ต้องกำหนดโดย owner/system administrator
- ไม่มี hardcoded thresholds
- ไม่มี default thresholds ที่ตีความได้

**Implementation:**
```cpp
struct DecisionParams {
    double H_threshold;        // Must be set by owner
    double D_traj_threshold;   // Must be set by owner
    double restrict_min;       // Must be set by owner
    double restrict_max;       // Must be set by owner
};
```

**Validation:**
- Thresholds ต้อง validate ก่อนใช้
- Thresholds ต้อง log เมื่อตั้งค่า
- Thresholds ต้อง audit ได้

---

## Terminology Lock

### Approved Terms

| Term | Usage | Context |
|------|-------|---------|
| **Energy** | Abstract dimensionless scalar | Mathematical model |
| **State** | System state vector | Engineering |
| **Trajectory** | Sequence of states | Engineering |
| **Gate** | Deterministic judge | Engineering |
| **Memory** | Passive field storage | Engineering |
| **Resonance** | Pattern matching | Engineering |

### Prohibited Terms

| Term | Why Prohibited | Alternative |
|------|----------------|-------------|
| **Brain** | Biological implication | System |
| **Neuron** | Biological implication | Component |
| **Emotion** | Psychological implication | State |
| **Cognition** | Clinical implication | Processing |
| **Consciousness** | Philosophical implication | Awareness (as metric) |

---

## Documentation Requirements

### Must Include

1. **Disclaimer** - ในทุกเอกสารหลัก
2. **Mode Flag** - ใน code documentation
3. **No-Clinical Assertion** - ใน API documentation
4. **Terminology** - ในทุก specification

### Template Usage

ทุกเอกสารต้องมี:
- Disclaimer section
- Terminology section
- Mode flag reference

---

## Code Embedding

### Header Template

```cpp
/**
 * Cogman Core Kernel (CCK)
 * 
 * MODE: ENGINEERING_SIM (locked)
 * 
 * This is a pure engineering simulation framework based on mathematical 
 * models inspired by physics.
 * 
 * DISCLAIMER:
 * - No medical or clinical interpretation
 * - No biological modeling
 * - No psychological assessment
 * - Engineering simulation only
 */
```

### Function Documentation

```cpp
/**
 * CORE-1: Energy of Perception (ΔEΨ)
 * 
 * Mathematical model inspired by physics.
 * Abstract dimensionless scalar.
 * 
 * NOT: Biological energy, neural activity, or psychological state.
 */
double energy_of_perception(...);
```

---

## Legal Boundaries

### Medical Device Classification

**Status:** NOT a medical device

**Criteria:**
- No diagnostic purpose
- No therapeutic purpose
- No clinical interpretation
- Engineering simulation only

### Regulatory Compliance

**Requirements:**
- Clinical usage requires separate compliance layer
- Medical usage requires regulatory approval
- Psychiatric usage requires ethical review

---

## Version History

- **v1.0-LOCKED**: Initial legal/meaning lock specification

---

## Notes

- **Lock Status**: LOCKED — Legal/meaning boundaries must not be violated
- **Review Process**: ต้องผ่าน legal/compliance review ก่อนแก้ไข
- **Impact**: Legal/meaning violations กระทบ compliance และ liability

