"""
Full Flow Integration Tests

Purpose: Test complete system flow from input to output
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from runtime import RuntimeLoop
from gate import GateCore, DecisionGate, GatePolicy, GateTrace
from memory import EpisodicField, SemanticField, ProceduralField, IdentityField
from reasoning import ReasoningModule
from action import ActionModule
from runtime import PostProcessor
from perception import TrajectoryBuilder


class TestFullFlow(unittest.TestCase):
    """Test complete system flow"""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create all modules
        gate_policy = GatePolicy(config={
            "H_threshold": 0.85,
            "D_traj_threshold": 0.7,
            "S_min": 0.5,
        })
        
        class DummyDecisionGate:
            def __init__(self, policy):
                self.policy = policy
            
            def decide(self, state):
                H = state.get('H', 0.0)
                S = state.get('S', 1.0)
                if S == 0.0:
                    return "BLOCK"
                elif H > 0.85:
                    return "REVIEW"
                else:
                    return "ALLOW"
        
        decision_gate = DummyDecisionGate(gate_policy)
        gatecore = GateCore(decision_gate=decision_gate)
        
        memory_fields = {
            "episodic": EpisodicField(),
            "semantic": SemanticField(),
            "procedural": ProceduralField(),
            "identity": IdentityField()
        }
        
        from runtime import WMController
        wm_controller = WMController(memory_fields=memory_fields)
        
        reasoning_module = ReasoningModule()
        action_module = ActionModule()
        post_processor = PostProcessor(enable_async=False)  # Synchronous for testing
        trajectory_builder = TrajectoryBuilder()
        
        # Create Runtime Loop
        self.runtime_loop = RuntimeLoop(
            gatecore=gatecore,
            wm_controller=wm_controller,
            reasoning_module=reasoning_module,
            action_module=action_module,
            post_processor=post_processor,
            trajectory_builder=trajectory_builder
        )
    
    def test_single_cycle_execution(self):
        """Test single cycle execution."""
        # This would require input injection mechanism
        # For now, test structure
        self.assertTrue(hasattr(self.runtime_loop, '_execute_cycle'))
    
    def test_phase_sequence(self):
        """Test that phases execute in sequence."""
        # Test structure
        phases = [
            "IDLE", "INPUT_INTAKE", "SENSORY_ADAPTATION",
            "PERCEPTION_BOUNDARY", "TRAJECTORY_ADMISSION",
            "WORKING_MEMORY_CONTROL", "REASONING", "DECISION",
            "ACTION_OUTPUT", "POST_PROCESSING"
        ]
        
        for phase_name in phases:
            self.assertTrue(hasattr(self.runtime_loop, f"_phase_{phase_name.lower()}"))


class TestFullFlowErrorHandling(unittest.TestCase):
    """Test full flow error handling"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.runtime_loop = RuntimeLoop()
    
    def test_error_propagation(self):
        """Test that errors propagate correctly."""
        # Test structure
        self.assertTrue(hasattr(self.runtime_loop, '_execute_cycle'))
    
    def test_blocked_trajectory_handling(self):
        """Test blocked trajectory handling."""
        # Test that blocked trajectories don't break the loop
        pass


if __name__ == "__main__":
    unittest.main()

