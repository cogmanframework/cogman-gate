"""
Procedural Field

Purpose: Action weight memory
Spec: docs/MEMORY_FIELD_SPEC.md
"""

from typing import Dict, Any, List, Optional
import time
import math
from .memory_query import EPS8State, MemoryQuery, MemoryResult


class ProceduralField:
    """
    Procedural memory field.
    
    Stores action weights.
    
    Resonance formula:
    Res(S, M) = cosine(S.vector, M.vector) × e^(-|θ_s - θ_m|)
    """
    
    def __init__(self):
        """Initialize procedural field."""
        self.weights: Dict[str, float] = {}
        self.action_states: Dict[str, Dict[str, Any]] = {}  # action -> state mapping
    
    def store(self, action: str, weight: float, state: Optional[Dict[str, Any]] = None):
        """Store procedural memory."""
        self.weights[action] = weight
        if state:
            self.action_states[action] = state
    
    def retrieve(self, action: str) -> float:
        """Retrieve action weight."""
        return self.weights.get(action, 0.0)
    
    def query_resonance(self, state: EPS8State, trace_id: str = "") -> float:
        """
        Query resonance score for given state.
        
        Args:
            state: EPS-8 state
            trace_id: Trace ID for audit
        
        Returns:
            Resonance score [0, 1] (based on action-state matching)
        """
        if not self.action_states:
            return 0.0
        
        # Create state vector from EPS-8
        state_vector = self._eps8_to_vector(state)
        
        # Calculate resonance with all action states
        max_resonance = 0.0
        
        for action, action_state in self.action_states.items():
            # Extract action state vector
            action_vector = self._state_to_vector(action_state)
            if action_vector is None:
                continue
            
            # Calculate cosine similarity
            cosine_sim = self._cosine_similarity(state_vector, action_vector)
            
            # Extract phases
            state_phase = state.theta
            action_phase = action_state.get("theta", 0.0)
            
            # Calculate phase alignment
            phase_diff = abs(state_phase - action_phase)
            phase_alignment = math.exp(-phase_diff)
            
            # Calculate resonance
            resonance = cosine_sim * phase_alignment
            max_resonance = max(max_resonance, resonance)
        
        return max_resonance
    
    def query(self, query: MemoryQuery) -> MemoryResult:
        """
        Query memory with MemoryQuery object.
        
        Args:
            query: MemoryQuery object
        
        Returns:
            MemoryResult with resonance score and matched entries
        """
        resonance_score = self.query_resonance(query.eps8, query.trace_id)
        
        # Find matched actions (simplified)
        matched_entries = []
        if resonance_score > 0.6:  # Threshold for matching
            # Return top actions
            sorted_actions = sorted(
                self.weights.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            matched_entries = [{"action": a, "weight": w} for a, w in sorted_actions]
        
        return MemoryResult(
            resonance_score=resonance_score,
            matched_entries=matched_entries,
            query_type="procedural",
            trace_id=query.trace_id,
            timestamp=time.time()
        )
    
    def _eps8_to_vector(self, state: EPS8State) -> List[float]:
        """Convert EPS-8 state to vector."""
        return [state.I, state.P, state.S, state.H, state.A, state.S_a]
    
    def _state_to_vector(self, state: Dict[str, Any]) -> Optional[List[float]]:
        """Convert state dict to vector."""
        return [
            state.get("I", 0.0),
            state.get("P", 0.0),
            state.get("S", 0.0),
            state.get("H", 0.0),
            state.get("A", 0.0),
            state.get("S_a", 0.0)
        ]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(a * a for a in vec2))
        
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

