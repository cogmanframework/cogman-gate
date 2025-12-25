"""
Basic Bridge Test (No YAML required)

Tests basic kernel bridge functionality without requiring YAML
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bridge import KernelBridge

def test_bridge_loading():
    """Test that bridge can be loaded"""
    print("=== Testing Bridge Loading ===")
    try:
        bridge = KernelBridge()
        print("✓ Bridge loaded successfully")
        return bridge
    except Exception as e:
        print(f"✗ Failed to load bridge: {e}")
        return None

def test_energy_projection(bridge):
    """Test energy projection"""
    print("\n=== Testing Energy Projection ===")
    try:
        eps8_state = {
            'I': 0.8,
            'P': 0.6,
            'S': 0.7,
            'H': 0.3,
            'F': 0.0,
            'A': 0.5,
            'S_a': 0.6,
            'theta': 1.5,
        }
        
        neural_components = {
            'dopamine': 0.4,
            'serotonin': 0.5,
            'oxytocin': 0.3,
            'adrenaline': 0.2,
            'cortisol': 0.1,
        }
        
        decision_params = {
            'rule_fail': False,
            'H_threshold': 0.85,
            'D_traj_threshold': 0.7,
        }
        
        energy = bridge.energy_projection(
            eps8_state,
            neural_components,
            theta_phase=1.5,
            E_pred=0.5,
            decision_params=decision_params,
        )
        
        print(f"✓ Energy projection successful")
        print(f"  ΔEΨ = {energy['delta_E_psi']:.3f}")
        print(f"  E_reflex = {energy['E_reflex']:.3f}")
        print(f"  E_mind = {energy['E_mind']:.3f}")
        print(f"  Verdict: {energy['verdict']}")
        return True
    except Exception as e:
        print(f"✗ Energy projection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validate_state(bridge):
    """Test state validation"""
    print("\n=== Testing State Validation ===")
    try:
        valid_state = {
            'I': 0.8,
            'P': 0.6,
            'S': 0.7,
            'H': 0.3,
            'A': 0.5,
            'S_a': 0.6,
            'theta': 1.5,
        }
        
        is_valid = bridge.validate_state(valid_state)
        print(f"✓ State validation: {is_valid}")
        return True
    except Exception as e:
        print(f"✗ State validation failed: {e}")
        return False

def test_decision_gate(bridge):
    """Test basic decision gate"""
    print("\n=== Testing Decision Gate ===")
    try:
        decision_params = {
            'rule_fail': False,
            'H_threshold': 0.85,
            'D_traj_threshold': 0.7,
        }
        
        verdict = bridge.decision_gate(decision_params, H_current=0.5)
        print(f"✓ Decision gate: H=0.5 → {verdict}")
        return True
    except Exception as e:
        print(f"✗ Decision gate failed: {e}")
        return False

if __name__ == "__main__":
    print("Cogman Kernel Bridge - Basic Test\n")
    
    bridge = test_bridge_loading()
    if not bridge:
        print("\n✗ Cannot proceed without bridge")
        sys.exit(1)
    
    results = []
    results.append(test_energy_projection(bridge))
    results.append(test_validate_state(bridge))
    results.append(test_decision_gate(bridge))
    
    print("\n=== Test Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

