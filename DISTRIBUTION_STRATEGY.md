# Distribution Strategy

**Status:** GitHub + Binary-First (NOT PyPI)

---

## Core Principle

> **Cogman Gate is not "easy to install"**  
> **It's "must be trusted"**

---

## Why NOT PyPI (Now)

### 1. Wrong Signal
- ❌ pip = "library to play with"
- ✅ Runtime = "infrastructure to trust"

### 2. Weakens Boundary Perception
- ❌ pip = Python-first, flexibility expected
- ✅ Runtime = Enforcement layer, no override

### 3. Wrong Audience
- ❌ Attracts: hobbyist, LLM dev, tweakers
- ✅ Targets: infra lead, platform engineer, safety team

---

## Current Distribution: GitHub + Binary-First

### What We Provide

```
✅ GitHub Repository (open)
   - Source code (Python bridge)
   - Specifications (open for audit)
   - Documentation

✅ Binary Kernel (protected IP)
   - Compiled C++ kernel
   - Signature verified
   - Checksum validated

✅ Installation Script
   - curl | bash installer
   - Downloads binary
   - Verifies signature
   - Sets up CLI
```

### Installation Flow

```bash
# 1. Clone repository
git clone https://github.com/cogmanframework/cogman_gate.git
cd cogman_gate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Download/verify kernel binary
curl -fsSL https://install.cogman.ai/runtime | bash

# 4. Verify installation
cogman --version
```

---

## When to Consider PyPI

### Prerequisites
- ✅ Have enterprise users
- ✅ Need convenience layer
- ✅ Positioning established
- ✅ Binary-first approach proven

### If PyPI Needed (Future)

**Option: Stub-Only Package**

```python
# Package name: cogman-runtime-client (NOT cogman-runtime)
# Contains:
# - Interface definitions
# - Type hints
# - CLI launcher
# - Binary downloader/verifier

# Kernel must be downloaded separately
# Signature must be verified
```

---

## Positioning Message

### Current (GitHub-First)
- "Infrastructure-grade runtime"
- "Binary-verified enforcement"
- "Auditable specifications"

### If PyPI (Future)
- "Client SDK for Cogman Runtime"
- "Requires verified kernel binary"
- "Enterprise deployment ready"

---

## Distribution Channels

| Channel | Purpose | Audience |
|---------|---------|----------|
| **GitHub** | Source, specs, docs | All (open) |
| **Binary CDN** | Kernel distribution | Verified users |
| **Installer Script** | Easy setup | Operators |
| **PyPI** | ❌ Not now | Future convenience |

---

## Security & IP Protection

### What's Open
- ✅ Python bridge code
- ✅ Specifications
- ✅ Documentation
- ✅ Test cases

### What's Protected
- 🔒 C++ kernel source
- 🔒 Core formulas
- 🔒 Binary signatures

### Verification
- ✅ Binary checksums
- ✅ GPG signatures
- ✅ Audit trail

---

## Roadmap

### Phase 1: GitHub-First (Current)
- [x] Repository structure
- [x] Binary build system
- [x] Installer script
- [x] Documentation

### Phase 2: Enterprise Ready
- [ ] Binary CDN
- [ ] Signature verification
- [ ] Enterprise installer
- [ ] Support channels

### Phase 3: Convenience Layer (If Needed)
- [ ] PyPI stub package (optional)
- [ ] Package manager integration
- [ ] Cloud marketplace

---

## Key Message

**Cogman Runtime is infrastructure, not a library.**

Installation should reflect that.

---

**Last Updated:** 2024-12-25

