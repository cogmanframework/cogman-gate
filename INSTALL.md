# Installation Guide

**Version:** v2.0-LOCKED

---

## Prerequisites

- **CMake:** 3.10 or higher
- **Compiler:** C++17 compatible (g++ 7+, clang++ 5+, MSVC 2017+)
- **Build Tools:** make or ninja

---

## Building from Source

### Step 1: Clone and Navigate

```bash
cd kernel
```

### Step 2: Create Build Directory

```bash
mkdir build
cd build
```

### Step 3: Configure with CMake

```bash
cmake ..
```

### Step 4: Build

```bash
make
# or
cmake --build .
```

### Step 5: Run Tests (Optional)

```bash
./test_core_formulas
./test_energy_bounds
./test_determinism
```

---

## Installation

### Install Library

```bash
sudo make install
```

This will install:
- Headers to `/usr/local/include/cogman_kernel/`
- Library to `/usr/local/lib/libcogman_kernel.a`

### Custom Install Prefix

```bash
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install ..
make install
```

---

## Using in Your Project

### CMake (Recommended)

```cmake
# In your CMakeLists.txt
add_subdirectory(kernel)
target_link_libraries(your_target cogman_kernel)
target_include_directories(your_target PRIVATE kernel/include)
```

### Manual Linking

```bash
# Compile your code
g++ -std=c++17 \
    -Ikernel/include \
    your_code.cpp \
    -Lkernel/build \
    -lcogman_kernel \
    -o your_program
```

### Include in Your Code

```cpp
// Option 1: Include master header
#include "cogman_kernel/cogman_kernel.hpp"

// Option 2: Include specific headers
#include "cogman_kernel/core_formulas.hpp"
#include "cogman_kernel/eps8.hpp"
```

---

## Package Managers

### vcpkg (Future)

```bash
vcpkg install cogman-kernel
```

### Conan (Future)

```bash
conan install cogman-kernel/2.0.0@
```

---

## Troubleshooting

### Build Errors

**Error:** `C++17 not supported`
- **Solution:** Update your compiler or set `CMAKE_CXX_STANDARD=17`

**Error:** `CMake version too old`
- **Solution:** Update CMake to 3.10 or higher

### Link Errors

**Error:** `undefined reference`
- **Solution:** Make sure you link against `cogman_kernel` library

**Error:** `header not found`
- **Solution:** Add `kernel/include` to include path

---

## Verification

After installation, verify with:

```cpp
#include "cogman_kernel/cogman_kernel.hpp"
#include <iostream>

int main() {
    std::cout << "Cogman Kernel v" 
              << cogman_kernel::Version::string 
              << std::endl;
    return 0;
}
```

---

## Status

**Development Status:** LOCKED  
**Installation Status:** Manual installation supported

