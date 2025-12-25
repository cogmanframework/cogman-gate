"""
Reasoning Module

Purpose: Structural reasoning (NO FORMULA, NO DECISION)
Spec: docs/REASONING_MODULE_SPEC.md
"""

from typing import Dict, Any, List, Optional, Literal
from dataclasses import dataclass, field
import time
import logging

from .causal_graph import CausalGraph
from .planner import Planner
from .simulator import Simulator

logger = logging.getLogger(__name__)


@dataclass
class ReasoningInput:
    """
    Reasoning Input Structure
    
    Spec: docs/REASONING_MODULE_SPEC.md
    """
    trajectory: Dict[str, Any]  # From WM Controller only
    wm_decision_hint: Optional[str] = None  # Informational only
    context: Dict[str, Any] = field(default_factory=dict)  # Informational only
    trace_id: str = ""


@dataclass
class ReasoningOutput:
    """
    Reasoning Output Structure
    
    Spec: docs/REASONING_MODULE_SPEC.md
    
    Rules:
    - Structure only (graph, plan, tree, simulation)
    - NO verdict, NO score, NO preference
    """
    structure_type: Literal[
        "graph",
        "plan",
        "tree",
        "simulation"
    ]
    structure: Any  # Graph/Plan/Tree structure
    assumptions: List[str] = field(default_factory=list)  # Structural assumptions
    constraints: List[str] = field(default_factory=list)  # Structural constraints
    meta: Dict[str, Any] = field(default_factory=dict)  # Non-semantic metadata
    trace_id: str = ""
    timestamp: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert output to dictionary."""
        return {
            "structure_type": self.structure_type,
            "structure": self.structure,
            "assumptions": self.assumptions,
            "constraints": self.constraints,
            "meta": self.meta,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp
        }


class ReasoningModule:
    """
    Reasoning Module
    
    Purpose: Structural reasoning only
    - Create structure (graph/tree/plan)
    - Link causal relations
    - Simulate paths (non-evaluative)
    - Output structural alternatives (no preference)
    
    Rules:
    - NO decision making
    - NO evaluation
    - NO scoring
    - NO optimization
    """
    
    def __init__(
        self,
        causal_graph: Optional[CausalGraph] = None,
        planner: Optional[Planner] = None,
        simulator: Optional[Simulator] = None
    ):
        """
        Initialize Reasoning Module.
        
        Args:
            causal_graph: CausalGraph instance (optional)
            planner: Planner instance (optional)
            simulator: Simulator instance (optional)
        """
        self.causal_graph = causal_graph or CausalGraph()
        self.planner = planner or Planner()
        self.simulator = simulator or Simulator()
    
    def process(self, input_data: ReasoningInput) -> ReasoningOutput:
        """
        Process trajectory through Reasoning Module.
        
        This is the PHASE 6 operation in Runtime Loop.
        
        Args:
            input_data: ReasoningInput from WM Controller
        
        Returns:
            ReasoningOutput with structure
        """
        trajectory = input_data.trajectory
        trace_id = input_data.trace_id
        
        # Determine reasoning type based on trajectory and hint
        reasoning_type = self._determine_reasoning_type(input_data)
        
        # Create structure based on type
        if reasoning_type == "graph":
            structure = self._create_causal_graph(trajectory)
            structure_type = "graph"
        elif reasoning_type == "plan":
            structure = self._create_plan(trajectory, input_data)
            structure_type = "plan"
        elif reasoning_type == "simulation":
            structure = self._create_simulation(trajectory, input_data)
            structure_type = "simulation"
        else:
            # Default: tree structure
            structure = self._create_tree(trajectory)
            structure_type = "tree"
        
        # Extract assumptions and constraints
        assumptions = self._extract_assumptions(trajectory, structure)
        constraints = self._extract_constraints(trajectory, structure)
        
        # Create output
        output = ReasoningOutput(
            structure_type=structure_type,
            structure=structure,
            assumptions=assumptions,
            constraints=constraints,
            meta={
                "reasoning_type": reasoning_type,
                "wm_hint": input_data.wm_decision_hint,
                "trajectory_length": len(trajectory.get("states", []))
            },
            trace_id=trace_id,
            timestamp=time.time()
        )
        
        logger.info(
            f"Reasoning Module processed: {structure_type} "
            f"(trace_id={trace_id}, assumptions={len(assumptions)}, constraints={len(constraints)})"
        )
        
        return output
    
    def _determine_reasoning_type(self, input_data: ReasoningInput) -> str:
        """
        Determine reasoning type based on input.
        
        Rules:
        - Based on WM decision hint (informational only)
        - Based on trajectory structure
        - NO evaluation, NO decision
        """
        wm_hint = input_data.wm_decision_hint
        
        # Use hint to determine type (informational only)
        if wm_hint == "CREATE_NEW_SN":
            return "graph"  # Create new causal graph
        elif wm_hint == "EXTEND_PATH":
            return "plan"  # Create plan to extend
        elif wm_hint == "RECALL_SN":
            return "simulation"  # Simulate recalled pattern
        elif wm_hint == "TRIGGER_ACTION":
            return "plan"  # Create action plan
        else:
            return "tree"  # Default: tree structure
    
    def _create_causal_graph(self, trajectory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create causal graph structure.
        
        Rules:
        - Link causal relations only
        - NO evaluation
        - NO scoring
        """
        states = trajectory.get("states", [])
        
        # Build causal graph from trajectory states
        for i, state in enumerate(states):
            node_id = f"state_{i}"
            self.causal_graph.add_node({
                "id": node_id,
                "state": state,
                "index": i
            })
            
            # Add causal edge to next state
            if i < len(states) - 1:
                next_node_id = f"state_{i+1}"
                self.causal_graph.add_edge(node_id, next_node_id, "causes")
        
        return self.causal_graph.build()
    
    def _create_plan(self, trajectory: Dict[str, Any], input_data: ReasoningInput) -> List[Dict[str, Any]]:
        """
        Create plan structure.
        
        Rules:
        - Structural plan only
        - NO evaluation
        - NO optimization
        """
        states = trajectory.get("states", [])
        current_state = states[-1] if states else {}
        
        # Create plan from current state (structural only)
        plan = self.planner.plan(
            goal={"type": "structural", "state": current_state},
            state=current_state
        )
        
        return plan
    
    def _create_simulation(self, trajectory: Dict[str, Any], input_data: ReasoningInput) -> Dict[str, Any]:
        """
        Create simulation structure.
        
        Rules:
        - Non-evaluative simulation
        - NO scoring
        - NO optimization
        """
        states = trajectory.get("states", [])
        current_state = states[-1] if states else {}
        
        # Create simulation (structural only)
        simulation = self.simulator.simulate({
            "scenario": "structural",
            "initial_state": current_state,
            "trajectory": trajectory
        })
        
        return simulation
    
    def _create_tree(self, trajectory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create tree structure.
        
        Rules:
        - Hierarchical structure only
        - NO evaluation
        """
        states = trajectory.get("states", [])
        
        # Build tree from trajectory
        tree = {
            "root": {
                "state": states[0] if states else {},
                "index": 0
            },
            "children": []
        }
        
        # Add children (simplified)
        for i, state in enumerate(states[1:], start=1):
            tree["children"].append({
                "state": state,
                "index": i
            })
        
        return tree
    
    def _extract_assumptions(self, trajectory: Dict[str, Any], structure: Any) -> List[str]:
        """
        Extract structural assumptions.
        
        Rules:
        - Structural preconditions only
        - NO semantic interpretation
        """
        assumptions = []
        
        # Extract assumptions from trajectory
        states = trajectory.get("states", [])
        if states:
            assumptions.append(f"Trajectory has {len(states)} states")
            assumptions.append("States are ordered sequentially")
        
        # Extract assumptions from structure
        if isinstance(structure, dict):
            if "nodes" in structure:
                assumptions.append(f"Graph has {len(structure['nodes'])} nodes")
            if "edges" in structure:
                assumptions.append(f"Graph has {len(structure['edges'])} edges")
        
        return assumptions
    
    def _extract_constraints(self, trajectory: Dict[str, Any], structure: Any) -> List[str]:
        """
        Extract structural constraints.
        
        Rules:
        - Structural requirements only
        - NO semantic interpretation
        """
        constraints = []
        
        # Extract constraints from trajectory
        states = trajectory.get("states", [])
        if states:
            constraints.append("States must be in chronological order")
            constraints.append("Each state must have valid EPS-8 parameters")
        
        # Extract constraints from structure
        if isinstance(structure, dict):
            if "edges" in structure:
                constraints.append("Edges must connect existing nodes")
        
        return constraints

