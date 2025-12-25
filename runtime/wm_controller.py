"""
Working Memory Controller

Purpose: Central control unit for system orchestration
Spec: docs/WM_CONTROLLER_SPEC.md
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class EPS8State:
    """EPS-8 State (8 dimensions)"""
    I: float
    P: float
    S: float
    H: float
    F: float
    A: float
    S_a: float
    theta: float


@dataclass
class Trajectory:
    """Trajectory structure"""
    states: List[EPS8State]
    trace_id: str
    source_modality: str
    timestamp: float
    debug_lineage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WMControllerOutput:
    """WM Controller Output"""
    trajectory: Trajectory
    navigation_decision: str
    modulated_eps8: EPS8State
    resonance_scores: Dict[str, float]
    gate_status: Dict[str, bool]
    trace_id: str
    timestamp: float


class WMController:
    """
    Working Memory Controller - Central control unit.
    
    Responsibilities:
    1. Gate Control (pass / block)
    2. Routing (where to go next)
    3. Context Modulation (minor energy adjustment)
    4. Memory Resonance Invocation (call memory)
    5. Navigation Decision (select system path)
    """
    
    def __init__(
        self,
        gatecore=None,
        memory_fields=None,
        config=None
    ):
        """
        Initialize WM Controller.
        
        Args:
            gatecore: GateCore module
            memory_fields: Memory fields (episodic, semantic, procedural, identity)
            config: Configuration (thresholds, etc.)
        """
        self.gatecore = gatecore
        self.memory_fields = memory_fields or {}
        self.config = config or {}
        
        # Gate thresholds from config
        self.H_max = self.config.get("H_max", 0.62)
        self.S_min = self.config.get("S_min", 0.5)
        self.budget_max = self.config.get("budget_max", 100.0)
    
    def process(self, trajectory: Dict[str, Any]) -> WMControllerOutput:
        """
        Process trajectory through WM Controller.
        
        Args:
            trajectory: Trajectory dictionary (from Runtime Loop)
        
        Returns:
            WMControllerOutput
        """
        # Convert trajectory dict to Trajectory object
        traj = self._dict_to_trajectory(trajectory)
        
        # Get current state (last state in trajectory)
        current_state = traj.states[-1] if traj.states else self._create_default_state()
        
        # STEP 1: Gate Control (FIRST STEP)
        gate_status = self._gate_control(current_state)
        
        if not all(gate_status.values()):
            # Gate failed → BLOCKED
            return WMControllerOutput(
                trajectory=traj,
                navigation_decision="BLOCKED",
                modulated_eps8=current_state,
                resonance_scores={},
                gate_status=gate_status,
                trace_id=traj.trace_id,
                timestamp=time.time()
            )
        
        # STEP 2: Memory Resonance Invocation
        resonance_scores = self._invoke_memory_resonance(current_state)
        
        # STEP 3: Context Modulation
        modulated_eps8 = self._context_modulation(current_state, resonance_scores)
        
        # STEP 4: Navigation Decision
        navigation_decision = self._navigation_decision(
            current_state,
            resonance_scores,
            modulated_eps8
        )
        
        # Update trajectory with new state
        traj.states.append(modulated_eps8)
        
        return WMControllerOutput(
            trajectory=traj,
            navigation_decision=navigation_decision,
            modulated_eps8=modulated_eps8,
            resonance_scores=resonance_scores,
            gate_status=gate_status,
            trace_id=traj.trace_id,
            timestamp=time.time()
        )
    
    def _gate_control(self, state: EPS8State) -> Dict[str, bool]:
        """
        Gate Control Layer (FIRST STEP)
        
        Gates (in order):
        1. Entropy Gate
        2. Safety Gate
        3. Budget Gate
        """
        gate_status = {
            "entropy": True,
            "safety": True,
            "budget": True
        }
        
        # 1. Entropy Gate
        if state.H > self.H_max:
            gate_status["entropy"] = False
            logger.warning(f"Entropy gate failed: H={state.H} > H_max={self.H_max}")
        
        # 2. Safety Gate (call GateCore if available)
        if self.gatecore is not None:
            safety_result = self.gatecore.evaluate_safety(state)
            gate_status["safety"] = safety_result.get("pass", False)
        else:
            # Fallback: check S (stability)
            if state.S < self.S_min:
                gate_status["safety"] = False
                logger.warning(f"Safety gate failed: S={state.S} < S_min={self.S_min}")
        
        # 3. Budget Gate (placeholder - would check resource budget)
        # For now, always pass
        gate_status["budget"] = True
        
        return gate_status
    
    def _invoke_memory_resonance(self, state: EPS8State) -> Dict[str, float]:
        """
        Memory Resonance Invocation
        
        Calculate resonance scores for each memory field.
        
        Uses canonical resonance formula:
        Res(S, M) = cosine(S.vector, M.vector) × e^(-|θ_s - θ_m|)
        """
        resonance_scores = {}
        
        if not self.memory_fields:
            return resonance_scores
        
        # Import MemoryQuery for proper query interface
        try:
            from memory import MemoryQuery, EPS8State as MemoryEPS8State
        except ImportError:
            # Fallback: use direct query_resonance
            MemoryQuery = None
            MemoryEPS8State = None
        
        # Calculate resonance for each memory field
        for field_name, memory_field in self.memory_fields.items():
            if memory_field is None:
                continue
            
            try:
                # Convert WM Controller EPS8State to Memory EPS8State
                if MemoryEPS8State:
                    memory_state = MemoryEPS8State(
                        I=state.I,
                        P=state.P,
                        S=state.S,
                        H=state.H,
                        F=state.F,
                        A=state.A,
                        S_a=state.S_a,
                        theta=state.theta
                    )
                else:
                    # Fallback: use state directly if query_resonance accepts it
                    memory_state = state
                
                # Query resonance
                if hasattr(memory_field, 'query_resonance'):
                    score = memory_field.query_resonance(memory_state, trace_id="")
                else:
                    # Fallback: default score
                    logger.warning(f"Memory field {field_name} does not have query_resonance method")
                    score = 0.0
                
                resonance_scores[field_name] = score
                
            except Exception as e:
                logger.warning(f"Memory resonance query failed for {field_name}: {e}")
                resonance_scores[field_name] = 0.0
        
        return resonance_scores
    
    def _context_modulation(
        self,
        state: EPS8State,
        resonance_scores: Dict[str, float]
    ) -> EPS8State:
        """
        Context Modulation
        
        Minor energy adjustment based on context/resonance.
        """
        # Simple modulation: adjust I (intensity) based on resonance
        modulation_factor = 1.0
        
        # If strong episodic resonance, slightly increase I
        episodic_resonance = resonance_scores.get("episodic", 0.0)
        if episodic_resonance > 0.7:
            modulation_factor = 1.1
        
        # If strong semantic resonance, slightly increase S
        semantic_resonance = resonance_scores.get("semantic", 0.0)
        if semantic_resonance > 0.8:
            modulation_factor = 1.05
        
        # Apply modulation (minor adjustment only)
        modulated = EPS8State(
            I=state.I * modulation_factor,
            P=state.P,
            S=min(state.S * 1.05 if semantic_resonance > 0.8 else state.S, 1.0),
            H=state.H,
            F=state.F,
            A=state.A,
            S_a=state.S_a,
            theta=state.theta
        )
        
        return modulated
    
    def _navigation_decision(
        self,
        state: EPS8State,
        resonance_scores: Dict[str, float],
        modulated_eps8: EPS8State
    ) -> str:
        """
        Navigation Decision
        
        Select system path based on state and resonance.
        """
        # Decision logic (deterministic, no randomness)
        
        # 1. Check for strong episodic resonance
        episodic_resonance = resonance_scores.get("episodic", 0.0)
        if episodic_resonance > 0.7:
            return "EXTEND_PATH"
        
        # 2. Check for strong semantic resonance
        semantic_resonance = resonance_scores.get("semantic", 0.0)
        if semantic_resonance > 0.8:
            return "RECALL_SN"
        
        # 3. Check for high intensity and stability
        if modulated_eps8.I > 0.8 and modulated_eps8.S > 0.7:
            return "TRIGGER_ACTION"
        
        # 4. Check for low entropy (reflex)
        if modulated_eps8.H < 0.2:
            return "ACTIVATE_REFLEX"
        
        # 5. Default: create new semantic node
        return "CREATE_NEW_SN"
    
    def _dict_to_trajectory(self, traj_dict: Dict[str, Any]) -> Trajectory:
        """Convert trajectory dict to Trajectory object."""
        states = []
        
        # Convert EPS states
        if "eps" in traj_dict:
            eps = traj_dict["eps"]
            states.append(EPS8State(
                I=eps.get("I", 0.0),
                P=eps.get("P", 0.0),
                S=eps.get("S", 0.0),
                H=eps.get("H", 0.0),
                F=eps.get("F", 0.0),
                A=eps.get("A", 0.0),
                S_a=eps.get("S_a", 0.0),
                theta=eps.get("theta", 0.0)
            ))
        
        return Trajectory(
            states=states,
            trace_id=traj_dict.get("trace_id", ""),
            source_modality=traj_dict.get("source_modality", "text"),
            timestamp=traj_dict.get("timestamp", time.time()),
            debug_lineage=traj_dict.get("debug_lineage", {})
        )
    
    def _create_default_state(self) -> EPS8State:
        """Create default EPS-8 state."""
        return EPS8State(
            I=0.0, P=0.0, S=0.0, H=0.0,
            F=0.0, A=0.0, S_a=0.0, theta=0.0
        )

