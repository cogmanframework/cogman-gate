"""
Agent Controller

Purpose: Control agent actions
"""

from typing import Dict, Any
from .text_output import TextOutput
from .motor_output import MotorOutput


class AgentController:
    """
    Agent controller.
    
    Controls agent actions.
    """
    
    def __init__(self):
        """Initialize agent controller."""
        self.text_output = TextOutput()
        self.motor_output = MotorOutput()
    
    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute action.
        
        Returns:
            Execution result
        """
        action_type = action.get("type", "text")
        
        if action_type == "text":
            return {"output": self.text_output.generate(action)}
        elif action_type == "motor":
            return {"output": self.motor_output.generate(action)}
        else:
            return {"output": {}}

