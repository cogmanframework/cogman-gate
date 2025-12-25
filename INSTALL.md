# Installation Guide

**Cogman Gate - Infrastructure Installation**

---

## Installation Method: GitHub + Binary-First

Cogman Gate is distributed as **infrastructure**, not a library.

---

## Quick Install

### Option 1: From Source (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/cogmanframework/cogman_gate.git
cd cogman_gate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build C++ kernel
cd kernel
mkdir build && cd build
cmake .. && make
cd ../..

# 4. Run installer script
chmod +x install.sh
./install.sh

# 5. Set environment
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.so"  # Linux
# or
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.dylib"  # macOS
```

### Option 2: Using Installer Script

```bash
# Download and run installer
curl -fsSL https://raw.githubusercontent.com/cogmanframework/cogman_gate/main/install.sh | bash

# Set environment
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.so"
```

---

## Prerequisites

- **Python 3.8+**
- **C++17 compiler** (g++ 7+, clang++ 8+, MSVC 2017+)
- **CMake 3.10+**
- **Git**

---

## Verification

```bash
# Check kernel binary
ls -lh $HOME/.cogman/lib/libcogman_kernel.*

# Test Python bridge
python -c "from bridge import KernelBridge; print('OK')"

# Test CLI
python -m cog_cli.main --help
```

---

## Why Not PyPI?

Cogman Runtime is **infrastructure**, not a library:

- ✅ Binary-verified enforcement
- ✅ Signature-checked distribution
- ✅ Enterprise-grade deployment
- ❌ Not a "pip install and play" tool

**Target Audience:**
- Infrastructure teams
- Platform engineers
- Safety-critical systems
- Enterprise deployments

---

## Troubleshooting

### Kernel Binary Not Found

```bash
# Build kernel manually
cd kernel
mkdir build && cd build
cmake .. && make
cd ../..
```

### Python Import Error

```bash
# Check environment
export COGMAN_KERNEL_PATH="$HOME/.cogman/lib/libcogman_kernel.so"
python -c "from bridge import KernelBridge; print('OK')"
```

### Permission Denied

```bash
# Make installer executable
chmod +x install.sh
```

---

## Enterprise Installation

For enterprise deployments:

1. **Download binary** from releases
2. **Verify signature** (GPG)
3. **Deploy to** internal artifact repository
4. **Configure** environment variables
5. **Audit** installation

---

## Security Notes

- ✅ Kernel binary is signature-verified
- ✅ Checksums are validated
- ✅ Source code is auditable
- ✅ Specifications are open

---

**See also:** `DISTRIBUTION_STRATEGY.md`

