"""
Runtime Loop

Purpose: Deterministic execution loop with 9 canonical phases
Spec: docs/RUNTIME_LOOP_SPEC.md
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid
import logging

logger = logging.getLogger(__name__)

# Import for GateCore and Trace integration
try:
    from gate import GateCore
    from perception.trajectory_builder import Trace, TraceManager
    GATE_AVAILABLE = True
except ImportError:
    GATE_AVAILABLE = False
    GateCore = None
    Trace = None
    TraceManager = None


class Phase(Enum):
    """Runtime Loop Phases (CANONICAL ORDER)"""
    IDLE = 0
    INPUT_INTAKE = 1
    SENSORY_ADAPTATION = 2
    PERCEPTION_BOUNDARY = 3
    TRAJECTORY_ADMISSION = 4
    WORKING_MEMORY_CONTROL = 5
    REASONING = 6
    DECISION = 7
    ACTION_OUTPUT = 8
    POST_PROCESSING = 9


@dataclass
class RawInputEnvelope:
    """PHASE 1 Output: Raw input envelope"""
    raw_input: Any
    request_id: str
    timestamp: float
    source_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OriginPack:
    """PHASE 2 Output: Normalized input"""
    raw_signal: Any
    modality: str  # "text" | "image" | "audio"
    timestamp: float
    source_id: str


@dataclass
class EnergeticState:
    """PHASE 3 Output: Energetic state (EPS-8)"""
    I: float
    P: float
    S: float
    H: float
    A: float
    S_a: float
    E_mu: float
    theta: float


@dataclass
class ActionOutput:
    """PHASE 8 Output: Action output"""
    action_type: str
    output_data: Any
    trace_id: str
    timestamp: float


class RuntimeLoop:
    """
    Runtime Loop - Deterministic execution loop with 9 canonical phases.
    
    Rules:
    - MUST execute phases in canonical order
    - MUST NOT skip phases
    - MUST NOT reverse order
    - MUST be deterministic
    """
    
    def __init__(
        self,
        sensory_adapter=None,
        perception_module=None,
        gatecore=None,
        wm_controller=None,
        reasoning_module=None,
        decision_module=None,
        action_module=None,
        post_processor=None,
        trajectory_builder=None
    ):
        """
        Initialize Runtime Loop.
        
        Args:
            sensory_adapter: Sensory adaptation module
            perception_module: Perception boundary module
            gatecore: GateCore admission module
            wm_controller: Working Memory Controller
            reasoning_module: Reasoning module
            decision_module: Decision module
            action_module: Action module
            post_processor: Post-processing module
        """
        self.sensory_adapter = sensory_adapter
        self.perception_module = perception_module
        self.gatecore = gatecore
        self.wm_controller = wm_controller
        self.reasoning_module = reasoning_module
        self.decision_module = decision_module
        self.action_module = action_module
        self.post_processor = post_processor
        self.trajectory_builder = trajectory_builder
        
        self.running = False
        self.current_phase = Phase.IDLE
        self.system_state = "running"  # "running" | "paused" | "sleep"
    
    def run(self):
        """Run Runtime Loop (main execution loop)."""
        self.running = True
        logger.info("Runtime Loop started")
        
        # Import error handler
        try:
            from .error_handler import RuntimeErrorHandler, ErrorSeverity
            error_handler = RuntimeErrorHandler()
        except ImportError:
            error_handler = None
        
        while self.running:
            try:
                self._execute_cycle()
            except Exception as e:
                # Handle error
                if error_handler:
                    error_result = error_handler.handle_error(
                        phase=self.current_phase.name,
                        error=e,
                        context={"system_state": self.system_state},
                        severity=ErrorSeverity.HIGH
                    )
                    logger.error(
                        f"Runtime Loop error in {error_result['phase']}: {e}",
                        exc_info=True
                    )
                else:
                    logger.error(f"Runtime Loop error: {e}", exc_info=True)
                
                # ABORT current cycle, CONTINUE to next
                continue
    
    def stop(self):
        """Stop Runtime Loop."""
        self.running = False
        logger.info("Runtime Loop stopped")
    
    def _execute_cycle(self):
        """Execute one complete cycle (9 phases)."""
        # PHASE 0: Idle / Wait
        self.current_phase = Phase.IDLE
        input_data = self._phase_idle()
        
        if input_data is None:
            return  # No input, wait
        
        # PHASE 1: Input Intake
        self.current_phase = Phase.INPUT_INTAKE
        raw_input = self._phase_input_intake(input_data)
        
        # PHASE 2: Sensory Adaptation
        self.current_phase = Phase.SENSORY_ADAPTATION
        origin = self._phase_sensory_adaptation(raw_input)
        
        # PHASE 3: Perception Boundary
        self.current_phase = Phase.PERCEPTION_BOUNDARY
        eps = self._phase_perception_boundary(origin)
        
        # PHASE 4: Trajectory Admission
        self.current_phase = Phase.TRAJECTORY_ADMISSION
        # Pass origin info for Trace creation
        origin_info = {
            "source_id": raw_input.source_id,
            "modality": origin.modality,
            "adapter": "sensory"
        }
        context_info = {
            "gate_profile": "default",
            "runtime_mode": "normal"
        }
        trajectory = self._phase_trajectory_admission(eps, origin_info, context_info)
        
        if trajectory is None:
            # BLOCKED: log and continue to next input
            logger.info(f"Trajectory blocked: {raw_input.request_id}")
            return
        
        # PHASE 5: Working Memory Control
        self.current_phase = Phase.WORKING_MEMORY_CONTROL
        wm_output = self._phase_working_memory_control(trajectory)
        
        # PHASE 6: Reasoning
        self.current_phase = Phase.REASONING
        reasoning_output = self._phase_reasoning(wm_output)
        
        # PHASE 7: Decision
        self.current_phase = Phase.DECISION
        decision = self._phase_decision(reasoning_output)
        
        # PHASE 8: Action / Output
        self.current_phase = Phase.ACTION_OUTPUT
        action_output = self._phase_action_output(decision, trajectory, reasoning_output)
        
        # PHASE 9: Post-Processing
        self.current_phase = Phase.POST_PROCESSING
        # Collect phase results for metrics
        phase_results = {
            "phase_times": {},  # Would be populated with actual phase times
            "gate_verdict": trajectory.get("verdict"),
            "transformations": [
                {"module": "perception", "timestamp": time.time()},
                {"module": "wm_controller", "timestamp": time.time()},
                {"module": "reasoning", "timestamp": time.time()},
                {"module": "action", "timestamp": time.time()}
            ]
        }
        self._phase_post_processing(trajectory, action_output, phase_results)
    
    def _phase_idle(self) -> Optional[Any]:
        """
        PHASE 0: Idle / Wait
        
        Purpose: Wait for input / event
        """
        # Check system state
        if self.system_state != "running":
            time.sleep(0.1)
            return None
        
        # Wait for input (non-blocking)
        # In real implementation, this would check input queue
        time.sleep(0.01)  # Small delay to prevent busy-wait
        
        # Return input if available (placeholder)
        return None  # No input available
    
    def _phase_input_intake(self, input_data: Any) -> RawInputEnvelope:
        """
        PHASE 1: Input Intake
        
        Purpose: Receive input from external world
        """
        request_id = str(uuid.uuid4())
        timestamp = time.time()
        
        return RawInputEnvelope(
            raw_input=input_data,
            request_id=request_id,
            timestamp=timestamp,
            source_id="external",
            metadata={}
        )
    
    def _phase_sensory_adaptation(self, raw_input: RawInputEnvelope) -> OriginPack:
        """
        PHASE 2: Sensory Adaptation
        
        Purpose: Normalize input
        """
        if self.sensory_adapter is None:
            # Fallback: create minimal OriginPack
            return OriginPack(
                raw_signal=raw_input.raw_input,
                modality="text",
                timestamp=raw_input.timestamp,
                source_id=raw_input.source_id
            )
        
        # Call sensory adapter
        normalized = self.sensory_adapter.adapt(raw_input.raw_input)
        
        return OriginPack(
            raw_signal=normalized,
            modality=normalized.get("modality", "text"),
            timestamp=raw_input.timestamp,
            source_id=raw_input.source_id
        )
    
    def _phase_perception_boundary(self, origin: OriginPack) -> EnergeticState:
        """
        PHASE 3: Perception Boundary
        
        Purpose: Feature extraction → Energy projection
        """
        if self.perception_module is None:
            # Fallback: create minimal EnergeticState
            return EnergeticState(
                I=0.0, P=0.0, S=0.0, H=0.0,
                A=0.0, S_a=0.0, E_mu=0.0, theta=0.0
            )
        
        # Call perception module
        eps_result = self.perception_module.project_energy(origin.raw_signal)
        
        return EnergeticState(
            I=eps_result.get("I", 0.0),
            P=eps_result.get("P", 0.0),
            S=eps_result.get("S", 0.0),
            H=eps_result.get("H", 0.0),
            A=eps_result.get("A", 0.0),
            S_a=eps_result.get("S_a", 0.0),
            E_mu=eps_result.get("E_mu", 0.0),
            theta=eps_result.get("theta", 0.0)
        )
    
    def _phase_trajectory_admission(
        self,
        eps: EnergeticState,
        origin: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """
        PHASE 4: Trajectory Admission
        
        Purpose: GateCore admission check
        
        Rules:
        - Call GateCore for admission
        - Create Trace (via TrajectoryBuilder)
        - If BLOCKED → return None (will be logged and continue)
        - If ALLOW/REVIEW → create trajectory with trace
        
        Args:
            eps: Energetic state (EPS-8)
            origin: Origin information (source_id, modality, adapter)
            context: Context information (gate profile, runtime mode)
        """
        # Prepare origin and context if not provided
        if origin is None:
            origin = {
                "source_id": "runtime_loop",
                "modality": "text",
                "adapter": "default"
            }
        
        if context is None:
            context = {
                "gate_profile": "default",
                "runtime_mode": "normal"
            }
        
        if self.gatecore is None:
            # Fallback: allow all (create minimal trajectory and trace)
            if self.trajectory_builder:
                trace = self.trajectory_builder.create_trace(origin, context)
                trace = TraceManager.transition_trace(trace, "ACTIVE", reason="No GateCore")
                trace_id = trace.trace_id
            else:
                trace_id = str(uuid.uuid4())
            
            return {
                "trace_id": trace_id,
                "eps": eps,
                "verdict": "ALLOW",
                "gate_result": None,
                "trace": trace if self.trajectory_builder else None
            }
        
        # Convert EnergeticState to GateCore format
        from gate import EnergeticState as GateEnergeticState
        gate_eps = GateEnergeticState(
            I=eps.I,
            P=eps.P,
            S=eps.S,
            H=eps.H,
            A=eps.A,
            S_a=eps.S_a,
            E_mu=eps.E_mu,
            theta=eps.theta
        )
        
        # Create Trace first (CREATED state)
        if self.trajectory_builder:
            trace = self.trajectory_builder.create_trace(origin, context)
        else:
            trace = None
        
        # Call GateCore for admission check
        gate_result = self.gatecore.admit(
            gate_eps,
            trace_id=trace.trace_id if trace else None
        )
        
        # Update Trace state based on verdict
        if trace:
            if gate_result.verdict == "BLOCK":
                # BLOCKED: transition to BLOCKED state
                trace = TraceManager.transition_trace(
                    trace,
                    "BLOCKED",
                    reason=gate_result.reason,
                    event_data={
                        "gate_metrics": gate_result.metrics,
                        "verdict": gate_result.verdict
                    }
                )
            else:
                # ALLOW or REVIEW: transition to ACTIVE state
                trace = TraceManager.transition_trace(
                    trace,
                    "ACTIVE",
                    reason=f"GateCore {gate_result.verdict}",
                    event_data={
                        "gate_metrics": gate_result.metrics,
                        "verdict": gate_result.verdict
                    }
                )
        
        # Check verdict
        if gate_result.verdict == "BLOCK":
            # BLOCKED: log and return None (will continue to next input)
            logger.info(
                f"Trajectory admission BLOCKED: {gate_result.reason} "
                f"(trace_id={gate_result.trace_id or (trace.trace_id if trace else 'unknown')})"
            )
            return None  # BLOCKED → None (will be handled by caller)
        
        # ALLOW or REVIEW: create trajectory
        trace_id = gate_result.trace_id or (trace.trace_id if trace else str(uuid.uuid4()))
        
        return {
            "trace_id": trace_id,
            "eps": eps,
            "verdict": gate_result.verdict,
            "gate_result": gate_result,
            "metrics": gate_result.metrics,
            "trace": trace
        }
    
    def _phase_working_memory_control(self, trajectory: Dict[str, Any]) -> Dict[str, Any]:
        """
        PHASE 5: Working Memory Control
        
        Purpose: WM Controller orchestration
        """
        if self.wm_controller is None:
            # Fallback: pass through
            return {"trajectory": trajectory}
        
        # Call WM Controller
        wm_output = self.wm_controller.process(trajectory)
        
        return wm_output
    
    def _phase_reasoning(self, wm_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        PHASE 6: Reasoning
        
        Purpose: Structural reasoning
        
        Rules:
        - Call Reasoning Module with trajectory from WM Controller
        - Receive structured output (graph/plan/tree/simulation)
        - Pass structure to next phase (NO interpretation)
        """
        if self.reasoning_module is None:
            # Fallback: pass through
            return {"structure": None, "structure_type": "none"}
        
        # Import ReasoningInput
        try:
            from reasoning import ReasoningInput
        except ImportError:
            # Fallback: create minimal input
            ReasoningInput = None
        
        # Prepare reasoning input
        trajectory = wm_output.get("trajectory", {})
        wm_decision_hint = wm_output.get("navigation_decision")
        trace_id = wm_output.get("trace_id", trajectory.get("trace_id", ""))
        
        if ReasoningInput:
            reasoning_input = ReasoningInput(
                trajectory=trajectory,
                wm_decision_hint=wm_decision_hint,
                context={"source": "wm_controller"},
                trace_id=trace_id
            )
        else:
            # Fallback: use dict
            reasoning_input = {
                "trajectory": trajectory,
                "wm_decision_hint": wm_decision_hint,
                "context": {"source": "wm_controller"},
                "trace_id": trace_id
            }
        
        # Call Reasoning Module
        if hasattr(self.reasoning_module, 'process'):
            reasoning_output = self.reasoning_module.process(reasoning_input)
            
            # Convert output to dict if needed
            if hasattr(reasoning_output, 'to_dict'):
                return reasoning_output.to_dict()
            else:
                return {
                    "structure_type": getattr(reasoning_output, 'structure_type', 'unknown'),
                    "structure": getattr(reasoning_output, 'structure', None),
                    "assumptions": getattr(reasoning_output, 'assumptions', []),
                    "constraints": getattr(reasoning_output, 'constraints', []),
                    "meta": getattr(reasoning_output, 'meta', {}),
                    "trace_id": trace_id
                }
        else:
            # Fallback: minimal output
            return {"structure": None, "structure_type": "none"}
    
    def _phase_decision(self, reasoning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        PHASE 7: Decision
        
        Purpose: Final decision
        """
        if self.decision_module is None:
            # Fallback: pass through
            return {"decision": "ALLOW"}
        
        # Call Decision Module
        decision = self.decision_module.decide(reasoning_output)
        
        return decision
    
    def _phase_action_output(
        self,
        decision: Dict[str, Any],
        trajectory: Dict[str, Any],
        reasoning_output: Optional[Dict[str, Any]] = None
    ) -> ActionOutput:
        """
        PHASE 8: Action / Output
        
        Purpose: Execute action
        
        Rules:
        - Call Action Module with decision
        - Pass reasoning output structure (if available)
        - Generate observable output
        - Attach trace_id
        - NO decision making
        - NO evaluation
        """
        trace_id = trajectory.get("trace_id", str(uuid.uuid4()))
        
        if self.action_module is None:
            # Fallback: create minimal output
            return ActionOutput(
                action_type="none",
                output_data=None,
                trace_id=trace_id,
                timestamp=time.time()
            )
        
        # Call Action Module
        # Import ActionOutput if available
        try:
            from action import ActionOutput as ActionModuleOutput
        except ImportError:
            ActionModuleOutput = None
        
        if hasattr(self.action_module, 'execute'):
            # Call Action Module execute method
            action_output = self.action_module.execute(
                decision=decision,
                trace_id=trace_id,
                reasoning_output=reasoning_output,
                trajectory=trajectory
            )
            
            # Convert to Runtime Loop ActionOutput format
            if hasattr(action_output, 'to_dict'):
                output_dict = action_output.to_dict()
                return ActionOutput(
                    action_type=output_dict.get("action_type", "none"),
                    output_data=output_dict.get("output_data"),
                    trace_id=trace_id,
                    timestamp=output_dict.get("timestamp", time.time())
                )
            elif isinstance(action_output, dict):
                return ActionOutput(
                    action_type=action_output.get("action_type", "none"),
                    output_data=action_output.get("output_data"),
                    trace_id=trace_id,
                    timestamp=action_output.get("timestamp", time.time())
                )
            else:
                # Fallback: use action_output directly if it's already ActionOutput
                return action_output
        else:
            # Fallback: minimal output
            return ActionOutput(
                action_type="none",
                output_data=None,
                trace_id=trace_id,
                timestamp=time.time()
            )
    
    def _phase_post_processing(
        self,
        trajectory: Dict[str, Any],
        action_output: ActionOutput,
        phase_results: Optional[Dict[str, Any]] = None
    ):
        """
        PHASE 9: Post-Processing
        
        Purpose: Logging, audit, metrics
        
        Rules:
        - MUST NOT affect current loop
        - MUST NOT block execution
        - MUST be asynchronous (if possible)
        - No state modification
        - No decision influence
        - No blocking operations
        """
        if self.post_processor is None:
            # Fallback: basic logging
            trace_id = getattr(action_output, 'trace_id', trajectory.get("trace_id", "unknown"))
            logger.info(f"Trace {trace_id} completed")
            return
        
        # Call Post-Processor (async if possible)
        self.post_processor.process(
            trajectory=trajectory,
            action_output=action_output,
            phase_results=phase_results or {}
        )
