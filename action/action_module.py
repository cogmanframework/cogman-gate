"""
Action Module

Purpose: Execute actions and generate outputs
Spec: Runtime Loop PHASE 8
"""

from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass, field
import time
import logging

from .agent_controller import AgentController
from .text_output import TextOutput
from .motor_output import MotorOutput

logger = logging.getLogger(__name__)


@dataclass
class ActionInput:
    """
    Action Input Structure
    
    From Decision Module or Reasoning Module
    """
    decision: Dict[str, Any]  # Decision from Decision Module
    reasoning_output: Optional[Dict[str, Any]] = None  # Structure from Reasoning Module
    trajectory: Optional[Dict[str, Any]] = None  # Trajectory (for context)
    trace_id: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionOutput:
    """
    Action Output Structure
    
    Spec: Runtime Loop PHASE 8
    """
    action_type: str  # "text" | "motor" | "none"
    output_data: Any  # Output data
    trace_id: str
    timestamp: float
    success: bool = True
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert output to dictionary."""
        return {
            "action_type": self.action_type,
            "output_data": self.output_data,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "success": self.success,
            "error": self.error
        }


class ActionModule:
    """
    Action Module
    
    Purpose: Execute actions and generate outputs
    
    Rules:
    - Execute action based on decision
    - Generate observable output
    - Attach trace_id
    - NO decision making
    - NO evaluation
    """
    
    def __init__(
        self,
        agent_controller: Optional[AgentController] = None,
        text_output: Optional[TextOutput] = None,
        motor_output: Optional[MotorOutput] = None
    ):
        """
        Initialize Action Module.
        
        Args:
            agent_controller: AgentController instance (optional)
            text_output: TextOutput instance (optional)
            motor_output: MotorOutput instance (optional)
        """
        self.agent_controller = agent_controller or AgentController()
        self.text_output = text_output or TextOutput()
        self.motor_output = motor_output or MotorOutput()
    
    def execute(
        self,
        decision: Dict[str, Any],
        trace_id: str,
        reasoning_output: Optional[Dict[str, Any]] = None,
        trajectory: Optional[Dict[str, Any]] = None
    ) -> ActionOutput:
        """
        Execute action based on decision.
        
        This is the PHASE 8 operation in Runtime Loop.
        
        Args:
            decision: Decision from Decision Module
            trace_id: Trace identifier
            reasoning_output: Reasoning output structure (optional)
            trajectory: Trajectory (optional, for context)
        
        Returns:
            ActionOutput with execution result
        """
        # Determine action type from decision
        action_type = self._determine_action_type(decision, reasoning_output)
        
        # Prepare action data
        action_data = self._prepare_action_data(decision, reasoning_output, trajectory)
        
        # Execute action
        try:
            if action_type == "text":
                output_data = self._execute_text_action(action_data)
            elif action_type == "motor":
                output_data = self._execute_motor_action(action_data)
            else:
                output_data = None
            
            success = True
            error = None
            
        except Exception as e:
            logger.error(f"Action execution failed: {e}", exc_info=True)
            output_data = None
            success = False
            error = str(e)
        
        # Create output
        output = ActionOutput(
            action_type=action_type,
            output_data=output_data,
            trace_id=trace_id,
            timestamp=time.time(),
            success=success,
            error=error
        )
        
        logger.info(
            f"Action executed: {action_type} "
            f"(trace_id={trace_id}, success={success})"
        )
        
        return output
    
    def _determine_action_type(
        self,
        decision: Dict[str, Any],
        reasoning_output: Optional[Dict[str, Any]]
    ) -> str:
        """
        Determine action type from decision.
        
        Rules:
        - Based on decision structure
        - Based on reasoning output structure type
        - NO evaluation, NO preference
        """
        # Check decision for action type
        decision_type = decision.get("type", decision.get("decision", "none"))
        
        if decision_type in ["text", "motor"]:
            return decision_type
        
        # Check reasoning output structure type
        if reasoning_output:
            structure_type = reasoning_output.get("structure_type", "")
            if structure_type == "plan":
                # Plan structure might indicate motor action
                return "motor"
            elif structure_type in ["graph", "tree", "simulation"]:
                # Other structures might indicate text action
                return "text"
        
        # Default: text action
        return "text"
    
    def _prepare_action_data(
        self,
        decision: Dict[str, Any],
        reasoning_output: Optional[Dict[str, Any]],
        trajectory: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prepare action data from decision and reasoning output.
        
        Rules:
        - Combine decision and reasoning structure
        - NO interpretation
        - NO evaluation
        """
        action_data = {
            "decision": decision,
            "reasoning": reasoning_output,
            "trajectory": trajectory
        }
        
        # Extract structure from reasoning output if available
        if reasoning_output:
            structure = reasoning_output.get("structure")
            if structure:
                action_data["structure"] = structure
        
        return action_data
    
    def _execute_text_action(self, action_data: Dict[str, Any]) -> str:
        """
        Execute text action.
        
        Rules:
        - Generate text output only
        - NO decision making
        - NO evaluation
        """
        # Use text output generator
        output = self.text_output.generate(action_data)
        
        # If empty, generate minimal output
        if not output:
            output = self._generate_minimal_text(action_data)
        
        return output
    
    def _execute_motor_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute motor action.
        
        Rules:
        - Generate motor output only
        - NO decision making
        - NO evaluation
        """
        # Use motor output generator
        output = self.motor_output.generate(action_data)
        
        # If empty, generate minimal output
        if not output:
            output = self._generate_minimal_motor(action_data)
        
        return output
    
    def _generate_minimal_text(self, action_data: Dict[str, Any]) -> str:
        """Generate minimal text output."""
        decision = action_data.get("decision", {})
        decision_type = decision.get("decision", "ALLOW")
        
        return f"Action executed: {decision_type}"
    
    def _generate_minimal_motor(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate minimal motor output."""
        return {
            "type": "motor",
            "status": "executed",
            "timestamp": time.time()
        }

