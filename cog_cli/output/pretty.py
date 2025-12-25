"""
Pretty Output Formatter

Formatting only - no logic
"""

from typing import Dict, Any


def print_energy_result(result: Dict[str, Any]) -> None:
    """Print energy computation result in pretty format."""
    if 'formula' in result:
        print(f"\n{'='*50}")
        print(f"Formula: {result['formula']}")
        print(f"{'='*50}")
        print(f"Result: {result.get('result', 'N/A')}")
        if 'inputs' in result:
            print("\nInputs:")
            for k, v in result['inputs'].items():
                print(f"  {k:10s} = {v}")
    else:
        print("\nEnergy Result:")
        for k, v in result.items():
            print(f"  {k:20s} = {v}")


def print_energy_projection(result: Dict[str, Any]) -> None:
    """Print energy projection result in pretty format."""
    print(f"\n{'='*50}")
    print("Energy Projection")
    print(f"{'='*50}")
    print(f"ΔEΨ          = {result.get('delta_E_psi', 'N/A'):.6f}")
    print(f"E_reflex     = {result.get('E_reflex', 'N/A'):.6f}")
    print(f"ΔEΨ_theta    = {result.get('delta_E_psi_theta', 'N/A'):.6f}")
    print(f"E_mind       = {result.get('E_mind', 'N/A'):.6f}")
    print(f"E_coherence  = {result.get('E_coherence', 'N/A'):.6f}")
    print(f"E_neural     = {result.get('E_neural', 'N/A'):.6f}")
    print(f"E_bind       = {result.get('E_bind', 'N/A'):.6f}")
    print(f"E_mem        = {result.get('E_mem', 'N/A'):.6f}")
    print(f"Verdict      = {result.get('verdict', 'N/A')}")


def print_decision_result(result: Dict[str, Any]) -> None:
    """Print decision result in pretty format."""
    print(f"\n{'='*50}")
    print("Decision Result")
    print(f"{'='*50}")
    print(f"Verdict      = {result.get('verdict', 'N/A')}")
    print(f"Protocol     = {result.get('protocol', 'N/A')}")
    print(f"Context      = {result.get('context', 'N/A')}")
    print(f"Rule Fail    = {result.get('rule_fail', False)}")
    
    if 'metrics' in result:
        print("\nMetrics:")
        metrics = result['metrics']
        print(f"  Eμ         = {metrics.get('E_mu', 'N/A'):.3f}")
        print(f"  H          = {metrics.get('H', 'N/A'):.3f}")
        print(f"  D          = {metrics.get('D', 'N/A'):.3f}")
        print(f"  S          = {metrics.get('S', 'N/A'):.3f}")
        print(f"  T          = {metrics.get('T', 'N/A'):.3f}")
        print(f"  V          = {metrics.get('V', 'N/A'):.3f}")
    
    if 'reasons' in result and result['reasons']:
        print("\nReasons:")
        for reason in result['reasons']:
            print(f"  - {reason}")


def print_memory(result: Dict[str, Any]) -> None:
    """Print memory data in pretty format."""
    print(f"\n{'='*50}")
    print("Memory Data")
    print(f"{'='*50}")
    if isinstance(result, dict):
        for k, v in result.items():
            print(f"{k:20s} = {v}")
    else:
        print(result)


def print_memory_fields(fields: list) -> None:
    """Print memory fields list in pretty format."""
    print(f"\n{'='*50}")
    print("Memory Fields")
    print(f"{'='*50}")
    for i, field in enumerate(fields, 1):
        print(f"  {i}. {field}")


def print_memory_stats(stats: Dict[str, Any]) -> None:
    """Print memory statistics in pretty format."""
    print(f"\n{'='*50}")
    print("Memory Statistics")
    print(f"{'='*50}")
    if isinstance(stats, dict) and 'stats' in stats:
        for k, v in stats['stats'].items():
            print(f"{k:20s} = {v}")
    else:
        for k, v in stats.items():
            print(f"{k:20s} = {v}")

