"""
Example: Memory Integration with WM Controller

Purpose: Demonstrate Memory resonance integration with WM Controller
"""

import logging
from memory import (
    EpisodicField, SemanticField, ProceduralField, IdentityField,
    MemoryQuery, EPS8State
)
from runtime import WMController, EPS8State as WMEPS8State

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_memory_fields():
    """Create memory fields with sample data."""
    # Episodic Field
    episodic = EpisodicField()
    episodic.store({
        "I": 0.7,
        "P": 0.6,
        "S": 0.8,
        "H": 0.3,
        "A": 0.5,
        "S_a": 0.4,
        "theta": 1.2
    })
    
    # Semantic Field
    semantic = SemanticField()
    semantic.store({
        "pattern": {
            "I": 0.6,
            "P": 0.5,
            "S": 0.7,
            "H": 0.4,
            "A": 0.5,
            "S_a": 0.4
        },
        "theta": 1.0,
        "stability": 0.8
    })
    
    # Procedural Field
    procedural = ProceduralField()
    procedural.store("action_1", 0.8, {
        "I": 0.7,
        "P": 0.6,
        "S": 0.8,
        "H": 0.3,
        "A": 0.5,
        "S_a": 0.4,
        "theta": 1.2
    })
    
    # Identity Field
    identity = IdentityField()
    identity.store({
        "baselines": {
            "I": 0.5,
            "P": 0.5,
            "S": 0.5,
            "H": 0.5,
            "A": 0.5,
            "S_a": 0.5
        }
    })
    
    return {
        "episodic": episodic,
        "semantic": semantic,
        "procedural": procedural,
        "identity": identity
    }


def example_memory_resonance():
    """Example: Direct memory resonance query."""
    logger.info("=== Example: Memory Resonance Query ===")
    
    # Create memory fields
    memory_fields = create_memory_fields()
    
    # Create test state
    test_state = EPS8State(
        I=0.7,
        P=0.6,
        S=0.8,
        H=0.3,
        F=0.0,
        A=0.5,
        S_a=0.4,
        theta=1.2
    )
    
    # Query each memory field
    for field_name, field in memory_fields.items():
        resonance = field.query_resonance(test_state, trace_id="test_001")
        logger.info(f"{field_name} resonance: {resonance:.3f}")
        
        # Query with MemoryQuery object
        query = MemoryQuery(
            eps8=test_state,
            query_type=field_name,
            resonance_params={"threshold": 0.5},
            trace_id="test_001",
            timestamp=0.0
        )
        
        result = field.query(query)
        logger.info(f"{field_name} query result: score={result.resonance_score:.3f}, "
                   f"matched={len(result.matched_entries)} entries")


def example_wm_controller_with_memory():
    """Example: WM Controller with Memory integration."""
    logger.info("\n=== Example: WM Controller with Memory ===")
    
    # Create memory fields
    memory_fields = create_memory_fields()
    
    # Create WM Controller
    wm_controller = WMController(
        memory_fields=memory_fields,
        config={
            "H_max": 0.65,
            "S_min": 0.5
        }
    )
    
    # Create test trajectory
    from runtime.wm_controller import Trajectory
    test_state = WMEPS8State(
        I=0.7,
        P=0.6,
        S=0.8,
        H=0.3,
        F=0.0,
        A=0.5,
        S_a=0.4,
        theta=1.2
    )
    
    trajectory = Trajectory(
        states=[test_state],
        trace_id="test_trace_001",
        source_modality="text",
        timestamp=0.0
    )
    
    # Process trajectory through WM Controller
    result = wm_controller.process({"trace_id": "test_trace_001", "eps": {
        "I": test_state.I,
        "P": test_state.P,
        "S": test_state.S,
        "H": test_state.H,
        "A": test_state.A,
        "S_a": test_state.S_a,
        "theta": test_state.theta
    }})
    
    logger.info(f"Navigation decision: {result.navigation_decision}")
    logger.info(f"Resonance scores: {result.resonance_scores}")
    logger.info(f"Gate status: {result.gate_status}")


def example_resonance_formula():
    """Example: Demonstrate resonance formula calculation."""
    logger.info("\n=== Example: Resonance Formula ===")
    
    # Create episodic field
    episodic = EpisodicField()
    
    # Store a memory
    episodic.store({
        "I": 0.7,
        "P": 0.6,
        "S": 0.8,
        "H": 0.3,
        "A": 0.5,
        "S_a": 0.4,
        "theta": 1.2
    })
    
    # Test with similar state (should have high resonance)
    similar_state = EPS8State(
        I=0.7,
        P=0.6,
        S=0.8,
        H=0.3,
        F=0.0,
        A=0.5,
        S_a=0.4,
        theta=1.2  # Same phase
    )
    
    resonance_similar = episodic.query_resonance(similar_state)
    logger.info(f"Similar state resonance: {resonance_similar:.3f}")
    
    # Test with different state (should have lower resonance)
    different_state = EPS8State(
        I=0.3,
        P=0.2,
        S=0.4,
        H=0.7,
        F=0.0,
        A=0.2,
        S_a=0.3,
        theta=0.5  # Different phase
    )
    
    resonance_different = episodic.query_resonance(different_state)
    logger.info(f"Different state resonance: {resonance_different:.3f}")
    
    logger.info(f"Resonance difference: {resonance_similar - resonance_different:.3f}")


if __name__ == "__main__":
    example_memory_resonance()
    example_wm_controller_with_memory()
    example_resonance_formula()

