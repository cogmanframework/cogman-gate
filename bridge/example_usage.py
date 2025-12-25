"""
Bridge Usage Example

Demonstrates how to use the kernel bridge from Python
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bridge import KernelBridge
from bridge.data_marshalling import marshal_eps8, create_decision_bands_from_policy
from config.gate_policy_loader import GatePolicyLoader


def example_energy_projection():
    """Example: Energy projection"""
    print("=== Energy Projection Example ===")
    
    # Initialize bridge
    bridge = KernelBridge()  # Auto-loads library
    
    # Create EPS-8 state
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
    
    # Neural components
    neural_components = {
        'dopamine': 0.4,
        'serotonin': 0.5,
        'oxytocin': 0.3,
        'adrenaline': 0.2,
        'cortisol': 0.1,
    }
    
    # Decision parameters
    decision_params = {
        'rule_fail': False,
        'H_threshold': 0.85,
        'D_traj_threshold': 0.7,
    }
    
    # Call kernel
    energy = bridge.energy_projection(
        eps8_state,
        neural_components,
        theta_phase=1.5,
        E_pred=0.5,
        decision_params=decision_params,
    )
    
    print(f"ΔEΨ = {energy['delta_E_psi']:.3f}")
    print(f"E_reflex = {energy['E_reflex']:.3f}")
    print(f"E_mind = {energy['E_mind']:.3f}")
    print(f"Verdict: {energy['verdict']}")


def example_core9_gate():
    """Example: CORE-9 Decision Gate"""
    print("\n=== CORE-9 Decision Gate Example ===")
    
    # Load policy
    policy = GatePolicyLoader.load_from_file("config/gate_profiles.yaml")
    if not policy:
        print("Failed to load policy, using defaults")
        return
    
    # Get robot_control profile
    profile = policy.get_context("robot_control")
    if not profile:
        print("Context not found")
        return
    
    # Create bands from policy
    bands = create_decision_bands_from_policy(profile)
    
    # Initialize bridge
    bridge = KernelBridge()
    
    # Create metrics
    metrics = {
        'E_mu': 50.0,
        'H': 0.5,
        'D': 0.25,
        'S': 1.0,
        'T': 0.5,
        'V': 4.0,
    }
    
    # Eμ history for trend/variance
    E_mu_history = [45.0, 48.0, 50.0, 52.0]
    
    # Call CORE-9 gate
    result = bridge.core9_evaluate(
        metrics=metrics,
        bands=bands,
        context="robot_control",
        E_mu_history=E_mu_history,
    )
    
    print(f"Verdict: {result['verdict']}")
    print(f"Protocol: {result['protocol']}")
    print(f"Context: {result['context']}")
    print(f"Reasons:")
    for reason in result['reasons']:
        print(f"  - {reason}")
    print(f"\nMetrics:")
    for key, value in result['metrics'].items():
        print(f"  {key}: {value:.3f}")


def example_decision_gate():
    """Example: Basic decision gate"""
    print("\n=== Decision Gate Example ===")
    
    bridge = KernelBridge()
    
    decision_params = {
        'rule_fail': False,
        'H_threshold': 0.85,
        'D_traj_threshold': 0.7,
    }
    
    # Test different entropy values
    for H in [0.3, 0.7, 0.9]:
        verdict = bridge.decision_gate(decision_params, H_current=H)
        print(f"H = {H:.2f} → Verdict: {verdict}")


def example_validate_state():
    """Example: State validation"""
    print("\n=== State Validation Example ===")
    
    bridge = KernelBridge()
    
    # Valid state
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
    print(f"Valid state: {is_valid}")
    
    # Invalid state (H > 1)
    invalid_state = valid_state.copy()
    invalid_state['H'] = 1.5
    
    is_valid = bridge.validate_state(invalid_state)
    print(f"Invalid state (H=1.5): {is_valid}")


if __name__ == "__main__":
    try:
        example_energy_projection()
        example_core9_gate()
        example_decision_gate()
        example_validate_state()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

