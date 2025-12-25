"""
GateCore (CORE-9) Integration

Purpose: GateCore adapter for Runtime Loop integration
Spec: docs/GATECORE_SPEC.md
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time
import logging

from .decision_gate import DecisionGate
from .gate_policy import GatePolicy
from .gate_trace import GateTrace

logger = logging.getLogger(__name__)


@dataclass
class EnergeticState:
    """Energetic State (EPS-8)"""
    I: float
    P: float
    S: float
    H: float
    A: float
    S_a: float
    E_mu: float
    theta: float


@dataclass
class GateCoreResult:
    """GateCore admission result"""
    verdict: str  # "ALLOW", "REVIEW", "BLOCK"
    reason: str
    metrics: Dict[str, float]
    trace_id: Optional[str] = None
    timestamp: float = 0.0


class GateCore:
    """
    GateCore (CORE-9) - Final authority for admission decisions.
    
    Purpose:
    - Admission check for trajectories
    - Safety gate enforcement
    - Deterministic decision making
    
    Spec: docs/GATECORE_SPEC.md
    """
    
    def __init__(
        self,
        decision_gate: DecisionGate,
        gate_trace: Optional[GateTrace] = None,
        context: str = "default"
    ):
        """
        Initialize GateCore.
        
        Args:
            decision_gate: DecisionGate instance
            gate_trace: GateTrace instance (optional)
            context: Application context (robot_control, chat, finance, etc.)
        """
        self.decision_gate = decision_gate
        self.gate_trace = gate_trace or GateTrace()
        self.context = context
    
    def admit(
        self,
        eps: EnergeticState,
        trace_id: Optional[str] = None,
        E_mu_history: Optional[List[float]] = None
    ) -> GateCoreResult:
        """
        Admission check for trajectory.
        
        This is the PHASE 4 operation in Runtime Loop.
        
        Args:
            eps: Energetic state (EPS-8)
            trace_id: Trace identifier (optional)
            E_mu_history: Eμ history for T/V calculation (optional)
        
        Returns:
            GateCoreResult with verdict and reason
        """
        # Prepare metrics for decision gate
        metrics = self._prepare_metrics(eps, E_mu_history)
        
        # Call decision gate
        verdict = self.decision_gate.decide(metrics)
        
        # Determine reason
        reason = self._determine_reason(verdict, eps, metrics)
        
        # Create result
        result = GateCoreResult(
            verdict=verdict,
            reason=reason,
            metrics=metrics,
            trace_id=trace_id,
            timestamp=time.time()
        )
        
        # Trace decision
        self.gate_trace.trace(
            decision=verdict,
            state={
                "I": eps.I,
                "P": eps.P,
                "S": eps.S,
                "H": eps.H,
                "A": eps.A,
                "S_a": eps.S_a,
                "E_mu": eps.E_mu,
                "theta": eps.theta
            },
            reason=reason
        )
        
        logger.info(
            f"GateCore admission: {verdict} "
            f"(trace_id={trace_id}, H={eps.H:.3f}, S={eps.S:.3f}, E_mu={eps.E_mu:.3f})"
        )
        
        return result
    
    def evaluate_safety(self, eps: EnergeticState) -> Dict[str, Any]:
        """
        Evaluate safety (for WM Controller).
        
        Args:
            eps: Energetic state
        
        Returns:
            Safety evaluation result
        """
        # Simple safety check: S (stability) must be above threshold
        policy = self.decision_gate.policy
        config = policy.get_params()
        S_min = config.get("S_min", 0.5)
        
        safety_pass = eps.S >= S_min
        
        return {
            "pass": safety_pass,
            "S": eps.S,
            "S_min": S_min,
            "reason": "Safety gate passed" if safety_pass else f"S={eps.S:.3f} < S_min={S_min}"
        }
    
    def _prepare_metrics(
        self,
        eps: EnergeticState,
        E_mu_history: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Prepare metrics for decision gate.
        
        Args:
            eps: Energetic state
            E_mu_history: Eμ history (optional)
        
        Returns:
            Metrics dictionary
        """
        metrics = {
            "I": eps.I,
            "P": eps.P,
            "S": eps.S,
            "H": eps.H,
            "A": eps.A,
            "S_a": eps.S_a,
            "E_mu": eps.E_mu,
            "theta": eps.theta,
            "D_traj": 0.0,  # Semantic drift (would be calculated from trajectory)
        }
        
        # Calculate T (trend) and V (variance) from history if available
        if E_mu_history and len(E_mu_history) >= 2:
            metrics["T"] = self._calculate_trend(E_mu_history)
            metrics["V"] = self._calculate_variance(E_mu_history)
        else:
            metrics["T"] = 0.0
            metrics["V"] = 0.0
        
        return metrics
    
    def _calculate_trend(self, history: List[float]) -> float:
        """
        Calculate trend (T) from Eμ history.
        
        Simple linear trend: (last - first) / length
        """
        if len(history) < 2:
            return 0.0
        
        return (history[-1] - history[0]) / len(history)
    
    def _calculate_variance(self, history: List[float]) -> float:
        """
        Calculate variance (V) from Eμ history.
        
        Simple variance calculation.
        """
        if len(history) < 2:
            return 0.0
        
        mean = sum(history) / len(history)
        variance = sum((x - mean) ** 2 for x in history) / len(history)
        
        return variance
    
    def _determine_reason(
        self,
        verdict: str,
        eps: EnergeticState,
        metrics: Dict[str, float]
    ) -> str:
        """
        Determine reason for verdict.
        
        Args:
            verdict: Decision verdict
            eps: Energetic state
            metrics: Metrics dictionary
        
        Returns:
            Reason string
        """
        policy = self.decision_gate.policy
        config = policy.get_params()
        
        H_threshold = config.get("H_threshold", 0.85)
        D_threshold = config.get("D_traj_threshold", 0.7)
        E_mu_restrict_max = config.get("E_mu_restrict_max", 15.0)
        
        if verdict == "BLOCK":
            # Determine block reason
            if eps.S == 0.0:
                return "Safety rule failed (S == 0)"
            elif eps.E_mu < E_mu_restrict_max:
                return f"Eμ in restrict range (Eμ={eps.E_mu:.3f} < {E_mu_restrict_max})"
            else:
                return "GateCore blocked (unknown reason)"
        
        elif verdict == "REVIEW":
            # Determine review reason
            if eps.H > H_threshold:
                return f"Entropy above threshold (H={eps.H:.3f} > {H_threshold})"
            elif metrics.get("D_traj", 0.0) > D_threshold:
                return f"Semantic drift above threshold (D={metrics['D_traj']:.3f} > {D_threshold})"
            elif metrics.get("V", 0.0) > config.get("V_max", 8.0):
                return f"Variance above threshold (V={metrics['V']:.3f})"
            elif metrics.get("T", 0.0) < 0.0 and self._is_E_mu_caution(eps.E_mu, config):
                return "Negative trend AND Eμ in caution range"
            else:
                return "GateCore review required"
        
        else:  # ALLOW
            return "All metrics within safety bounds"

    def _is_E_mu_caution(self, E_mu: float, config: Dict[str, Any]) -> bool:
        """Check if Eμ is in caution range."""
        E_mu_caution_min = config.get("E_mu_caution_min", 15.0)
        E_mu_caution_max = config.get("E_mu_caution_max", 30.0)
        
        return E_mu_caution_min <= E_mu < E_mu_caution_max

