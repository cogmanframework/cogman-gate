"""
Example: Action Integration with Runtime Loop

Purpose: Demonstrate Action Module integration with Runtime Loop PHASE 8
"""

import logging
from action import ActionModule, ActionInput, ActionOutput, AgentController, TextOutput, MotorOutput
from reasoning import ReasoningOutput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_action_module():
    """Create Action Module instance."""
    agent_controller = AgentController()
    text_output = TextOutput()
    motor_output = MotorOutput()
    
    action_module = ActionModule(
        agent_controller=agent_controller,
        text_output=text_output,
        motor_output=motor_output
    )
    
    return action_module


def example_action_execution():
    """Example: Direct action execution."""
    logger.info("=== Example: Action Module Execution ===")
    
    # Create action module
    action_module = create_action_module()
    
    # Create test decision
    decision = {
        "decision": "ALLOW",
        "type": "text",
        "reason": "All metrics within safety bounds"
    }
    
    # Create test reasoning output
    reasoning_output = {
        "structure_type": "plan",
        "structure": {
            "steps": [
                {"id": 1, "action": "generate_text"},
                {"id": 2, "action": "format_output"}
            ]
        },
        "assumptions": ["Text generation is safe"],
        "constraints": ["Output must be non-empty"]
    }
    
    # Execute action
    output = action_module.execute(
        decision=decision,
        trace_id="test_trace_001",
        reasoning_output=reasoning_output
    )
    
    logger.info(f"Action type: {output.action_type}")
    logger.info(f"Success: {output.success}")
    logger.info(f"Output data: {output.output_data}")
    logger.info(f"Trace ID: {output.trace_id}")


def example_different_action_types():
    """Example: Different action types."""
    logger.info("\n=== Example: Different Action Types ===")
    
    # Create action module
    action_module = create_action_module()
    
    # Test text action
    text_decision = {
        "decision": "ALLOW",
        "type": "text"
    }
    
    text_output = action_module.execute(
        decision=text_decision,
        trace_id="test_trace_002"
    )
    logger.info(f"Text action: type={text_output.action_type}, success={text_output.success}")
    
    # Test motor action
    motor_decision = {
        "decision": "ALLOW",
        "type": "motor"
    }
    
    motor_output = action_module.execute(
        decision=motor_decision,
        trace_id="test_trace_003"
    )
    logger.info(f"Motor action: type={motor_output.action_type}, success={motor_output.success}")


def example_action_with_reasoning():
    """Example: Action with reasoning structure."""
    logger.info("\n=== Example: Action with Reasoning Structure ===")
    
    # Create action module
    action_module = create_action_module()
    
    # Decision
    decision = {
        "decision": "ALLOW",
        "type": "text"
    }
    
    # Reasoning output with plan structure
    reasoning_output = {
        "structure_type": "plan",
        "structure": {
            "steps": [
                {"id": 1, "action": "step_1"},
                {"id": 2, "action": "step_2"},
                {"id": 3, "action": "step_3"}
            ]
        },
        "assumptions": ["Plan is executable"],
        "constraints": ["Sequential execution"]
    }
    
    # Execute action
    output = action_module.execute(
        decision=decision,
        trace_id="test_trace_004",
        reasoning_output=reasoning_output
    )
    
    logger.info(f"Action type: {output.action_type}")
    logger.info(f"Output: {output.output_data}")


def example_action_error_handling():
    """Example: Action error handling."""
    logger.info("\n=== Example: Action Error Handling ===")
    
    # Create action module
    action_module = create_action_module()
    
    # Test with invalid decision
    invalid_decision = {
        "decision": "INVALID",
        "type": "unknown"
    }
    
    output = action_module.execute(
        decision=invalid_decision,
        trace_id="test_trace_005"
    )
    
    logger.info(f"Action type: {output.action_type}")
    logger.info(f"Success: {output.success}")
    if output.error:
        logger.info(f"Error: {output.error}")


if __name__ == "__main__":
    example_action_execution()
    example_different_action_types()
    example_action_with_reasoning()
    example_action_error_handling()

