"""
Semantic Field

Purpose: Principle / pattern memory
Spec: docs/MEMORY_FIELD_SPEC.md
"""

from typing import Dict, Any, List, Optional
import time
import math
from .memory_query import EPS8State, MemoryQuery, MemoryResult


class SemanticField:
    """
    Semantic memory field.
    
    Stores principle and pattern memories.
    
    Resonance formula:
    Res(S, M) = cosine(S.vector, M.vector) × e^(-|θ_s - θ_m|)
    """
    
    def __init__(self):
        """Initialize semantic field."""
        self.memories: List[Dict[str, Any]] = []
    
    def store(self, principle: Dict[str, Any]):
        """Store semantic memory."""
        self.memories.append(principle)
    
    def retrieve(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve semantic memories."""
        # Placeholder: Simple retrieval
        return self.memories
    
    def query_resonance(self, state: EPS8State, trace_id: str = "") -> float:
        """
        Query resonance score for given state.
        
        Args:
            state: EPS-8 state
            trace_id: Trace ID for audit
        
        Returns:
            Resonance score [0, 1]
        """
        if not self.memories:
            return 0.0
        
        # Create state vector from EPS-8
        state_vector = self._eps8_to_vector(state)
        
        # Calculate resonance with all memories
        max_resonance = 0.0
        
        for memory in self.memories:
            # Extract memory vector
            memory_vector = self._memory_to_vector(memory)
            if memory_vector is None:
                continue
            
            # Calculate cosine similarity
            cosine_sim = self._cosine_similarity(state_vector, memory_vector)
            
            # Extract phases
            state_phase = state.theta
            memory_phase = memory.get("theta", 0.0)
            
            # Calculate phase alignment
            phase_diff = abs(state_phase - memory_phase)
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
        
        # Find matched entries (simplified)
        matched_entries = []
        if resonance_score > 0.7:  # Higher threshold for semantic
            matched_entries = self.memories[:2]  # Top 2
        
        return MemoryResult(
            resonance_score=resonance_score,
            matched_entries=matched_entries,
            query_type="semantic",
            trace_id=query.trace_id,
            timestamp=time.time()
        )
    
    def _eps8_to_vector(self, state: EPS8State) -> List[float]:
        """Convert EPS-8 state to vector."""
        return [state.I, state.P, state.S, state.H, state.A, state.S_a]
    
    def _memory_to_vector(self, memory: Dict[str, Any]) -> Optional[List[float]]:
        """Convert memory to vector."""
        # Extract pattern vector from memory
        pattern = memory.get("pattern", {})
        if not pattern:
            return None
        
        return [
            pattern.get("I", 0.0),
            pattern.get("P", 0.0),
            pattern.get("S", 0.0),
            pattern.get("H", 0.0),
            pattern.get("A", 0.0),
            pattern.get("S_a", 0.0)
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

