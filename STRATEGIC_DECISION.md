# Strategic Decision: GitHub + Binary-First (NOT PyPI)

**Date:** 2024-12-25  
**Status:** ✅ Implemented

---

## Decision

**Do NOT publish to PyPI at this stage.**

**Reason:** Strategic positioning + IP protection, not technical limitation.

---

## Key Principle

> **Cogman Gate is not "easy to install"**  
> **It's "must be trusted"**

---

## Why NOT PyPI

### 1. Wrong Signal
- pip = "library to play with"
- Runtime = "infrastructure to trust"

### 2. Weakens Boundary
- pip = Python-first, flexibility expected
- Runtime = Enforcement layer, no override

### 3. Wrong Audience
- pip attracts: hobbyist, LLM dev, tweakers
- We target: infra lead, platform engineer, safety team

---

## Distribution Strategy

### Current: GitHub + Binary-First ✅

```
✅ GitHub Repository
   - Open source (Python bridge)
   - Open specifications
   - Open documentation

✅ Binary Kernel
   - Compiled C++ (IP protected)
   - Signature verified
   - Checksum validated

✅ Installer Script
   - curl | bash style
   - Downloads binary
   - Verifies signature
```

**Similar tools:**
- kubectl, terraform, vault, docker
- None are "pip install" tools

---

## When PyPI (Future)

**Prerequisites:**
- ✅ Have enterprise users
- ✅ Positioning established
- ✅ Need convenience layer

**If needed:** Stub-only package
- Name: `cogman-gate-client` (NOT `cogman-gate`)
- Contains: interface, types, CLI launcher
- Kernel: downloaded separately, verified

---

## Files Created

- ✅ `install.sh` - Installer script
- ✅ `INSTALL.md` - Installation guide
- ✅ `DISTRIBUTION_STRATEGY.md` - Full strategy
- ✅ `WHY_NOT_PYPI.md` - Detailed reasoning

---

## Action Items

- [x] Remove PyPI publishing plans
- [x] Create installer script
- [x] Update installation docs
- [x] Emphasize binary-first approach
- [ ] Set up binary CDN (future)
- [ ] Add signature verification (future)

---

**This is the right decision for infrastructure positioning.**

