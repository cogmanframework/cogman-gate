"""
Trajectory Builder

Purpose: Build trajectory and create Trace
Spec: docs/TRACE_LIFECYCLE_SPEC.md
"""

from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
import time
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Trace:
    """
    Trace structure (immutable)
    
    Spec: docs/TRACE_LIFECYCLE_SPEC.md
    """
    trace_id: str
    state: Literal[
        "CREATED",
        "ACTIVE",
        "BLOCKED",
        "COMPLETED",
        "INVALID",
        "ARCHIVED"
    ]
    created_at: float
    closed_at: Optional[float]
    
    origin: Dict[str, Any]
    context: Dict[str, Any]
    
    lifecycle_log: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "state": self.state,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "origin": self.origin,
            "context": self.context,
            "lifecycle_log": self.lifecycle_log
        }


@dataclass
class Trajectory:
    """
    Trajectory structure
    
    Contains state history and metadata.
    """
    states: List[Dict[str, Any]]
    trace_id: str
    source_modality: str
    timestamp: float
    debug_lineage: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Trajectory to dictionary."""
        return {
            "trace_id": self.trace_id,
            "states": self.states,
            "source_modality": self.source_modality,
            "timestamp": self.timestamp,
            "debug_lineage": self.debug_lineage
        }


class TrajectoryBuilder:
    """
    Trajectory Builder
    
    Purpose: Build trajectory from perception states and create Trace.
    
    Rules:
    - ONLY TrajectoryBuilder can create Trace
    - Trace creation is logged
    - Trace state transitions are locked
    """
    
    def __init__(self):
        """Initialize Trajectory Builder."""
        self.trajectory_id: Optional[str] = None
        self.states: List[Dict[str, Any]] = []
        self.origin: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}
    
    def create_trace(
        self,
        origin: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Trace:
        """
        Create Trace (ONLY TrajectoryBuilder can do this).
        
        Args:
            origin: Source information (source_id, modality, adapter)
            context: Context information (gate profile, runtime mode)
        
        Returns:
            Trace in CREATED state
        """
        trace_id = str(uuid.uuid4())
        created_at = time.time()
        
        # Create lifecycle log entry
        lifecycle_log = [{
            "event": "TRACE_CREATED",
            "trace_id": trace_id,
            "source": origin.get("source_id", "unknown"),
            "modality": origin.get("modality", "text"),
            "timestamp": created_at
        }]
        
        trace = Trace(
            trace_id=trace_id,
            state="CREATED",
            created_at=created_at,
            closed_at=None,
            origin=origin,
            context=context,
            lifecycle_log=lifecycle_log
        )
        
        logger.info(f"Trace created: {trace_id}")
        
        return trace
    
    def append_state(self, state: Dict[str, Any]):
        """
        Append state to trajectory.
        
        Args:
            state: State dictionary (EPS-8 or other)
        """
        self.states.append(state)
    
    def build_trajectory(
        self,
        trace: Trace,
        source_modality: str = "text"
    ) -> Trajectory:
        """
        Build trajectory from states.
        
        Args:
            trace: Trace object
            source_modality: Source modality
        
        Returns:
            Trajectory object
        """
        trajectory = Trajectory(
            states=self.states.copy(),
            trace_id=trace.trace_id,
            source_modality=source_modality,
            timestamp=trace.created_at,
            debug_lineage={
                "origin": trace.origin,
                "context": trace.context
            }
        )
        
        return trajectory
    
    def build(self) -> Dict[str, Any]:
        """
        Build trajectory dictionary (legacy method).
        
        Returns:
            Trajectory dictionary
        """
        if self.trajectory_id is None:
            self.trajectory_id = str(uuid.uuid4())
        
        return {
            "trace_id": self.trajectory_id,
            "states": self.states,
            "metadata": {
                "state_count": len(self.states),
            },
        }
    
    def reset(self):
        """Reset Trajectory Builder state."""
        self.trajectory_id = None
        self.states = []
        self.origin = {}
        self.context = {}


class TraceManager:
    """
    Trace Manager
    
    Purpose: Manage Trace lifecycle and state transitions.
    
    Rules:
    - Trace state transitions are locked
    - Trace lifecycle log is append-only
    - Trace closure is irreversible
    """
    
    @staticmethod
    def transition_trace(
        trace: Trace,
        new_state: Literal[
            "ACTIVE",
            "BLOCKED",
            "COMPLETED",
            "INVALID",
            "ARCHIVED"
        ],
        reason: str = "",
        event_data: Optional[Dict[str, Any]] = None
    ) -> Trace:
        """
        Transition trace to new state.
        
        Args:
            trace: Current Trace
            new_state: New state
            reason: Transition reason
            event_data: Additional event data
        
        Returns:
            New Trace with updated state
        """
        # Validate state transition
        allowed_transitions = {
            "CREATED": ["ACTIVE", "BLOCKED"],
            "ACTIVE": ["BLOCKED", "COMPLETED"],
            "BLOCKED": ["INVALID"],
            "COMPLETED": ["ARCHIVED"]
        }
        
        if trace.state not in allowed_transitions:
            raise ValueError(f"Cannot transition from state: {trace.state}")
        
        if new_state not in allowed_transitions.get(trace.state, []):
            raise ValueError(
                f"Invalid transition: {trace.state} → {new_state}"
            )
        
        # Create new lifecycle log entry
        new_log_entry = {
            "event": f"TRACE_{new_state}",
            "trace_id": trace.trace_id,
            "timestamp": time.time(),
            "reason": reason
        }
        
        if event_data:
            new_log_entry.update(event_data)
        
        # Append to lifecycle log (immutable operation)
        new_lifecycle_log = trace.lifecycle_log + [new_log_entry]
        
        # Determine closed_at
        closed_at = trace.closed_at
        if new_state in ["BLOCKED", "COMPLETED", "INVALID"]:
            closed_at = time.time()
        
        # Create new Trace (immutable)
        new_trace = Trace(
            trace_id=trace.trace_id,
            state=new_state,
            created_at=trace.created_at,
            closed_at=closed_at,
            origin=trace.origin,
            context=trace.context,
            lifecycle_log=new_lifecycle_log
        )
        
        logger.info(f"Trace {trace.trace_id} transitioned: {trace.state} → {new_state}")
        
        return new_trace
    
    @staticmethod
    def close_trace(
        trace: Trace,
        reason: str
    ) -> Trace:
        """
        Close trace with reason.
        
        Args:
            trace: Trace to close
            reason: Closure reason (COMPLETED, BLOCKED, INVALID)
        
        Returns:
            New Trace with closed state
        """
        if trace.state not in ["ACTIVE", "CREATED"]:
            raise ValueError(f"Cannot close trace in state: {trace.state}")
        
        # Determine new state based on reason
        state_map = {
            "COMPLETED": "COMPLETED",
            "BLOCKED": "BLOCKED",
            "INVALID": "INVALID"
        }
        
        new_state = state_map.get(reason, "COMPLETED")
        
        return TraceManager.transition_trace(trace, new_state, reason)
