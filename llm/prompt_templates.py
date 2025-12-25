"""
Prompt Templates

Purpose: LLM prompt templates
"""

from typing import Dict, Any


class PromptTemplates:
    """
    Prompt template manager.
    """
    
    def __init__(self):
        """Initialize prompt templates."""
        # Template placeholders (can be expanded with actual templates)
        self._templates = {
            "gate_decision_explanation": "Explain the gate decision: {verdict} - {reason}",
            "energy_projection_summary": "Summarize energy projection: {energy_state}",
            "trajectory_summary": "Summarize trajectory: {trajectory}"
        }
    
    def get_template(self, template_name: str, variables: Dict[str, Any] = None) -> str:
        """
        Get prompt template.
        
        Args:
            template_name: Name of template
            variables: Variables to substitute in template
        
        Returns:
            Formatted prompt
        """
        template = self._templates.get(template_name, "")
        
        if variables and template:
            try:
                return template.format(**variables)
            except KeyError:
                # If variables don't match, return template as-is
                return template
        
        return template
    
    def gate_decision_explanation(self, verdict: str, reason: str, metrics: Dict[str, Any] = None) -> str:
        """
        Get gate decision explanation template.
        
        Args:
            verdict: Decision verdict (ALLOW/REVIEW/BLOCK)
            reason: Decision reason
            metrics: Decision metrics (optional)
        
        Returns:
            Formatted prompt
        """
        variables = {
            "verdict": verdict,
            "reason": reason
        }
        if metrics:
            variables["metrics"] = str(metrics)
        
        return self.get_template("gate_decision_explanation", variables)
    
    def energy_projection_summary(self, energy_state: Dict[str, float]) -> str:
        """
        Get energy projection summary template.
        
        Args:
            energy_state: Energy state dictionary
        
        Returns:
            Formatted prompt
        """
        variables = {
            "energy_state": str(energy_state)
        }
        return self.get_template("energy_projection_summary", variables)
    
    def trajectory_summary(self, trajectory: Dict[str, Any]) -> str:
        """
        Get trajectory summary template.
        
        Args:
            trajectory: Trajectory dictionary
        
        Returns:
            Formatted prompt
        """
        variables = {
            "trajectory": str(trajectory)
        }
        return self.get_template("trajectory_summary", variables)

