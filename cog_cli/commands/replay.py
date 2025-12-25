"""
Replay Command - Replay trajectory from logs

NO LOGIC - delegates to adapters
"""

import sys
from typing import Any

from ..output import table, json, pretty


def handle(args: Any) -> int:
    """Handle replay command."""
    if not args.log_file:
        print("ERROR: --log-file is required", file=sys.stderr)
        return 1
    
    try:
        # TODO: Implement trajectory replay
        print(f"Replaying trajectory from: {args.log_file}")
        if args.step:
            print(f"Replaying step: {args.step}")
        print("(Trajectory replay not yet implemented)")
        
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

