"""
Memory Command - Inspect memory fields (read-only)

NO LOGIC - delegates to adapters
"""

import sys
from typing import Any

from ..adapters import memory_adapter
from ..output import table, json, pretty


def handle(args: Any) -> int:
    """Handle memory command."""
    if args.subcommand == 'inspect':
        return _handle_inspect(args)
    elif args.subcommand == 'list':
        return _handle_list(args)
    elif args.subcommand == 'stats':
        return _handle_stats(args)
    else:
        print(f"ERROR: Unknown subcommand: {args.subcommand}", file=sys.stderr)
        return 1


def _handle_inspect(args: Any) -> int:
    """Inspect specific memory field or key."""
    if not args.field and not args.key:
        print("ERROR: --field or --key is required for inspect", file=sys.stderr)
        return 1
    
    try:
        if args.key:
            result = memory_adapter.get_memory_by_key(args.key, args.field)
        else:
            result = memory_adapter.get_memory_field(args.field)
        
        # Output result
        if args.output_format == 'json':
            json.print_memory(result)
        elif args.output_format == 'table':
            table.print_memory(result)
        else:
            pretty.print_memory(result)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_list(args: Any) -> int:
    """List memory fields."""
    try:
        fields = memory_adapter.list_memory_fields()
        
        # Output result
        if args.output_format == 'json':
            json.print_memory_fields(fields)
        elif args.output_format == 'table':
            table.print_memory_fields(fields)
        else:
            pretty.print_memory_fields(fields)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_stats(args: Any) -> int:
    """Show memory statistics."""
    try:
        stats = memory_adapter.get_memory_stats(args.field)
        
        # Output result
        if args.output_format == 'json':
            json.print_memory_stats(stats)
        elif args.output_format == 'table':
            table.print_memory_stats(stats)
        else:
            pretty.print_memory_stats(stats)
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

