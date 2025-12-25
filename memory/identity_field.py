"""
Identity Field

Purpose: Identity / self memory
Spec: docs/MEMORY_FIELD_SPEC.md
"""

from typing import Dict, Any, Optional
import time
import math
from .memory_query import EPS8State, MemoryQuery, MemoryResult


class IdentityField:
    """
    Identity memory field.
    
    Stores identity/self memories.
    
    Resonance formula:
    Res(S, M) = cosine(S.vector, M.vector) × e^(-|θ_s - θ_m|)
    """
    
    def __init__(self):
        """Initialize identity field."""
        self.identity: Dict[str, Any] = {}
        self.baselines: Dict[str, float] = {}  # Baseline values
    
    def store(self, identity: Dict[str, Any]):
        """Store identity memory."""
        self.identity.update(identity)
        # Extract baselines if available
        if "baselines" in identity:
            self.baselines.update(identity["baselines"])
    
    def retrieve(self) -> Dict[str, Any]:
        """Retrieve identity."""
        return self.identity
    
    def query_resonance(self, state: EPS8State, trace_id: str = "") -> float:
        """
        Query resonance score for given state.
        
        Identity field resonance is based on deviation from baselines.
        
        Args:
            state: EPS-8 state
            trace_id: Trace ID for audit
        
        Returns:
            Resonance score [0, 1] (1.0 = matches baseline, 0.0 = far from baseline)
        """
        if not self.baselines:
            return 0.5  # Default if no baselines
        
        # Create state vector from EPS-8
        state_vector = self._eps8_to_vector(state)
        
        # Create baseline vector
        baseline_vector = self._baselines_to_vector()
        
        # Calculate cosine similarity (how close to baseline)
        cosine_sim = self._cosine_similarity(state_vector, baseline_vector)
        
        # Identity resonance is based on how close to baseline
        return max(0.0, min(1.0, cosine_sim))
    
    def query(self, query: MemoryQuery) -> MemoryResult:
        """
        Query memory with MemoryQuery object.
        
        Args:
            query: MemoryQuery object
        
        Returns:
            MemoryResult with resonance score and matched entries
        """
        resonance_score = self.query_resonance(query.eps8, query.trace_id)
        
        # Identity field returns identity info
        matched_entries = [self.identity] if resonance_score > 0.5 else []
        
        return MemoryResult(
            resonance_score=resonance_score,
            matched_entries=matched_entries,
            query_type="identity",
            trace_id=query.trace_id,
            timestamp=time.time()
        )
    
    def _eps8_to_vector(self, state: EPS8State) -> List[float]:
        """Convert EPS-8 state to vector."""
        return [state.I, state.P, state.S, state.H, state.A, state.S_a]
    
    def _baselines_to_vector(self) -> List[float]:
        """Convert baselines to vector."""
        return [
            self.baselines.get("I", 0.5),
            self.baselines.get("P", 0.5),
            self.baselines.get("S", 0.5),
            self.baselines.get("H", 0.5),
            self.baselines.get("A", 0.5),
            self.baselines.get("S_a", 0.5)
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

