"""
Post-Processor

Purpose: Logging, audit, metrics (PHASE 9)
Spec: docs/RUNTIME_LOOP_SPEC.md
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time
import json
import logging
from pathlib import Path
import threading
from queue import Queue

logger = logging.getLogger(__name__)


@dataclass
class PostProcessInput:
    """Post-Processing Input"""
    trajectory: Dict[str, Any]
    action_output: Any
    trace_id: str
    timestamp: float
    phase_results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Metrics:
    """System Metrics"""
    trace_id: str
    execution_time: float
    phase_times: Dict[str, float] = field(default_factory=dict)
    gate_verdict: Optional[str] = None
    action_type: Optional[str] = None
    success: bool = True
    timestamp: float = 0.0


class PostProcessor:
    """
    Post-Processor
    
    Purpose: Logging, audit, metrics
    
    Rules:
    - MUST NOT affect current loop
    - MUST NOT block execution
    - MUST be asynchronous (if possible)
    - No state modification
    - No decision influence
    - No blocking operations
    """
    
    def __init__(
        self,
        audit_storage_path: str = "storage/audit",
        metrics_storage_path: str = "storage/runtime",
        enable_async: bool = True
    ):
        """
        Initialize Post-Processor.
        
        Args:
            audit_storage_path: Path for audit storage
            metrics_storage_path: Path for metrics storage
            enable_async: Enable asynchronous processing
        """
        self.audit_storage_path = Path(audit_storage_path)
        self.metrics_storage_path = Path(metrics_storage_path)
        self.enable_async = enable_async
        
        # Create storage directories
        self.audit_storage_path.mkdir(parents=True, exist_ok=True)
        self.metrics_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Async queue for non-blocking operations
        if enable_async:
            self.async_queue = Queue()
            self.async_thread = threading.Thread(target=self._async_worker, daemon=True)
            self.async_thread.start()
        else:
            self.async_queue = None
    
    def process(
        self,
        trajectory: Dict[str, Any],
        action_output: Any,
        phase_results: Optional[Dict[str, Any]] = None
    ):
        """
        Process post-processing tasks.
        
        This is the PHASE 9 operation in Runtime Loop.
        
        Args:
            trajectory: Trajectory from execution
            action_output: Action output from PHASE 8
            phase_results: Results from all phases (optional)
        """
        trace_id = trajectory.get("trace_id", action_output.trace_id if hasattr(action_output, 'trace_id') else "")
        
        # Prepare input
        input_data = PostProcessInput(
            trajectory=trajectory,
            action_output=action_output,
            trace_id=trace_id,
            timestamp=time.time(),
            phase_results=phase_results or {}
        )
        
        # Perform post-processing (non-blocking)
        if self.enable_async and self.async_queue:
            # Queue for async processing
            self.async_queue.put(("process", input_data))
        else:
            # Synchronous processing
            self._process_sync(input_data)
    
    def _process_sync(self, input_data: PostProcessInput):
        """Synchronous post-processing."""
        try:
            # 1. Logging
            self._log_execution(input_data)
            
            # 2. Audit trail
            self._store_audit_trail(input_data)
            
            # 3. Metrics collection
            self._collect_metrics(input_data)
            
            # 4. Memory consolidation trigger (async)
            self._trigger_memory_consolidation(input_data)
            
        except Exception as e:
            logger.error(f"Post-processing error: {e}", exc_info=True)
    
    def _async_worker(self):
        """Async worker thread."""
        while True:
            try:
                operation, data = self.async_queue.get(timeout=1.0)
                if operation == "process":
                    self._process_sync(data)
                elif operation == "consolidation":
                    self._do_memory_consolidation(data)
                self.async_queue.task_done()
            except Exception as e:
                logger.error(f"Async worker error: {e}", exc_info=True)
    
    def _log_execution(self, input_data: PostProcessInput):
        """
        Log execution.
        
        Rules:
        - Log to file
        - Include trace_id
        - Include all phase results
        """
        trace_id = input_data.trace_id
        timestamp = input_data.timestamp
        
        log_entry = {
            "trace_id": trace_id,
            "timestamp": timestamp,
            "trajectory": {
                "trace_id": input_data.trajectory.get("trace_id"),
                "state_count": len(input_data.trajectory.get("states", []))
            },
            "action_output": {
                "action_type": getattr(input_data.action_output, 'action_type', 'unknown') if hasattr(input_data.action_output, 'action_type') else str(type(input_data.action_output)),
                "success": getattr(input_data.action_output, 'success', True) if hasattr(input_data.action_output, 'success') else True,
                "trace_id": getattr(input_data.action_output, 'trace_id', trace_id) if hasattr(input_data.action_output, 'trace_id') else trace_id
            },
            "phase_results": input_data.phase_results
        }
        
        # Log to file
        log_file = self.audit_storage_path / "execution_logs" / f"{trace_id}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(log_file, 'w') as f:
                json.dump(log_entry, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to write log file: {e}")
        
        # Also log to logger
        logger.info(f"Execution logged: trace_id={trace_id}")
    
    def _store_audit_trail(self, input_data: PostProcessInput):
        """
        Store audit trail.
        
        Rules:
        - Store complete audit trail
        - Include lineage information
        - Include all phase transitions
        """
        trace_id = input_data.trace_id
        timestamp = input_data.timestamp
        
        audit_entry = {
            "trace_id": trace_id,
            "timestamp": timestamp,
            "trajectory": input_data.trajectory,
            "action_output": {
                "action_type": getattr(input_data.action_output, 'action_type', 'unknown') if hasattr(input_data.action_output, 'action_type') else str(type(input_data.action_output)),
                "output_data": getattr(input_data.action_output, 'output_data', None) if hasattr(input_data.action_output, 'output_data') else None,
                "success": getattr(input_data.action_output, 'success', True) if hasattr(input_data.action_output, 'success') else True,
                "error": getattr(input_data.action_output, 'error', None) if hasattr(input_data.action_output, 'error') else None
            },
            "lineage": {
                "source": input_data.trajectory.get("origin", {}).get("source_id", "unknown"),
                "transformations": input_data.phase_results.get("transformations", []),
                "sink": "action"
            },
            "phase_results": input_data.phase_results
        }
        
        # Store audit trail
        audit_file = self.audit_storage_path / "trace_map" / f"{trace_id}.json"
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(audit_file, 'w') as f:
                json.dump(audit_entry, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to write audit file: {e}")
        
        logger.debug(f"Audit trail stored: trace_id={trace_id}")
    
    def _collect_metrics(self, input_data: PostProcessInput):
        """
        Collect metrics.
        
        Rules:
        - Collect execution metrics
        - Calculate phase times
        - Store metrics
        """
        trace_id = input_data.trace_id
        timestamp = input_data.timestamp
        
        # Calculate metrics
        phase_times = input_data.phase_results.get("phase_times", {})
        execution_time = sum(phase_times.values()) if phase_times else 0.0
        
        metrics = Metrics(
            trace_id=trace_id,
            execution_time=execution_time,
            phase_times=phase_times,
            gate_verdict=input_data.phase_results.get("gate_verdict"),
            action_type=getattr(input_data.action_output, 'action_type', None) if hasattr(input_data.action_output, 'action_type') else None,
            success=getattr(input_data.action_output, 'success', True) if hasattr(input_data.action_output, 'success') else True,
            timestamp=timestamp
        )
        
        # Store metrics
        metrics_file = self.metrics_storage_path / "metrics" / f"{trace_id}.json"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(metrics_file, 'w') as f:
                json.dump({
                    "trace_id": metrics.trace_id,
                    "execution_time": metrics.execution_time,
                    "phase_times": metrics.phase_times,
                    "gate_verdict": metrics.gate_verdict,
                    "action_type": metrics.action_type,
                    "success": metrics.success,
                    "timestamp": metrics.timestamp
                }, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to write metrics file: {e}")
        
        logger.debug(f"Metrics collected: trace_id={trace_id}, execution_time={execution_time:.3f}s")
    
    def _trigger_memory_consolidation(self, input_data: PostProcessInput):
        """
        Trigger memory consolidation (async).
        
        Rules:
        - Trigger asynchronously
        - MUST NOT block
        - MUST NOT affect current loop
        """
        if self.enable_async and self.async_queue:
            # Queue for async consolidation
            self.async_queue.put(("consolidation", input_data))
        else:
            # Synchronous (but should be fast)
            self._do_memory_consolidation(input_data)
    
    def _do_memory_consolidation(self, input_data: PostProcessInput):
        """
        Perform memory consolidation.
        
        Rules:
        - Consolidate memory (if needed)
        - MUST NOT block
        - MUST NOT affect current loop
        """
        trace_id = input_data.trace_id
        
        # Check if consolidation is needed
        # (This would check memory state, trajectory completion, etc.)
        consolidation_needed = self._check_consolidation_needed(input_data)
        
        if consolidation_needed:
            # Trigger consolidation (would call memory consolidation engine)
            logger.info(f"Memory consolidation triggered: trace_id={trace_id}")
            # In real implementation, this would call memory consolidation engine
            # For now, just log
        else:
            logger.debug(f"Memory consolidation not needed: trace_id={trace_id}")
    
    def _check_consolidation_needed(self, input_data: PostProcessInput) -> bool:
        """
        Check if memory consolidation is needed.
        
        Rules:
        - Based on trajectory completion
        - Based on memory state
        - NO blocking checks
        """
        # Simple heuristic: consolidate if trajectory is complete
        trajectory = input_data.trajectory
        states = trajectory.get("states", [])
        
        # Consolidate if trajectory has multiple states
        return len(states) > 1
    
    def shutdown(self):
        """Shutdown post-processor (wait for async operations)."""
        if self.async_queue:
            self.async_queue.join()  # Wait for all tasks to complete
        logger.info("Post-processor shut down")

