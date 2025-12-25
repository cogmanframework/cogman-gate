"""
Scheduler

Purpose: Task scheduling
"""

from typing import Dict, Any, List
import time


class Scheduler:
    """
    Task scheduler.
    """
    
    def __init__(self):
        """Initialize scheduler."""
        self.tasks: List[Dict[str, Any]] = []
    
    def schedule(self, task: Dict[str, Any], delay: float = 0.0):
        """Schedule task."""
        self.tasks.append({
            "task": task,
            "execute_at": time.time() + delay,
        })
    
    def execute_pending(self):
        """Execute pending tasks."""
        current_time = time.time()
        pending = [t for t in self.tasks if t["execute_at"] <= current_time]
        self.tasks = [t for t in self.tasks if t["execute_at"] > current_time]
        return pending

