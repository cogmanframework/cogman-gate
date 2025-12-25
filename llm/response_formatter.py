"""
Response Formatter

Purpose: Format LLM responses
"""

from typing import Dict, Any


class ResponseFormatter:
    """
    Response formatter.
    """
    
    def format(self, response: str, format_type: str = "text") -> Dict[str, Any]:
        """
        Format LLM response.
        
        Returns:
            Formatted response
        """
        return {
            "format": format_type,
            "content": response,
        }
    
    def format_gate_decision(self, decision: Dict[str, Any]) -> str:
        """
        Format gate decision for display.
        
        Args:
            decision: Gate decision dictionary with 'verdict', 'reason', 'metrics'
        
        Returns:
            Formatted gate decision text
        """
        verdict = decision.get("verdict", "UNKNOWN")
        reason = decision.get("reason", "No reason provided")
        metrics = decision.get("metrics", {})
        
        lines = [
            f"Gate Decision: {verdict}",
            f"Reason: {reason}",
            "Metrics:"
        ]
        
        for key, value in metrics.items():
            lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
    
    def format_energy_state(self, energy_state: Dict[str, float]) -> str:
        """
        Format energy state for display.
        
        Args:
            energy_state: Energy state dictionary with I, P, S, H, etc.
        
        Returns:
            Formatted energy state text
        """
        lines = ["Energy State:"]
        
        for key, value in energy_state.items():
            lines.append(f"  {key}: {value:.4f}")
        
        return "\n".join(lines)

