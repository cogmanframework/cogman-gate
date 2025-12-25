"""
Table Output Formatter

Formatting only - no logic
"""

from typing import Dict, Any

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    # Fallback to simple formatting
    def tabulate(data, headers=None, tablefmt='grid'):
        """Simple tabulate fallback."""
        if headers:
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers))))
        for row in data:
            if isinstance(row, list):
                print(" | ".join(str(x) for x in row))
            else:
                print(row)


def print_energy_result(result: Dict[str, Any]) -> None:
    """Print energy computation result as table."""
    if not TABULATE_AVAILABLE:
        # Fallback to simple format
        if 'formula' in result:
            print(f"\nFormula: {result['formula']}")
            print(f"Result: {result.get('result', 'N/A')}")
            if 'inputs' in result:
                print("\nInputs:")
                for k, v in result['inputs'].items():
                    print(f"  {k:15s} = {v}")
        else:
            for k, v in result.items():
                print(f"  {k:20s} = {v}")
        return
    
    if 'formula' in result:
        print(f"\nFormula: {result['formula']}")
        print(f"Result: {result.get('result', 'N/A')}")
        if 'inputs' in result:
            print("\nInputs:")
            table_data = [[k, v] for k, v in result['inputs'].items()]
            print(tabulate(table_data, headers=['Parameter', 'Value'], tablefmt='grid'))
    else:
        print(tabulate([result], headers='keys', tablefmt='grid'))


def print_energy_projection(result: Dict[str, Any]) -> None:
    """Print energy projection result as table."""
    print("\nEnergy Projection:")
    table_data = [
        ['ΔEΨ', result.get('delta_E_psi', 'N/A')],
        ['E_reflex', result.get('E_reflex', 'N/A')],
        ['ΔEΨ_theta', result.get('delta_E_psi_theta', 'N/A')],
        ['E_mind', result.get('E_mind', 'N/A')],
        ['E_coherence', result.get('E_coherence', 'N/A')],
        ['E_neural', result.get('E_neural', 'N/A')],
        ['E_bind', result.get('E_bind', 'N/A')],
        ['E_mem', result.get('E_mem', 'N/A')],
        ['Verdict', result.get('verdict', 'N/A')],
    ]
    print(tabulate(table_data, headers=['Energy', 'Value'], tablefmt='grid'))


def print_decision_result(result: Dict[str, Any]) -> None:
    """Print decision result as table."""
    print("\nDecision Result:")
    table_data = [
        ['Verdict', result.get('verdict', 'N/A')],
        ['Protocol', result.get('protocol', 'N/A')],
        ['Context', result.get('context', 'N/A')],
        ['Rule Fail', result.get('rule_fail', False)],
    ]
    
    if 'metrics' in result:
        metrics = result['metrics']
        table_data.extend([
            ['Eμ', metrics.get('E_mu', 'N/A')],
            ['H', metrics.get('H', 'N/A')],
            ['D', metrics.get('D', 'N/A')],
            ['S', metrics.get('S', 'N/A')],
            ['T', metrics.get('T', 'N/A')],
            ['V', metrics.get('V', 'N/A')],
        ])
    
    if 'reasons' in result:
        table_data.append(['Reasons', '; '.join(result['reasons'])])
    
    print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))


def print_memory(result: Dict[str, Any]) -> None:
    """Print memory data as table."""
    print("\nMemory Data:")
    if isinstance(result, dict):
        table_data = [[k, v] for k, v in result.items()]
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    else:
        print(result)


def print_memory_fields(fields: list) -> None:
    """Print memory fields list as table."""
    print("\nMemory Fields:")
    table_data = [[i+1, field] for i, field in enumerate(fields)]
    print(tabulate(table_data, headers=['#', 'Field Name'], tablefmt='grid'))


def print_memory_stats(stats: Dict[str, Any]) -> None:
    """Print memory statistics as table."""
    print("\nMemory Statistics:")
    if isinstance(stats, dict) and 'stats' in stats:
        table_data = [[k, v] for k, v in stats['stats'].items()]
        print(tabulate(table_data, headers=['Statistic', 'Value'], tablefmt='grid'))
    else:
        print(tabulate([stats], headers='keys', tablefmt='grid'))

