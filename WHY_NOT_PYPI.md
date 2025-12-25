# Why NOT PyPI (Strategic Decision)

**Status:** GitHub + Binary-First Distribution

---

## Core Principle

> **Cogman Gate is not "easy to install"**  
> **It's "must be trusted"**

---

## Strategic Reasons

### 1. Wrong Signal ❌

**pip = "library to play with"**

But Cogman Gate is:
- Infrastructure enforcement layer
- Binary-verified system
- Must be trusted, not modified

**Perception matters:**
- pip → "install and hack"
- Binary-first → "deploy and trust"

---

### 2. Weakens Boundary Perception ❌

**Python community expects:**
- Flexibility
- Monkey patching
- Override capabilities
- "Hackable" code

**Cogman Runtime requires:**
- Hard boundaries
- No override
- Binary enforcement
- Trusted execution

**Conflict:** pip signals flexibility, but we need rigidity.

---

### 3. Wrong Audience ❌

**pip attracts:**
- ❌ Hobbyists
- ❌ LLM agent developers
- ❌ People who want to tweak formulas
- ❌ People who want to bypass runtime

**We target:**
- ✅ Infrastructure leads
- ✅ Platform engineers
- ✅ Robotics / safety teams
- ✅ Compliance / risk teams

**Reality:** Target audience doesn't search PyPI for infrastructure tools.

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
   - Sets up environment
```

**Examples of similar tools:**
- kubectl (Kubernetes)
- terraform (HashiCorp)
- vault (HashiCorp)
- docker (Docker)

**None of these are "pip install" tools.**

---

## When PyPI Makes Sense (Future)

### Prerequisites
- ✅ Have enterprise users
- ✅ Positioning established
- ✅ Binary-first proven
- ✅ Need convenience layer

### If Needed: Stub-Only Package

**Package name:** `cogman-runtime-client` (NOT `cogman-runtime`)

**Contains:**
- Interface definitions
- Type hints
- CLI launcher
- Binary downloader/verifier

**Kernel:**
- Downloaded separately
- Signature verified
- Checksum validated

**Message:**
- "Client SDK for Cogman Runtime"
- "Requires verified kernel binary"
- "Enterprise deployment ready"

---

## Positioning Comparison

| Aspect | PyPI (Now) | GitHub + Binary (Current) |
|--------|------------|---------------------------|
| **Signal** | Library | Infrastructure |
| **Audience** | Developers | Operators |
| **Trust** | Optional | Required |
| **Modification** | Expected | Forbidden |
| **Deployment** | Casual | Enterprise |

---

## Key Message

**Cogman Runtime is infrastructure, not a library.**

Installation method should reflect that.

---

## Decision Matrix

| Question | Answer |
|----------|--------|
| Should we publish to PyPI now? | ❌ No |
| Will we lose opportunities? | ❌ No |
| Will we look unprofessional? | ❌ Opposite |
| How will infra teams see us? | ✅ "This is real infrastructure" |
| How should we distribute? | ✅ GitHub + Binary-first |
| When should we consider PyPI? | After having enterprise users |

---

## Action Items

- [x] Remove PyPI publishing plans
- [x] Create installer script
- [x] Update installation docs
- [x] Emphasize binary-first approach
- [ ] Set up binary CDN (future)
- [ ] Add signature verification (future)

---

**Last Updated:** 2024-12-25

