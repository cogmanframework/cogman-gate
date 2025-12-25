"""
Gate Trace

Purpose: Trace gate decisions
"""

from typing import Dict, Any, List
import time


class GateTrace:
    """
    Gate decision tracer.
    """
    
    def __init__(self):
        """Initialize gate trace."""
        self.traces: List[Dict[str, Any]] = []
    
    def trace(self, decision: str, state: Dict[str, Any], reason: str = ""):
        """Trace gate decision."""
        self.traces.append({
            "timestamp": time.time(),
            "decision": decision,
            "state": state,
            "reason": reason,
        })
    
    def get_traces(self) -> List[Dict[str, Any]]:
        """Get all traces."""
        return self.traces

