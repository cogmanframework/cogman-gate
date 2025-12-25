"""
Trace Storage

Purpose: Store and retrieve Trace objects
Spec: docs/TRACE_LIFECYCLE_SPEC.md
"""

from typing import Optional, Dict, Any, List
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TraceStorage:
    """
    Trace Storage
    
    Purpose: Store and retrieve Trace objects by state.
    
    Storage Layout:
    storage/trace/
    ├── active/
    │   └── trace_<id>.json
    ├── completed/
    │   └── trace_<id>.json
    ├── blocked/
    │   └── trace_<id>.json
    ├── invalid/
    │   └── trace_<id>.json
    └── archived/
        └── trace_<id>.json
    """
    
    def __init__(self, base_path: str = "storage/trace"):
        """
        Initialize Trace Storage.
        
        Args:
            base_path: Base path for trace storage
        """
        self.base_path = Path(base_path)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage directories exist."""
        states = ["active", "completed", "blocked", "invalid", "archived"]
        for state in states:
            (self.base_path / state).mkdir(parents=True, exist_ok=True)
    
    def save_trace(self, trace: Dict[str, Any], state: str):
        """
        Save trace to storage.
        
        Args:
            trace: Trace dictionary
            state: Trace state (active, completed, blocked, invalid, archived)
        """
        trace_id = trace.get("trace_id", "unknown")
        state_dir = self.base_path / state
        
        # Validate state
        if state not in ["active", "completed", "blocked", "invalid", "archived"]:
            raise ValueError(f"Invalid trace state: {state}")
        
        # Save trace file
        trace_file = state_dir / f"trace_{trace_id}.json"
        
        try:
            with open(trace_file, 'w') as f:
                json.dump(trace, f, indent=2, default=str)
            
            logger.info(f"Trace saved: {trace_id} (state: {state})")
        except Exception as e:
            logger.error(f"Failed to save trace {trace_id}: {e}")
            raise
    
    def load_trace(self, trace_id: str, state: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load trace from storage.
        
        Args:
            trace_id: Trace identifier
            state: Trace state (if known, searches all states if None)
        
        Returns:
            Trace dictionary or None if not found
        """
        if state:
            # Load from specific state
            trace_file = self.base_path / state / f"trace_{trace_id}.json"
            if trace_file.exists():
                try:
                    with open(trace_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Failed to load trace {trace_id}: {e}")
                    return None
        else:
            # Search all states
            states = ["active", "completed", "blocked", "invalid", "archived"]
            for state_dir in states:
                trace_file = self.base_path / state_dir / f"trace_{trace_id}.json"
                if trace_file.exists():
                    try:
                        with open(trace_file, 'r') as f:
                            trace = json.load(f)
                            return trace
                    except Exception as e:
                        logger.error(f"Failed to load trace {trace_id} from {state_dir}: {e}")
                        continue
        
        return None
    
    def list_traces(self, state: str, limit: Optional[int] = None) -> List[str]:
        """
        List trace IDs for a given state.
        
        Args:
            state: Trace state
            limit: Maximum number of traces to return
        
        Returns:
            List of trace IDs
        """
        state_dir = self.base_path / state
        
        if not state_dir.exists():
            return []
        
        trace_ids = []
        for trace_file in state_dir.glob("trace_*.json"):
            trace_id = trace_file.stem.replace("trace_", "")
            trace_ids.append(trace_id)
        
        if limit:
            trace_ids = trace_ids[:limit]
        
        return trace_ids
    
    def move_trace(self, trace_id: str, from_state: str, to_state: str):
        """
        Move trace from one state to another.
        
        Args:
            trace_id: Trace identifier
            from_state: Current state
            to_state: New state
        """
        from_file = self.base_path / from_state / f"trace_{trace_id}.json"
        to_file = self.base_path / to_state / f"trace_{trace_id}.json"
        
        if not from_file.exists():
            raise FileNotFoundError(f"Trace {trace_id} not found in {from_state}")
        
        try:
            # Load trace
            with open(from_file, 'r') as f:
                trace = json.load(f)
            
            # Save to new location
            self.save_trace(trace, to_state)
            
            # Delete old file
            from_file.unlink()
            
            logger.info(f"Trace {trace_id} moved: {from_state} → {to_state}")
        except Exception as e:
            logger.error(f"Failed to move trace {trace_id}: {e}")
            raise
    
    def delete_trace(self, trace_id: str, state: str):
        """
        Delete trace from storage.
        
        Args:
            trace_id: Trace identifier
            state: Trace state
        """
        trace_file = self.base_path / state / f"trace_{trace_id}.json"
        
        if trace_file.exists():
            try:
                trace_file.unlink()
                logger.info(f"Trace {trace_id} deleted from {state}")
            except Exception as e:
                logger.error(f"Failed to delete trace {trace_id}: {e}")
                raise
        else:
            logger.warning(f"Trace {trace_id} not found in {state}")

