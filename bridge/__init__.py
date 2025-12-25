"""
Language Boundary

Purpose: C++ <-> Python bridge
"""

from .kernel_bridge import KernelBridge
from .data_marshalling import (
    marshal_eps8,
    unmarshal_energy_state,
    marshal_decision_input,
    unmarshal_decision_result,
    create_decision_bands_from_policy,
)
from .error_map import map_kernel_error, KernelError, InvalidStateError, ComputationError

__all__ = [
    'KernelBridge',
    'marshal_eps8',
    'unmarshal_energy_state',
    'marshal_decision_input',
    'unmarshal_decision_result',
    'create_decision_bands_from_policy',
    'map_kernel_error',
    'KernelError',
    'InvalidStateError',
    'ComputationError',
]
