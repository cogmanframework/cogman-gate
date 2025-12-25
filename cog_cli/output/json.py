"""
JSON Output Formatter

Formatting only - no logic
"""

import json
from typing import Dict, Any


def print_energy_result(result: Dict[str, Any]) -> None:
    """Print energy computation result as JSON."""
    print(json.dumps(result, indent=2))


def print_energy_projection(result: Dict[str, Any]) -> None:
    """Print energy projection result as JSON."""
    print(json.dumps(result, indent=2))


def print_decision_result(result: Dict[str, Any]) -> None:
    """Print decision result as JSON."""
    print(json.dumps(result, indent=2))


def print_memory(result: Dict[str, Any]) -> None:
    """Print memory data as JSON."""
    print(json.dumps(result, indent=2))


def print_memory_fields(fields: list) -> None:
    """Print memory fields list as JSON."""
    print(json.dumps({'fields': fields}, indent=2))


def print_memory_stats(stats: Dict[str, Any]) -> None:
    """Print memory statistics as JSON."""
    print(json.dumps(stats, indent=2))

