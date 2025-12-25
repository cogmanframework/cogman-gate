"""
Example: Reasoning Integration with Runtime Loop

Purpose: Demonstrate Reasoning Module integration with Runtime Loop PHASE 6
"""

import logging
from reasoning import ReasoningModule, ReasoningInput, CausalGraph, Planner, Simulator
from runtime import WMControllerOutput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_reasoning_module():
    """Create Reasoning Module instance."""
    causal_graph = CausalGraph()
    planner = Planner()
    simulator = Simulator()
    
    reasoning_module = ReasoningModule(
        causal_graph=causal_graph,
        planner=planner,
        simulator=simulator
    )
    
    return reasoning_module


def example_reasoning_processing():
    """Example: Direct reasoning processing."""
    logger.info("=== Example: Reasoning Module Processing ===")
    
    # Create reasoning module
    reasoning_module = create_reasoning_module()
    
    # Create test trajectory (from WM Controller)
    trajectory = {
        "trace_id": "test_trace_001",
        "states": [
            {"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3, "A": 0.5, "S_a": 0.4, "theta": 1.2},
            {"I": 0.8, "P": 0.7, "S": 0.9, "H": 0.2, "A": 0.6, "S_a": 0.5, "theta": 1.3},
            {"I": 0.9, "P": 0.8, "S": 0.9, "H": 0.1, "A": 0.7, "S_a": 0.6, "theta": 1.4}
        ],
        "source_modality": "text",
        "timestamp": 0.0
    }
    
    # Create reasoning input
    reasoning_input = ReasoningInput(
        trajectory=trajectory,
        wm_decision_hint="CREATE_NEW_SN",  # Informational only
        context={"source": "wm_controller"},
        trace_id="test_trace_001"
    )
    
    # Process through reasoning module
    output = reasoning_module.process(reasoning_input)
    
    logger.info(f"Structure type: {output.structure_type}")
    logger.info(f"Assumptions: {output.assumptions}")
    logger.info(f"Constraints: {output.constraints}")
    logger.info(f"Meta: {output.meta}")


def example_different_reasoning_types():
    """Example: Different reasoning types based on WM hint."""
    logger.info("\n=== Example: Different Reasoning Types ===")
    
    # Create reasoning module
    reasoning_module = create_reasoning_module()
    
    # Test trajectory
    trajectory = {
        "trace_id": "test_trace_002",
        "states": [
            {"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3, "A": 0.5, "S_a": 0.4, "theta": 1.2}
        ],
        "source_modality": "text",
        "timestamp": 0.0
    }
    
    # Test different WM hints
    hints = ["CREATE_NEW_SN", "EXTEND_PATH", "RECALL_SN", "TRIGGER_ACTION", None]
    
    for hint in hints:
        reasoning_input = ReasoningInput(
            trajectory=trajectory,
            wm_decision_hint=hint,
            context={"source": "wm_controller"},
            trace_id="test_trace_002"
        )
        
        output = reasoning_module.process(reasoning_input)
        logger.info(f"WM hint: {hint} → Structure type: {output.structure_type}")


def example_causal_graph_structure():
    """Example: Causal graph structure creation."""
    logger.info("\n=== Example: Causal Graph Structure ===")
    
    # Create reasoning module
    reasoning_module = create_reasoning_module()
    
    # Create trajectory with multiple states
    trajectory = {
        "trace_id": "test_trace_003",
        "states": [
            {"I": 0.5, "P": 0.5, "S": 0.5, "H": 0.5, "A": 0.5, "S_a": 0.5, "theta": 1.0},
            {"I": 0.6, "P": 0.6, "S": 0.6, "H": 0.4, "A": 0.6, "S_a": 0.6, "theta": 1.1},
            {"I": 0.7, "P": 0.7, "S": 0.7, "H": 0.3, "A": 0.7, "S_a": 0.7, "theta": 1.2}
        ],
        "source_modality": "text",
        "timestamp": 0.0
    }
    
    # Create reasoning input with graph hint
    reasoning_input = ReasoningInput(
        trajectory=trajectory,
        wm_decision_hint="CREATE_NEW_SN",
        context={"source": "wm_controller"},
        trace_id="test_trace_003"
    )
    
    # Process
    output = reasoning_module.process(reasoning_input)
    
    logger.info(f"Structure type: {output.structure_type}")
    if isinstance(output.structure, dict) and "nodes" in output.structure:
        logger.info(f"Graph nodes: {len(output.structure['nodes'])}")
        logger.info(f"Graph edges: {len(output.structure['edges'])}")
        logger.info(f"Edges: {output.structure['edges']}")


if __name__ == "__main__":
    example_reasoning_processing()
    example_different_reasoning_types()
    example_causal_graph_structure()

