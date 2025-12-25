"""
Kernel Adapter - Bridge CLI to C++ kernel

Delegates to bridge.kernel_bridge
"""

import sys
from typing import Dict, Any, Tuple, Optional

try:
    from bridge import KernelBridge
    KERNEL_AVAILABLE = True
except ImportError:
    KERNEL_AVAILABLE = False
    print("Warning: Kernel bridge not available. Install kernel first.", file=sys.stderr)


def compute_formula(formula_name: str, eps8_state: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute specific formula.
    
    Args:
        formula_name: Formula name (e.g., 'CORE-1')
        eps8_state: EPS-8 state dictionary
    
    Returns:
        Result dictionary
    """
    if not KERNEL_AVAILABLE:
        raise RuntimeError("Kernel bridge not available")
    
    bridge = KernelBridge()
    
    # Map formula name to computation
    if formula_name == 'CORE-1':
        # Energy of Perception
        I = eps8_state.get('I', 0.0)
        P = eps8_state.get('P', 0.0)
        S_a = eps8_state.get('S_a', 0.0)
        H = eps8_state.get('H', 0.0)
        
        # TODO: Call actual kernel function
        # For now, return placeholder
        return {
            'formula': 'CORE-1',
            'result': 0.0,
            'inputs': {'I': I, 'P': P, 'S_a': S_a, 'H': H}
        }
    else:
        raise ValueError(f"Unknown formula: {formula_name}")


def compute_energy_projection(eps8_state: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute energy projection from EPS-8 state.
    
    Args:
        eps8_state: EPS-8 state dictionary
    
    Returns:
        Energy state dictionary
    """
    if not KERNEL_AVAILABLE:
        raise RuntimeError("Kernel bridge not available")
    
    bridge = KernelBridge()
    
    # Build neural components (defaults)
    neural_components = {
        'dopamine': 0.0,
        'serotonin': 0.0,
        'oxytocin': 0.0,
        'adrenaline': 0.0,
        'cortisol': 0.0
    }
    
    # Build decision params (defaults)
    decision_params = {
        'rule_fail': False,
        'E_mu_restrict_min': -float('inf'),
        'E_mu_restrict_max': float('inf'),
        'H_threshold': 0.85,
        'D_traj_threshold': 0.7
    }
    
    try:
        result = bridge.energy_projection(
            eps8_state=eps8_state,
            neural_components=neural_components,
            theta_phase=eps8_state.get('theta', 0.0),
            E_pred=0.0,
            decision_params=decision_params
        )
        return result
    except Exception as e:
        raise RuntimeError(f"Energy projection failed: {e}")


def validate_eps8_state(eps8_state: Dict[str, float]) -> Tuple[bool, list]:
    """
    Validate EPS-8 state.
    
    Args:
        eps8_state: EPS-8 state dictionary
    
    Returns:
        Tuple of (is_valid, errors)
    """
    if not KERNEL_AVAILABLE:
        raise RuntimeError("Kernel bridge not available")
    
    bridge = KernelBridge()
    
    errors = []
    
    # Basic validation
    required_fields = ['I', 'P', 'S', 'H', 'F', 'A', 'S_a', 'theta']
    for field in required_fields:
        if field not in eps8_state:
            errors.append(f"Missing required field: {field}")
    
    # Range validation
    if 'I' in eps8_state and eps8_state['I'] < 0.0:
        errors.append("I (Intensity) must be >= 0")
    
    if 'S' in eps8_state:
        s = eps8_state['S']
        if s < 0.0 or s > 1.0:
            errors.append(f"S (Stability) must be in [0, 1], got {s}")
    
    if 'H' in eps8_state:
        h = eps8_state['H']
        if h < 0.0 or h > 1.0:
            errors.append(f"H (Entropy) must be in [0, 1], got {h}")
    
    if 'A' in eps8_state:
        a = eps8_state['A']
        if a < 0.0 or a > 1.0:
            errors.append(f"A (Awareness) must be in [0, 1], got {a}")
    
    if 'S_a' in eps8_state:
        s_a = eps8_state['S_a']
        if s_a < 0.0 or s_a > 1.0:
            errors.append(f"S_a (Sub-awareness) must be in [0, 1], got {s_a}")
    
    # Try kernel validation
    try:
        is_valid = bridge.validate_state(eps8_state)
        if not is_valid:
            errors.append("Kernel validation failed")
    except Exception as e:
        errors.append(f"Kernel validation error: {e}")
    
    return len(errors) == 0, errors

