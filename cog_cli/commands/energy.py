"""
Energy Command - Inspect EPS-8 / CORE formulas

NO LOGIC - delegates to adapters
"""

import sys
from typing import Any

from ..adapters import kernel_adapter
from ..output import table, json, pretty


def handle(args: Any) -> int:
    """Handle energy command."""
    if args.subcommand == 'compute':
        return _handle_compute(args)
    elif args.subcommand == 'project':
        return _handle_project(args)
    elif args.subcommand == 'validate':
        return _handle_validate(args)
    else:
        print(f"ERROR: Unknown subcommand: {args.subcommand}", file=sys.stderr)
        return 1


def _handle_compute(args: Any) -> int:
    """Compute specific formula."""
    if not args.formula:
        print("ERROR: --formula is required for compute", file=sys.stderr)
        return 1
    
    # Build EPS-8 state from args
    eps8_state = {}
    if args.I is not None:
        eps8_state['I'] = args.I
    if args.P is not None:
        eps8_state['P'] = args.P
    if args.S is not None:
        eps8_state['S'] = args.S
    if args.H is not None:
        eps8_state['H'] = args.H
    if args.A is not None:
        eps8_state['A'] = args.A
    if args.S_a is not None:
        eps8_state['S_a'] = args.S_a
    if args.theta is not None:
        eps8_state['theta'] = args.theta
    
    # Delegate to adapter
    try:
        result = kernel_adapter.compute_formula(args.formula, eps8_state)
        
        # Output result
        if args.output_format == 'json':
            json.print_energy_result(result)
        elif args.output_format == 'table':
            table.print_energy_result(result)
        else:
            pretty.print_energy_result(result)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_project(args: Any) -> int:
    """Project energy from EPS-8 state."""
    # Build EPS-8 state from args
    eps8_state = {}
    if args.I is not None:
        eps8_state['I'] = args.I
    if args.P is not None:
        eps8_state['P'] = args.P
    if args.S is not None:
        eps8_state['S'] = args.S
    if args.H is not None:
        eps8_state['H'] = args.H
    if args.A is not None:
        eps8_state['A'] = args.A
    if args.S_a is not None:
        eps8_state['S_a'] = args.S_a
    if args.theta is not None:
        eps8_state['theta'] = args.theta
    
    # Delegate to adapter
    try:
        result = kernel_adapter.compute_energy_projection(eps8_state)
        
        # Output result
        if args.output_format == 'json':
            json.print_energy_projection(result)
        elif args.output_format == 'table':
            table.print_energy_projection(result)
        else:
            pretty.print_energy_projection(result)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_validate(args: Any) -> int:
    """Validate EPS-8 state."""
    # Build EPS-8 state from args
    eps8_state = {}
    if args.I is not None:
        eps8_state['I'] = args.I
    if args.P is not None:
        eps8_state['P'] = args.P
    if args.S is not None:
        eps8_state['S'] = args.S
    if args.H is not None:
        eps8_state['H'] = args.H
    if args.A is not None:
        eps8_state['A'] = args.A
    if args.S_a is not None:
        eps8_state['S_a'] = args.S_a
    if args.theta is not None:
        eps8_state['theta'] = args.theta
    
    # Delegate to adapter
    try:
        is_valid, errors = kernel_adapter.validate_eps8_state(eps8_state)
        
        if is_valid:
            print("✓ EPS-8 state is valid")
            return 0
        else:
            print("✗ EPS-8 state is invalid:")
            for error in errors:
                print(f"  - {error}")
            return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

