"""
Gate Policy (thresholds / bands)

Purpose: Define gate thresholds and policies
"""

from typing import Dict, Any


class GatePolicy:
    """
    Gate policy manager.
    
    Defines thresholds and bands for decision gate.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize gate policy."""
        self.config = config or {
            "H_threshold": 0.85,
            "D_traj_threshold": 0.7,
            "E_mu_restrict_min": -100.0,
            "E_mu_restrict_max": 100.0,
        }
    
    def get_params(self) -> Dict[str, Any]:
        """Get decision parameters."""
        return self.config

