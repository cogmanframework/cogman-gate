"""
Log Viewer

Purpose: View and query execution logs
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import time
from datetime import datetime


class LogViewer:
    """
    Log Viewer
    
    Purpose: View and query execution logs
    """
    
    def __init__(self, log_path: str = "storage/audit/execution_logs"):
        """
        Initialize Log Viewer.
        
        Args:
            log_path: Path to execution logs
        """
        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)
    
    def list_logs(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all logs.
        
        Args:
            limit: Maximum number of logs to return
        
        Returns:
            List of log entries
        """
        logs = []
        
        for log_file in sorted(self.log_path.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(log_file, 'r') as f:
                    log_entry = json.load(f)
                    logs.append(log_entry)
            except Exception as e:
                print(f"Error reading log file {log_file}: {e}")
                continue
            
            if limit and len(logs) >= limit:
                break
        
        return logs
    
    def get_log(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get log by trace_id.
        
        Args:
            trace_id: Trace identifier
        
        Returns:
            Log entry or None
        """
        log_file = self.log_path / f"{trace_id}.json"
        
        if not log_file.exists():
            return None
        
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading log file {log_file}: {e}")
            return None
    
    def query_logs(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        action_type: Optional[str] = None,
        success: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Query logs by criteria.
        
        Args:
            start_time: Start timestamp
            end_time: End timestamp
            action_type: Action type filter
            success: Success filter
        
        Returns:
            List of matching log entries
        """
        logs = self.list_logs()
        results = []
        
        for log in logs:
            # Time filter
            if start_time and log.get("timestamp", 0) < start_time:
                continue
            if end_time and log.get("timestamp", 0) > end_time:
                continue
            
            # Action type filter
            if action_type:
                log_action_type = log.get("action_output", {}).get("action_type")
                if log_action_type != action_type:
                    continue
            
            # Success filter
            if success is not None:
                log_success = log.get("action_output", {}).get("success")
                if log_success != success:
                    continue
            
            results.append(log)
        
        return results
    
    def format_log(self, log: Dict[str, Any]) -> str:
        """
        Format log entry for display.
        
        Args:
            log: Log entry
        
        Returns:
            Formatted string
        """
        trace_id = log.get("trace_id", "unknown")
        timestamp = log.get("timestamp", 0)
        dt = datetime.fromtimestamp(timestamp) if timestamp else datetime.now()
        
        action_output = log.get("action_output", {})
        action_type = action_output.get("action_type", "unknown")
        success = action_output.get("success", True)
        
        trajectory = log.get("trajectory", {})
        state_count = trajectory.get("state_count", 0)
        
        return f"""
Trace ID: {trace_id}
Timestamp: {dt.strftime('%Y-%m-%d %H:%M:%S')}
Action Type: {action_type}
Success: {success}
State Count: {state_count}
"""

