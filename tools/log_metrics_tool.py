"""
Log and Metrics Tool

Purpose: CLI tool to view logs and metrics
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from storage import LogViewer, MetricsViewer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="View logs and metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Log commands
    log_parser = subparsers.add_parser("log", help="View logs")
    log_subparsers = log_parser.add_subparsers(dest="log_command", help="Log commands")
    
    log_list_parser = log_subparsers.add_parser("list", help="List logs")
    log_list_parser.add_argument("--limit", type=int, help="Limit number of logs")
    
    log_get_parser = log_subparsers.add_parser("get", help="Get log by trace_id")
    log_get_parser.add_argument("trace_id", help="Trace ID")
    
    log_query_parser = log_subparsers.add_parser("query", help="Query logs")
    log_query_parser.add_argument("--action-type", help="Filter by action type")
    log_query_parser.add_argument("--success", type=bool, help="Filter by success")
    
    # Metrics commands
    metrics_parser = subparsers.add_parser("metrics", help="View metrics")
    metrics_subparsers = metrics_parser.add_subparsers(dest="metrics_command", help="Metrics commands")
    
    metrics_list_parser = metrics_subparsers.add_parser("list", help="List metrics")
    metrics_list_parser.add_argument("--limit", type=int, help="Limit number of metrics")
    
    metrics_get_parser = metrics_subparsers.add_parser("get", help="Get metrics by trace_id")
    metrics_get_parser.add_argument("trace_id", help="Trace ID")
    
    metrics_stats_parser = metrics_subparsers.add_parser("stats", help="Show statistics")
    
    metrics_query_parser = metrics_subparsers.add_parser("query", help="Query metrics")
    metrics_query_parser.add_argument("--gate-verdict", help="Filter by gate verdict")
    metrics_query_parser.add_argument("--action-type", help="Filter by action type")
    metrics_query_parser.add_argument("--success", type=bool, help="Filter by success")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "log":
        log_viewer = LogViewer()
        
        if args.log_command == "list":
            logs = log_viewer.list_logs(limit=args.limit)
            print(f"Found {len(logs)} logs")
            for log in logs:
                print(log_viewer.format_log(log))
        
        elif args.log_command == "get":
            log = log_viewer.get_log(args.trace_id)
            if log:
                print(log_viewer.format_log(log))
            else:
                print(f"Log not found: {args.trace_id}")
        
        elif args.log_command == "query":
            logs = log_viewer.query_logs(
                action_type=args.action_type,
                success=args.success
            )
            print(f"Found {len(logs)} matching logs")
            for log in logs:
                print(log_viewer.format_log(log))
    
    elif args.command == "metrics":
        metrics_viewer = MetricsViewer()
        
        if args.metrics_command == "list":
            metrics = metrics_viewer.list_metrics(limit=args.limit)
            print(f"Found {len(metrics)} metrics")
            for metric in metrics:
                print(metrics_viewer.format_metrics(metric))
        
        elif args.metrics_command == "get":
            metrics = metrics_viewer.get_metrics(args.trace_id)
            if metrics:
                print(metrics_viewer.format_metrics(metrics))
            else:
                print(f"Metrics not found: {args.trace_id}")
        
        elif args.metrics_command == "stats":
            stats = metrics_viewer.get_statistics()
            print("=== Metrics Statistics ===")
            print(f"Total: {stats.get('total', 0)}")
            if stats.get('total', 0) > 0:
                exec_time = stats.get('execution_time', {})
                print(f"\nExecution Time:")
                print(f"  Mean: {exec_time.get('mean', 0):.3f}s")
                print(f"  Median: {exec_time.get('median', 0):.3f}s")
                print(f"  Min: {exec_time.get('min', 0):.3f}s")
                print(f"  Max: {exec_time.get('max', 0):.3f}s")
                
                print(f"\nGate Verdicts:")
                for verdict, count in stats.get('gate_verdicts', {}).items():
                    print(f"  {verdict}: {count}")
                
                print(f"\nAction Types:")
                for action_type, count in stats.get('action_types', {}).items():
                    print(f"  {action_type}: {count}")
                
                print(f"\nSuccess Rate: {stats.get('success_rate', 0):.2%}")
                print(f"Success: {stats.get('success_count', 0)}")
                print(f"Failure: {stats.get('failure_count', 0)}")
        
        elif args.metrics_command == "query":
            metrics = metrics_viewer.query_metrics(
                gate_verdict=args.gate_verdict,
                action_type=args.action_type,
                success=args.success
            )
            print(f"Found {len(metrics)} matching metrics")
            for metric in metrics:
                print(metrics_viewer.format_metrics(metric))


if __name__ == "__main__":
    main()

