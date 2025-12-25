"""
Fail-Closed Safety Tests

Purpose: Test fail-closed behavior and safety constraints
"""

import unittest
import sys
from pathlib import Path
import math

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from gate import GateCore, DecisionGate, GatePolicy, GateTrace, EnergeticState
from runtime import RuntimeLoop


class TestFailClosed(unittest.TestCase):
    """Test fail-closed behavior"""
    
    def setUp(self):
        """Set up test fixtures."""
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
        self.gatecore = GateCore(decision_gate=decision_gate)
    
    def test_safety_rule_failure_blocks(self):
        """Test that safety rule failure always blocks."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.0, H=0.3,  # S == 0 → must BLOCK
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_safety_fail")
        
        self.assertEqual(result.verdict, "BLOCK")
        self.assertIn("Safety rule failed", result.reason)
    
    def test_high_entropy_reviews(self):
        """Test that high entropy triggers REVIEW."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.9,  # H > 0.85 → REVIEW
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_high_entropy")
        
        self.assertEqual(result.verdict, "REVIEW")
        self.assertIn("entropy", result.reason.lower())
    
    def test_low_entropy_allows(self):
        """Test that low entropy allows."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.3,  # H < 0.85 → ALLOW
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_low_entropy")
        
        self.assertEqual(result.verdict, "ALLOW")


class TestBoundaryConditions(unittest.TestCase):
    """Test boundary conditions"""
    
    def setUp(self):
        """Set up test fixtures."""
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
        self.gatecore = GateCore(decision_gate=decision_gate)
    
    def test_boundary_entropy_threshold(self):
        """Test boundary entropy threshold."""
        # Test exactly at threshold
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.85,  # Exactly at threshold
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_boundary")
        
        # Should be ALLOW (H == 0.85, not > 0.85)
        self.assertEqual(result.verdict, "ALLOW")
    
    def test_minimum_values(self):
        """Test with minimum values."""
        eps = EnergeticState(
            I=0.0, P=-1.0, S=0.0, H=0.0,
            A=0.0, S_a=0.0, E_mu=0.0, theta=0.0
        )
        
        result = self.gatecore.admit(eps, trace_id="test_minimum")
        
        # Should handle gracefully
        self.assertIsNotNone(result)
    
    def test_maximum_values(self):
        """Test with maximum values."""
        eps = EnergeticState(
            I=1.0, P=1.0, S=1.0, H=1.0,
            A=1.0, S_a=1.0, E_mu=100.0, theta=2.0
        )
        
        result = self.gatecore.admit(eps, trace_id="test_maximum")
        
        # Should handle gracefully
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()

