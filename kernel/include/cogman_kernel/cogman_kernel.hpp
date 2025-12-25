/**
 * Cogman Kernel - Master Header
 * 
 * Version: v2.0-LOCKED
 * Status: LOCKED - Master include file
 * 
 * Include this file to get all Cogman Kernel functionality.
 * This is the main public API header.
 */

#ifndef COGMAN_KERNEL_HPP
#define COGMAN_KERNEL_HPP

// Core types
#include "cogman_kernel/types.hpp"
#include "cogman_kernel/version.hpp"

// Error handling
#include "cogman_kernel/errors.hpp"

// EPS-8 state
#include "cogman_kernel/eps8.hpp"

// Core formulas (CORE-1 to CORE-9)
#include "cogman_kernel/core_formulas.hpp"

// Cognitive Decision Gate (legacy)
#include "cogman_kernel/cognitive_decision_gate.hpp"

// CORE-9 Decision Gate (production spec)
#include "cogman_kernel/core9_gate.hpp"

// Gate Policy Loader
#include "cogman_kernel/gate_policy.hpp"

// C API (for FFI)
#include "cogman_kernel/kernel_api.hpp"

#endif // COGMAN_KERNEL_HPP
