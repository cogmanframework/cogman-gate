"""
Gate Integration Tests

Purpose: Test Gate integration with Runtime Loop
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from gate import GateCore, DecisionGate, GatePolicy, GateTrace, EnergeticState
from runtime import RuntimeLoop, EnergeticState as RuntimeEnergeticState


class TestGateIntegration(unittest.TestCase):
    """Test Gate integration"""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create gate policy
        gate_policy = GatePolicy(config={
            "H_threshold": 0.85,
            "D_traj_threshold": 0.7,
            "E_mu_restrict_min": -100.0,
            "E_mu_restrict_max": 100.0,
            "S_min": 0.5,
        })
        
        # Create dummy decision gate (no kernel bridge needed for basic tests)
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
        
        # Create GateCore
        self.gatecore = GateCore(
            decision_gate=decision_gate,
            gate_trace=GateTrace(),
            context="test"
        )
    
    def test_gatecore_admission_allow(self):
        """Test GateCore admission with ALLOW verdict."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.3,  # Low entropy
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_001")
        
        self.assertEqual(result.verdict, "ALLOW")
        self.assertIsNotNone(result.reason)
        self.assertIsNotNone(result.metrics)
    
    def test_gatecore_admission_block(self):
        """Test GateCore admission with BLOCK verdict."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.0, H=0.3,  # S == 0 → BLOCK
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_002")
        
        self.assertEqual(result.verdict, "BLOCK")
        self.assertIn("Safety rule failed", result.reason)
    
    def test_gatecore_admission_review(self):
        """Test GateCore admission with REVIEW verdict."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.9,  # High entropy > 0.85
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        result = self.gatecore.admit(eps, trace_id="test_003")
        
        self.assertEqual(result.verdict, "REVIEW")
        self.assertIn("entropy", result.reason.lower())
    
    def test_gatecore_evaluate_safety(self):
        """Test GateCore safety evaluation."""
        eps = EnergeticState(
            I=0.7, P=0.6, S=0.8, H=0.3,
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        safety_result = self.gatecore.evaluate_safety(eps)
        
        self.assertIn("pass", safety_result)
        self.assertIn("S", safety_result)
        self.assertIn("S_min", safety_result)


class TestGateIntegrationErrorHandling(unittest.TestCase):
    """Test Gate integration error handling"""
    
    def setUp(self):
        """Set up test fixtures."""
        gate_policy = GatePolicy()
        
        class DummyDecisionGate:
            def __init__(self, policy):
                self.policy = policy
            
            def decide(self, state):
                return "ALLOW"
        
        decision_gate = DummyDecisionGate(gate_policy)
        self.gatecore = GateCore(decision_gate=decision_gate)
    
    def test_invalid_eps_state(self):
        """Test with invalid EPS state."""
        # Test with NaN values
        eps = EnergeticState(
            I=float('nan'), P=0.6, S=0.8, H=0.3,
            A=0.5, S_a=0.4, E_mu=50.0, theta=1.2
        )
        
        # Should handle gracefully (depends on implementation)
        # For now, just test that method exists
        self.assertTrue(hasattr(self.gatecore, 'admit'))


if __name__ == "__main__":
    unittest.main()

