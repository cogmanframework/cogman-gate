#!/usr/bin/env python3
"""
Cogman CLI - Main Entry Point

Usage:
    python -m cog_cli.main <command> [options]
    cogman <command> [options]  # if installed
"""

import sys
import argparse
from typing import List, Optional

from .commands import energy, gate, trace, replay, memory, config
from .safety import SafetyChecker


def create_parser() -> argparse.ArgumentParser:
    """Create main argument parser."""
    parser = argparse.ArgumentParser(
        prog='cogman',
        description='Cogman Gate CLI - Control & Operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cogman energy compute --I 0.8 --P 0.6 --S_a 0.7 --H 0.3
  cogman gate test --context robot_control --E_mu 50.0 --H 0.2
  cogman trace view --trace-id abc123
  cogman replay --log-file trajectory.log
  cogman memory inspect --field episodic
  cogman config validate --file gate_profiles.yaml
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['table', 'json', 'pretty'],
        default='pretty',
        help='Output format (default: pretty)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND'
    )
    
    # Energy command
    energy_parser = subparsers.add_parser(
        'energy',
        help='Inspect EPS-8 / CORE formulas'
    )
    energy_parser.add_argument(
        'subcommand',
        choices=['compute', 'project', 'validate'],
        help='Energy operation'
    )
    energy_parser.add_argument(
        '--I', type=float, help='Intensity'
    )
    energy_parser.add_argument(
        '--P', type=float, help='Polarity'
    )
    energy_parser.add_argument(
        '--S', type=float, help='Stability'
    )
    energy_parser.add_argument(
        '--H', type=float, help='Entropy'
    )
    energy_parser.add_argument(
        '--A', type=float, help='Awareness'
    )
    energy_parser.add_argument(
        '--S_a', type=float, help='Sub-awareness'
    )
    energy_parser.add_argument(
        '--theta', type=float, help='Phase angle'
    )
    energy_parser.add_argument(
        '--formula', choices=['CORE-1', 'CORE-2', 'CORE-3', 'CORE-4', 'CORE-5', 'CORE-6', 'CORE-7', 'CORE-8'],
        help='Specific formula to compute'
    )
    
    # Gate command
    gate_parser = subparsers.add_parser(
        'gate',
        help='Test Decision Gate (ALLOW/REVIEW/BLOCK)'
    )
    gate_parser.add_argument(
        'subcommand',
        choices=['test', 'evaluate', 'validate'],
        help='Gate operation'
    )
    gate_parser.add_argument(
        '--context',
        choices=['robot_control', 'chat', 'finance', 'default'],
        default='default',
        help='Decision context'
    )
    gate_parser.add_argument(
        '--E_mu', type=float, help='Internal readiness metric'
    )
    gate_parser.add_argument(
        '--H', type=float, help='Entropy'
    )
    gate_parser.add_argument(
        '--D', type=float, help='Semantic drift'
    )
    gate_parser.add_argument(
        '--S', type=float, default=1.0, help='Safety rule score'
    )
    gate_parser.add_argument(
        '--policy-file', help='Gate policy YAML file'
    )
    
    # Trace command
    trace_parser = subparsers.add_parser(
        'trace',
        help='View execution traces'
    )
    trace_parser.add_argument(
        'subcommand',
        choices=['view', 'list', 'search'],
        help='Trace operation'
    )
    trace_parser.add_argument(
        '--trace-id', help='Specific trace ID'
    )
    trace_parser.add_argument(
        '--limit', type=int, default=10, help='Number of traces to show'
    )
    trace_parser.add_argument(
        '--filter', help='Filter expression'
    )
    
    # Replay command
    replay_parser = subparsers.add_parser(
        'replay',
        help='Replay trajectory from logs'
    )
    replay_parser.add_argument(
        '--log-file', required=True, help='Trajectory log file'
    )
    replay_parser.add_argument(
        '--step', type=int, help='Replay specific step'
    )
    replay_parser.add_argument(
        '--output', help='Output file for replay results'
    )
    
    # Memory command
    memory_parser = subparsers.add_parser(
        'memory',
        help='Inspect memory fields (read-only)'
    )
    memory_parser.add_argument(
        'subcommand',
        choices=['inspect', 'list', 'stats'],
        help='Memory operation'
    )
    memory_parser.add_argument(
        '--field',
        choices=['episodic', 'semantic', 'procedural', 'identity'],
        help='Specific memory field'
    )
    memory_parser.add_argument(
        '--key', help='Memory key to inspect'
    )
    
    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Validate config / policy'
    )
    config_parser.add_argument(
        'subcommand',
        choices=['validate', 'show', 'diff'],
        help='Config operation'
    )
    config_parser.add_argument(
        '--file', required=True, help='Config file to validate'
    )
    config_parser.add_argument(
        '--schema', help='Schema file for validation'
    )
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Safety check
    safety_checker = SafetyChecker()
    if not safety_checker.check():
        print("ERROR: Safety checks failed. Aborting.", file=sys.stderr)
        return 1
    
    # Route to command handler
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    try:
        if parsed_args.command == 'energy':
            return energy.handle(parsed_args)
        elif parsed_args.command == 'gate':
            return gate.handle(parsed_args)
        elif parsed_args.command == 'trace':
            return trace.handle(parsed_args)
        elif parsed_args.command == 'replay':
            return replay.handle(parsed_args)
        elif parsed_args.command == 'memory':
            return memory.handle(parsed_args)
        elif parsed_args.command == 'config':
            return config.handle(parsed_args)
        else:
            print(f"ERROR: Unknown command: {parsed_args.command}", file=sys.stderr)
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

