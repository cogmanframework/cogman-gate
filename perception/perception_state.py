"""
Perception State (uses EPS-8 result)

Purpose: Manage perception state from EPS-8 computation
"""

from typing import Dict, Any
from bridge import KernelBridge


class PerceptionState:
    """
    Perception state manager.
    
    Uses EPS-8 result from kernel.
    """
    
    def __init__(self, kernel_bridge: KernelBridge):
        """Initialize perception state."""
        self.kernel_bridge = kernel_bridge
        self.current_state = None
    
    def update(self, eps8_result: Dict[str, Any]):
        """Update perception state from EPS-8 result."""
        self.current_state = eps8_result
    
    def get_state(self) -> Dict[str, Any]:
        """Get current perception state."""
        return self.current_state or {}

