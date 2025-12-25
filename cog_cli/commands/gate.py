"""
Gate Command - Test Decision Gate (ALLOW/REVIEW/BLOCK)

NO LOGIC - delegates to adapters
"""

import sys
from typing import Any

from ..adapters import gate_adapter
from ..output import table, json, pretty


def handle(args: Any) -> int:
    """Handle gate command."""
    if args.subcommand == 'test':
        return _handle_test(args)
    elif args.subcommand == 'evaluate':
        return _handle_evaluate(args)
    elif args.subcommand == 'validate':
        return _handle_validate(args)
    else:
        print(f"ERROR: Unknown subcommand: {args.subcommand}", file=sys.stderr)
        return 1


def _handle_test(args: Any) -> int:
    """Test decision gate with metrics."""
    # Build metrics from args
    metrics = {}
    if args.E_mu is not None:
        metrics['E_mu'] = args.E_mu
    if args.H is not None:
        metrics['H'] = args.H
    if args.D is not None:
        metrics['D'] = args.D
    if args.S is not None:
        metrics['S'] = args.S
    
    # Delegate to adapter
    try:
        result = gate_adapter.evaluate_decision(
            metrics=metrics,
            context=args.context,
            policy_file=args.policy_file
        )
        
        # Output result
        if args.output_format == 'json':
            json.print_decision_result(result)
        elif args.output_format == 'table':
            table.print_decision_result(result)
        else:
            pretty.print_decision_result(result)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_evaluate(args: Any) -> int:
    """Evaluate decision gate (same as test for now)."""
    return _handle_test(args)


def _handle_validate(args: Any) -> int:
    """Validate gate policy file."""
    if not args.policy_file:
        print("ERROR: --policy-file is required for validate", file=sys.stderr)
        return 1
    
    try:
        is_valid, errors = gate_adapter.validate_policy(args.policy_file)
        
        if is_valid:
            print(f"✓ Policy file '{args.policy_file}' is valid")
            return 0
        else:
            print(f"✗ Policy file '{args.policy_file}' is invalid:")
            for error in errors:
                print(f"  - {error}")
            return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

