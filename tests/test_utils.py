"""
Test Utilities

Purpose: Common utilities for testing
"""

from typing import Dict, Any
import time
import uuid


def create_test_eps8_state(
    I: float = 0.7,
    P: float = 0.6,
    S: float = 0.8,
    H: float = 0.3,
    A: float = 0.5,
    S_a: float = 0.4,
    E_mu: float = 50.0,
    theta: float = 1.2
) -> Dict[str, float]:
    """Create test EPS-8 state dictionary."""
    return {
        "I": I,
        "P": P,
        "S": S,
        "H": H,
        "A": A,
        "S_a": S_a,
        "E_mu": E_mu,
        "theta": theta
    }


def create_test_trajectory(
    trace_id: str = None,
    state_count: int = 3
) -> Dict[str, Any]:
    """Create test trajectory."""
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    states = []
    for i in range(state_count):
        states.append(create_test_eps8_state(
            I=0.7 + i * 0.1,
            H=0.3 - i * 0.1
        ))
    
    return {
        "trace_id": trace_id,
        "states": states,
        "source_modality": "text",
        "timestamp": time.time()
    }


def create_test_decision(
    decision: str = "ALLOW",
    type: str = "text"
) -> Dict[str, Any]:
    """Create test decision."""
    return {
        "decision": decision,
        "type": type,
        "reason": "Test decision"
    }


def create_test_reasoning_output(
    structure_type: str = "graph"
) -> Dict[str, Any]:
    """Create test reasoning output."""
    return {
        "structure_type": structure_type,
        "structure": {
            "nodes": ["A", "B", "C"],
            "edges": [("A", "B"), ("B", "C")]
        },
        "assumptions": ["Test assumption"],
        "constraints": ["Test constraint"],
        "meta": {},
        "trace_id": str(uuid.uuid4()),
        "timestamp": time.time()
    }

