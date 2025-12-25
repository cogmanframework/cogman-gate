"""
GateCore Adapter for Runtime Loop

Purpose: Adapter layer between Runtime Loop and GateCore
"""

from typing import Dict, Any, Optional
from gate import GateCore, GateCoreResult, EnergeticState as GateEnergeticState
from runtime.main_loop import EnergeticState
from perception.trajectory_builder import TrajectoryBuilder, Trace, TraceManager


class GateCoreAdapter:
    """
    GateCore Adapter
    
    Purpose: Bridge between Runtime Loop and GateCore,
    including Trace creation and lifecycle management.
    """
    
    def __init__(
        self,
        gatecore: GateCore,
        trajectory_builder: Optional[TrajectoryBuilder] = None
    ):
        """
        Initialize GateCore Adapter.
        
        Args:
            gatecore: GateCore instance
            trajectory_builder: TrajectoryBuilder instance (optional)
        """
        self.gatecore = gatecore
        self.trajectory_builder = trajectory_builder or TrajectoryBuilder()
    
    def admit_with_trace(
        self,
        eps: EnergeticState,
        origin: Dict[str, Any],
        context: Dict[str, Any],
        E_mu_history: Optional[list] = None
    ) -> tuple[Optional[Trace], Optional[GateCoreResult]]:
        """
        Admission check with Trace creation.
        
        This is the full PHASE 4 operation:
        1. Create Trace (CREATED state)
        2. Call GateCore for admission
        3. Update Trace state based on verdict
        
        Args:
            eps: Energetic state (EPS-8)
            origin: Origin information (source_id, modality, adapter)
            context: Context information (gate profile, runtime mode)
            E_mu_history: Eμ history for T/V calculation (optional)
        
        Returns:
            Tuple of (Trace, GateCoreResult)
            - If BLOCKED: (Trace in BLOCKED state, GateCoreResult)
            - If ALLOW/REVIEW: (Trace in ACTIVE state, GateCoreResult)
            - If error: (None, None)
        """
        # Step 1: Create Trace (CREATED state)
        trace = self.trajectory_builder.create_trace(origin, context)
        
        # Step 2: Convert EnergeticState to GateCore format
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
        
        # Step 3: Call GateCore for admission
        gate_result = self.gatecore.admit(
            gate_eps,
            trace_id=trace.trace_id,
            E_mu_history=E_mu_history
        )
        
        # Step 4: Update Trace state based on verdict
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
        
        return trace, gate_result
    
    def convert_eps(self, eps: EnergeticState) -> GateEnergeticState:
        """Convert Runtime Loop EnergeticState to GateCore format."""
        return GateEnergeticState(
            I=eps.I,
            P=eps.P,
            S=eps.S,
            H=eps.H,
            A=eps.A,
            S_a=eps.S_a,
            E_mu=eps.E_mu,
            theta=eps.theta
        )

