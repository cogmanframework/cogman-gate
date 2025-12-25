"""
LLM Integration Test Tool

Purpose: Test LLM integration manually
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from llm import Annotation
from llm.prompt_templates import PromptTemplates
from llm.response_formatter import ResponseFormatter


def test_basic_annotation():
    """Test basic LLM annotation."""
    print("=== Test Basic Annotation ===")
    
    annotation = Annotation()
    content = "Test content for annotation"
    
    result = annotation.annotate(content)
    print(f"Input: {content}")
    print(f"Output: {result}")
    print()


def test_gate_decision_annotation():
    """Test annotating gate decision."""
    print("=== Test Gate Decision Annotation ===")
    
    annotation = Annotation()
    
    gate_decision = {
        "verdict": "ALLOW",
        "reason": "Low entropy (H=0.3)",
        "metrics": {
            "H": 0.3,
            "D": 0.2,
            "S": 1.0
        }
    }
    
    result = annotation.annotate(
        str(gate_decision),
        context={"type": "gate_decision", "decision": gate_decision}
    )
    
    print(f"Gate Decision: {gate_decision}")
    print(f"Annotated: {result}")
    print()


def test_energy_state_annotation():
    """Test annotating energy state."""
    print("=== Test Energy State Annotation ===")
    
    annotation = Annotation()
    
    energy_state = {
        "I": 0.7,
        "P": 0.6,
        "S": 0.8,
        "H": 0.3,
        "A": 0.5,
        "S_a": 0.4,
        "E_mu": 50.0,
        "theta": 1.2
    }
    
    result = annotation.annotate(
        str(energy_state),
        context={"type": "energy_state", "state": energy_state}
    )
    
    print(f"Energy State: {energy_state}")
    print(f"Annotated: {result}")
    print()


def test_trajectory_annotation():
    """Test annotating trajectory."""
    print("=== Test Trajectory Annotation ===")
    
    annotation = Annotation()
    
    trajectory = {
        "trace_id": "test_001",
        "states": [
            {"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3},
            {"I": 0.8, "P": 0.7, "S": 0.9, "H": 0.2}
        ],
        "source_modality": "text"
    }
    
    result = annotation.annotate(
        str(trajectory),
        context={"type": "trajectory", "trajectory": trajectory}
    )
    
    print(f"Trajectory: {trajectory}")
    print(f"Annotated: {result}")
    print()


def main():
    """Main test function."""
    print("LLM Integration Test Tool")
    print("=" * 50)
    print()
    
    try:
        test_basic_annotation()
        test_gate_decision_annotation()
        test_energy_state_annotation()
        test_trajectory_annotation()
        
        print("=" * 50)
        print("All tests completed")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

