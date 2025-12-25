"""
Example: Gate Integration with Runtime Loop

Purpose: Demonstrate GateCore integration with Runtime Loop PHASE 4
"""

import logging
from gate import GateCore, DecisionGate, GatePolicy, GateTrace
from bridge import KernelBridge
from runtime import RuntimeLoop
from perception import TrajectoryBuilder

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_gatecore():
    """Create GateCore instance."""
    # Create kernel bridge
    try:
        kernel_bridge = KernelBridge()
    except Exception as e:
        logger.warning(f"Kernel bridge not available: {e}")
        kernel_bridge = None
    
    # Create gate policy
    gate_policy = GatePolicy(config={
        "H_threshold": 0.85,
        "D_traj_threshold": 0.7,
        "E_mu_restrict_min": -100.0,
        "E_mu_restrict_max": 100.0,
        "S_min": 0.5,
    })
    
    # Create decision gate
    if kernel_bridge:
        decision_gate = DecisionGate(kernel_bridge, gate_policy)
    else:
        # Fallback: create dummy decision gate
        class DummyDecisionGate:
            def __init__(self, policy):
                self.policy = policy
            
            def decide(self, state):
                # Simple decision logic
                H = state.get('H', 0.0)
                S = state.get('S', 1.0)
                
                if S == 0.0:
                    return "BLOCK"
                elif H > 0.85:
                    return "REVIEW"
                else:
                    return "ALLOW"
        
        decision_gate = DummyDecisionGate(gate_policy)
    
    # Create gate trace
    gate_trace = GateTrace()
    
    # Create GateCore
    gatecore = GateCore(
        decision_gate=decision_gate,
        gate_trace=gate_trace,
        context="default"
    )
    
    return gatecore


def example_runtime_loop_with_gate():
    """Example: Runtime Loop with GateCore integration."""
    logger.info("=== Example: Runtime Loop with GateCore ===")
    
    # Create components
    gatecore = create_gatecore()
    trajectory_builder = TrajectoryBuilder()
    
    # Create Runtime Loop
    runtime_loop = RuntimeLoop(
        gatecore=gatecore,
        trajectory_builder=trajectory_builder
    )
    
    # Note: In real usage, you would call runtime_loop.run()
    # For this example, we'll just demonstrate the setup
    
    logger.info("Runtime Loop created with GateCore integration")
    logger.info(f"GateCore context: {gatecore.context}")
    logger.info("Ready to process trajectories through PHASE 4")


def example_gatecore_admission():
    """Example: Direct GateCore admission check."""
    logger.info("=== Example: GateCore Admission Check ===")
    
    # Create GateCore
    gatecore = create_gatecore()
    
    # Create test EnergeticState
    from gate import EnergeticState
    eps = EnergeticState(
        I=0.7,
        P=0.6,
        S=0.8,
        H=0.3,  # Low entropy (should ALLOW)
        A=0.5,
        S_a=0.4,
        E_mu=50.0,
        theta=1.2
    )
    
    # Call admission
    result = gatecore.admit(eps, trace_id="test_trace_001")
    
    logger.info(f"GateCore verdict: {result.verdict}")
    logger.info(f"Reason: {result.reason}")
    logger.info(f"Metrics: {result.metrics}")
    
    # Test with high entropy (should REVIEW or BLOCK)
    eps_high_H = EnergeticState(
        I=0.9,
        P=0.5,
        S=0.3,  # Low stability
        H=0.9,  # High entropy (should REVIEW)
        A=0.5,
        S_a=0.4,
        E_mu=50.0,
        theta=1.2
    )
    
    result2 = gatecore.admit(eps_high_H, trace_id="test_trace_002")
    logger.info(f"\nHigh entropy test:")
    logger.info(f"GateCore verdict: {result2.verdict}")
    logger.info(f"Reason: {result2.reason}")


if __name__ == "__main__":
    example_gatecore_admission()
    print()
    example_runtime_loop_with_gate()

