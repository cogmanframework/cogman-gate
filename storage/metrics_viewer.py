"""
Metrics Viewer

Purpose: View and query execution metrics
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import time
from datetime import datetime
from statistics import mean, median, stdev


class MetricsViewer:
    """
    Metrics Viewer
    
    Purpose: View and query execution metrics
    """
    
    def __init__(self, metrics_path: str = "storage/runtime/metrics"):
        """
        Initialize Metrics Viewer.
        
        Args:
            metrics_path: Path to metrics storage
        """
        self.metrics_path = Path(metrics_path)
        self.metrics_path.mkdir(parents=True, exist_ok=True)
    
    def list_metrics(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all metrics.
        
        Args:
            limit: Maximum number of metrics to return
        
        Returns:
            List of metrics entries
        """
        metrics = []
        
        for metrics_file in sorted(self.metrics_path.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(metrics_file, 'r') as f:
                    metric_entry = json.load(f)
                    metrics.append(metric_entry)
            except Exception as e:
                print(f"Error reading metrics file {metrics_file}: {e}")
                continue
            
            if limit and len(metrics) >= limit:
                break
        
        return metrics
    
    def get_metrics(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metrics by trace_id.
        
        Args:
            trace_id: Trace identifier
        
        Returns:
            Metrics entry or None
        """
        metrics_file = self.metrics_path / f"{trace_id}.json"
        
        if not metrics_file.exists():
            return None
        
        try:
            with open(metrics_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading metrics file {metrics_file}: {e}")
            return None
    
    def query_metrics(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        gate_verdict: Optional[str] = None,
        action_type: Optional[str] = None,
        success: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Query metrics by criteria.
        
        Args:
            start_time: Start timestamp
            end_time: End timestamp
            gate_verdict: Gate verdict filter
            action_type: Action type filter
            success: Success filter
        
        Returns:
            List of matching metrics entries
        """
        metrics = self.list_metrics()
        results = []
        
        for metric in metrics:
            # Time filter
            if start_time and metric.get("timestamp", 0) < start_time:
                continue
            if end_time and metric.get("timestamp", 0) > end_time:
                continue
            
            # Gate verdict filter
            if gate_verdict and metric.get("gate_verdict") != gate_verdict:
                continue
            
            # Action type filter
            if action_type and metric.get("action_type") != action_type:
                continue
            
            # Success filter
            if success is not None and metric.get("success") != success:
                continue
            
            results.append(metric)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregated statistics.
        
        Returns:
            Statistics dictionary
        """
        metrics = self.list_metrics()
        
        if not metrics:
            return {
                "total": 0,
                "message": "No metrics available"
            }
        
        execution_times = [m.get("execution_time", 0.0) for m in metrics]
        gate_verdicts = [m.get("gate_verdict") for m in metrics]
        action_types = [m.get("action_type") for m in metrics]
        successes = [m.get("success", True) for m in metrics]
        
        # Count gate verdicts
        verdict_counts = {}
        for verdict in gate_verdicts:
            if verdict:
                verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        
        # Count action types
        action_counts = {}
        for action_type in action_types:
            if action_type:
                action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return {
            "total": len(metrics),
            "execution_time": {
                "mean": mean(execution_times) if execution_times else 0.0,
                "median": median(execution_times) if execution_times else 0.0,
                "stdev": stdev(execution_times) if len(execution_times) > 1 else 0.0,
                "min": min(execution_times) if execution_times else 0.0,
                "max": max(execution_times) if execution_times else 0.0
            },
            "gate_verdicts": verdict_counts,
            "action_types": action_counts,
            "success_rate": sum(successes) / len(successes) if successes else 0.0,
            "success_count": sum(successes),
            "failure_count": len(successes) - sum(successes)
        }
    
    def format_metrics(self, metrics: Dict[str, Any]) -> str:
        """
        Format metrics entry for display.
        
        Args:
            metrics: Metrics entry
        
        Returns:
            Formatted string
        """
        trace_id = metrics.get("trace_id", "unknown")
        timestamp = metrics.get("timestamp", 0)
        dt = datetime.fromtimestamp(timestamp) if timestamp else datetime.now()
        
        execution_time = metrics.get("execution_time", 0.0)
        gate_verdict = metrics.get("gate_verdict", "unknown")
        action_type = metrics.get("action_type", "unknown")
        success = metrics.get("success", True)
        
        phase_times = metrics.get("phase_times", {})
        
        phase_times_str = "\n".join([f"  {phase}: {time:.3f}s" for phase, time in phase_times.items()])
        
        return f"""
Trace ID: {trace_id}
Timestamp: {dt.strftime('%Y-%m-%d %H:%M:%S')}
Execution Time: {execution_time:.3f}s
Gate Verdict: {gate_verdict}
Action Type: {action_type}
Success: {success}
Phase Times:
{phase_times_str}
"""

