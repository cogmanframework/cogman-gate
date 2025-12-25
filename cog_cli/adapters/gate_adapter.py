"""
Gate Adapter - Bridge CLI to decision gate

Delegates to gate module and config
"""

import sys
from typing import Dict, Any, Tuple, Optional

try:
    from config import GatePolicyLoader
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("Warning: Gate policy loader not available.", file=sys.stderr)

try:
    from bridge import KernelBridge
    KERNEL_AVAILABLE = True
except ImportError:
    KERNEL_AVAILABLE = False


def evaluate_decision(
    metrics: Dict[str, float],
    context: str = 'default',
    policy_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate decision gate.
    
    Args:
        metrics: Decision metrics (E_mu, H, D, S, etc.)
        context: Decision context
        policy_file: Optional policy file path
    
    Returns:
        Decision result dictionary
    """
    if not KERNEL_AVAILABLE:
        raise RuntimeError("Kernel bridge not available")
    
    bridge = KernelBridge()
    
    # Load policy if provided
    bands = None
    if policy_file and CONFIG_AVAILABLE:
        try:
            loader = GatePolicyLoader()
            policy = loader.load_from_file(policy_file)
            context_profile = policy.get_context(context)
            if context_profile:
                # Convert to bands format
                bands = {
                    'D_max': context_profile.limits.get('D_max', 0.35),
                    'H_max': context_profile.limits.get('H_max', 0.62),
                    'V_max': context_profile.limits.get('V_max', 8.0),
                    'E_mu_accept_min': context_profile.limits.get('E_mu_accept_min', 30.0),
                    'E_mu_accept_max': context_profile.limits.get('E_mu_accept_max', 80.0),
                    'E_mu_caution_min': context_profile.limits.get('E_mu_caution_min', 15.0),
                    'E_mu_caution_max': context_profile.limits.get('E_mu_caution_max', 30.0),
                    'E_mu_restrict_max': context_profile.limits.get('E_mu_restrict_max', 15.0),
                    'version': policy.meta.get('version', '1.0')
                }
        except Exception as e:
            print(f"Warning: Failed to load policy file: {e}", file=sys.stderr)
    
    # Use default bands if not loaded
    if not bands:
        bands = {
            'D_max': 0.35,
            'H_max': 0.62,
            'V_max': 8.0,
            'E_mu_accept_min': 30.0,
            'E_mu_accept_max': 80.0,
            'E_mu_caution_min': 15.0,
            'E_mu_caution_max': 30.0,
            'E_mu_restrict_max': 15.0,
            'version': '1.0'
        }
    
    # Call kernel CORE-9 gate
    try:
        result = bridge.core9_evaluate(
            metrics=metrics,
            bands=bands,
            context=context,
            E_mu_history=None
        )
        return result
    except Exception as e:
        raise RuntimeError(f"Decision evaluation failed: {e}")


def validate_policy(policy_file: str) -> Tuple[bool, list]:
    """
    Validate gate policy file.
    
    Args:
        policy_file: Policy file path
    
    Returns:
        Tuple of (is_valid, errors)
    """
    if not CONFIG_AVAILABLE:
        raise RuntimeError("Gate policy loader not available")
    
    errors = []
    
    try:
        loader = GatePolicyLoader()
        policy = loader.load_from_file(policy_file)
        
        # Basic validation
        if not policy.meta:
            errors.append("Missing metadata")
        
        if not policy.contexts:
            errors.append("No contexts defined")
        
        # Validate each context
        for context_name, context_profile in policy.contexts.items():
            if not context_profile.limits:
                errors.append(f"Context '{context_name}' has no limits")
        
        return len(errors) == 0, errors
    except Exception as e:
        errors.append(f"Failed to load policy: {e}")
        return False, errors

