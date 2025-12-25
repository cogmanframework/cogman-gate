"""
Memory Query Interface

Purpose: Query interface for memory fields
Spec: docs/MEMORY_FIELD_SPEC.md
"""

from typing import Dict, Any, Literal, Optional
from dataclasses import dataclass
import time


@dataclass
class EPS8State:
    """EPS-8 State for memory queries"""
    I: float
    P: float
    S: float
    H: float
    F: float
    A: float
    S_a: float
    theta: float


@dataclass
class MemoryQuery:
    """
    Memory Query Structure
    
    Spec: docs/MEMORY_FIELD_SPEC.md
    """
    eps8: EPS8State
    query_type: Literal[
        "episodic",
        "semantic",
        "procedural",
        "identity"
    ]
    resonance_params: Dict[str, Any]
    trace_id: str
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert query to dictionary."""
        return {
            "eps8": {
                "I": self.eps8.I,
                "P": self.eps8.P,
                "S": self.eps8.S,
                "H": self.eps8.H,
                "F": self.eps8.F,
                "A": self.eps8.A,
                "S_a": self.eps8.S_a,
                "theta": self.eps8.theta
            },
            "query_type": self.query_type,
            "resonance_params": self.resonance_params,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp
        }


@dataclass
class MemoryResult:
    """
    Memory Query Result
    
    Spec: docs/MEMORY_FIELD_SPEC.md
    """
    resonance_score: float  # [0, 1]
    matched_entries: list  # List of matched memory entries
    query_type: str
    trace_id: str
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "resonance_score": self.resonance_score,
            "matched_entries": self.matched_entries,
            "query_type": self.query_type,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp
        }

