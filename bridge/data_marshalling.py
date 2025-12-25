"""
Data Marshalling

Purpose: Convert between Python dicts and C++ structs
"""

from typing import Dict, Any, List, Optional
from bridge.kernel_bridge import KernelBridge


def marshal_eps8(state_dict: Dict[str, float]) -> Dict[str, float]:
    """
    Marshal Python dict to EPS-8 state.
    
    Args:
        state_dict: Python dictionary with I, P, S, H, F, A, S_a, theta
    
    Returns:
        Validated EPS-8 state dict
    """
    required_keys = ['I', 'P', 'S', 'H', 'F', 'A', 'S_a', 'theta']
    eps8 = {}
    
    for key in required_keys:
        eps8[key] = state_dict.get(key, 0.0)
    
    return eps8


def unmarshal_energy_state(energy_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unmarshal energy state from kernel bridge result.
    
    Args:
        energy_state: Energy state dict from kernel bridge
    
    Returns:
        Python dictionary with energy values
    """
    return {
        "delta_E_psi": energy_state.get("delta_E_psi", 0.0),
        "E_reflex": energy_state.get("E_reflex", 0.0),
        "delta_E_psi_theta": energy_state.get("delta_E_psi_theta", 0.0),
        "E_mind": energy_state.get("E_mind", 0.0),
        "E_coherence": energy_state.get("E_coherence", 0.0),
        "E_neural": energy_state.get("E_neural", 0.0),
        "E_bind": energy_state.get("E_bind", 0.0),
        "E_mem": energy_state.get("E_mem", 0.0),
        "verdict": energy_state.get("verdict", "ALLOW"),
    }


def marshal_decision_input(metrics: Dict[str, float],
                          bands: Dict[str, Any],
                          context: str = "default",
                          E_mu_history: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Marshal decision input for CORE-9 gate.
    
    Args:
        metrics: Core metrics dict (E_mu, H, D, S, T, V)
        bands: Decision bands dict
        context: Context name
        E_mu_history: Optional Eμ history
    
    Returns:
        Decision input dict
    """
    return {
        "metrics": metrics,
        "bands": bands,
        "context": context,
        "E_mu_history": E_mu_history or [],
    }


def unmarshal_decision_result(decision_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unmarshal decision result from kernel bridge.
    
    Args:
        decision_result: Decision result dict from kernel bridge
    
    Returns:
        Python dictionary with decision result
    """
    return {
        "verdict": decision_result.get("verdict", "ALLOW"),
        "metrics": decision_result.get("metrics", {}),
        "rule_fail": decision_result.get("rule_fail", False),
        "reasons": decision_result.get("reasons", []),
        "protocol": decision_result.get("protocol", "CORE9_v1.0"),
        "context": decision_result.get("context", "default"),
    }


def create_decision_bands_from_policy(policy_profile: Any) -> Dict[str, Any]:
    """
    Create decision bands from policy profile.
    
    Args:
        policy_profile: ContextProfile from gate_policy_loader
    
    Returns:
        Decision bands dict
    """
    limits = policy_profile.limits
    bands = limits.e_mu_bands
    
    return {
        "D_max": limits.embedding_distance_max,
        "H_max": limits.entropy_max_p95,
        "V_max": limits.variance_max,
        "E_mu_accept_min": bands.accept_min,
        "E_mu_accept_max": bands.accept_max,
        "E_mu_caution_min": bands.caution_min,
        "E_mu_caution_max": bands.caution_max,
        "E_mu_restrict_max": bands.restrict_max,
    }
