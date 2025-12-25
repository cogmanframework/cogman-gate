#!/bin/bash
# Cogman Gate Installer
# 
# Purpose: Download and verify kernel binary
# Distribution: GitHub + Binary-First

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
KERNEL_VERSION="2.0.0"
INSTALL_DIR="${HOME}/.cogman"
BIN_DIR="${INSTALL_DIR}/bin"
LIB_DIR="${INSTALL_DIR}/lib"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Detect architecture
case $ARCH in
    x86_64)
        ARCH="x86_64"
        ;;
    arm64|aarch64)
        ARCH="arm64"
        ;;
    *)
        echo -e "${RED}Error: Unsupported architecture: $ARCH${NC}"
        exit 1
        ;;
esac

# Detect OS and set binary extension
case $OS in
    linux)
        BINARY_EXT=".so"
        BINARY_NAME="libcogman_kernel.so"
        ;;
    darwin)
        BINARY_EXT=".dylib"
        BINARY_NAME="libcogman_kernel.dylib"
        ;;
    *)
        echo -e "${RED}Error: Unsupported OS: $OS${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}Cogman Runtime Installer${NC}"
echo "================================"
echo ""

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$LIB_DIR"

# Check if kernel binary exists locally
KERNEL_BUILD_PATH="kernel/build/${BINARY_NAME}"
if [ -f "$KERNEL_BUILD_PATH" ]; then
    echo -e "${YELLOW}Found local kernel binary${NC}"
    cp "$KERNEL_BUILD_PATH" "$LIB_DIR/"
    echo -e "${GREEN}✓ Kernel binary installed${NC}"
else
    echo -e "${YELLOW}Local kernel binary not found${NC}"
    echo "Please build kernel first:"
    echo "  cd kernel && mkdir build && cd build"
    echo "  cmake .. && make"
    echo ""
    echo "Or download from:"
    echo "  https://github.com/cogmanframework/cogman_gate/releases"
    exit 1
fi

# Verify binary
if [ -f "$LIB_DIR/$BINARY_NAME" ]; then
    echo -e "${GREEN}✓ Binary verification: OK${NC}"
    file "$LIB_DIR/$BINARY_NAME"
else
    echo -e "${RED}✗ Binary verification failed${NC}"
    exit 1
fi

# Set up environment
echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Add to your ~/.bashrc or ~/.zshrc:"
echo ""
echo "  export COGMAN_KERNEL_PATH=\"$LIB_DIR/$BINARY_NAME\""
echo "  export PATH=\"\$PATH:$BIN_DIR\""
echo ""
echo "Or run:"
echo "  export COGMAN_KERNEL_PATH=\"$LIB_DIR/$BINARY_NAME\""
echo ""

