"""
WM Controller Tests

Purpose: Test WM Controller functionality
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from runtime import WMController, EPS8State, Trajectory
from memory import EpisodicField, SemanticField, ProceduralField, IdentityField


class TestWMController(unittest.TestCase):
    """Test WM Controller"""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create memory fields
        memory_fields = {
            "episodic": EpisodicField(),
            "semantic": SemanticField(),
            "procedural": ProceduralField(),
            "identity": IdentityField()
        }
        
        # Create WM Controller
        self.wm_controller = WMController(
            memory_fields=memory_fields,
            config={
                "H_max": 0.65,
                "S_min": 0.5
            }
        )
    
    def test_gate_control(self):
        """Test gate control."""
        # Test with low entropy (should pass)
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,  # Low entropy
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        gate_status = self.wm_controller._gate_control(state)
        self.assertTrue(gate_status["entropy"])
        self.assertTrue(gate_status["safety"])
        self.assertTrue(gate_status["budget"])
    
    def test_gate_control_high_entropy(self):
        """Test gate control with high entropy."""
        # Test with high entropy (should fail)
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.9,  # High entropy > H_max (0.65)
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        gate_status = self.wm_controller._gate_control(state)
        self.assertFalse(gate_status["entropy"])
    
    def test_memory_resonance(self):
        """Test memory resonance invocation."""
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        resonance_scores = self.wm_controller._invoke_memory_resonance(state)
        
        # Should have scores for all memory fields
        self.assertIn("episodic", resonance_scores)
        self.assertIn("semantic", resonance_scores)
        self.assertIn("procedural", resonance_scores)
        self.assertIn("identity", resonance_scores)
        
        # Scores should be in [0, 1]
        for score in resonance_scores.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
    
    def test_navigation_decision(self):
        """Test navigation decision."""
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        resonance_scores = {
            "episodic": 0.5,
            "semantic": 0.5,
            "procedural": 0.5,
            "identity": 0.5
        }
        
        modulated_eps8 = state  # No modulation for this test
        
        decision = self.wm_controller._navigation_decision(
            state, resonance_scores, modulated_eps8
        )
        
        # Should be one of the allowed decisions
        allowed_decisions = [
            "CREATE_NEW_SN",
            "EXTEND_PATH",
            "RECALL_SN",
            "TRIGGER_ACTION",
            "ACTIVATE_REFLEX",
            "BLOCKED"
        ]
        self.assertIn(decision, allowed_decisions)
    
    def test_navigation_decision_high_episodic_resonance(self):
        """Test navigation decision with high episodic resonance."""
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        resonance_scores = {
            "episodic": 0.8,  # > 0.7 → EXTEND_PATH
            "semantic": 0.5,
            "procedural": 0.5,
            "identity": 0.5
        }
        
        modulated_eps8 = state
        
        decision = self.wm_controller._navigation_decision(
            state, resonance_scores, modulated_eps8
        )
        
        self.assertEqual(decision, "EXTEND_PATH")
    
    def test_navigation_decision_high_semantic_resonance(self):
        """Test navigation decision with high semantic resonance."""
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        resonance_scores = {
            "episodic": 0.5,
            "semantic": 0.9,  # > 0.8 → RECALL_SN
            "procedural": 0.5,
            "identity": 0.5
        }
        
        modulated_eps8 = state
        
        decision = self.wm_controller._navigation_decision(
            state, resonance_scores, modulated_eps8
        )
        
        self.assertEqual(decision, "RECALL_SN")


class TestWMControllerErrorHandling(unittest.TestCase):
    """Test WM Controller error handling"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.wm_controller = WMController()
    
    def test_empty_memory_fields(self):
        """Test with empty memory fields."""
        state = EPS8State(
            I=0.7, P=0.6, S=0.8, H=0.3,
            F=0.0, A=0.5, S_a=0.4, theta=1.2
        )
        
        # Should not raise error
        resonance_scores = self.wm_controller._invoke_memory_resonance(state)
        self.assertEqual(resonance_scores, {})
    
    def test_invalid_state(self):
        """Test with invalid state."""
        # Test with None state (should handle gracefully)
        # Note: This depends on implementation
        pass


if __name__ == "__main__":
    unittest.main()

