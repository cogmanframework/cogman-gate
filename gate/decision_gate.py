"""
Decision Gate (ALLOW / REVIEW / BLOCK)

Purpose: Decision gate logic
"""

from typing import Dict, Any
from bridge import KernelBridge
from .gate_policy import GatePolicy


class DecisionGate:
    """
    Decision gate.
    
    Returns: ALLOW, REVIEW, or BLOCK
    """
    
    def __init__(self, kernel_bridge: KernelBridge, policy: GatePolicy):
        """Initialize decision gate."""
        self.kernel_bridge = kernel_bridge
        self.policy = policy
    
    def decide(self, state: Dict[str, Any]) -> str:
        """
        Make decision.
        
        Returns:
            "ALLOW", "REVIEW", or "BLOCK"
        """
        params = self.policy.get_params()
        H_current = state.get('H', 0.0)
        D_traj_current = state.get('D_traj', 0.0)
        
        # Call kernel decision gate
        verdict = self.kernel_bridge.decision_gate(params, H_current, D_traj_current)
        return verdict

