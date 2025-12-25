"""
Runtime Error Handler

Purpose: Centralized error handling for Runtime Loop
"""

from typing import Dict, Any, Optional, Callable
import logging
import traceback
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RuntimeErrorHandler:
    """
    Runtime Error Handler
    
    Purpose: Handle errors in Runtime Loop phases
    """
    
    def __init__(self):
        """Initialize error handler."""
        self.error_count = 0
        self.error_history: list = []
    
    def handle_error(
        self,
        phase: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM
    ) -> Dict[str, Any]:
        """
        Handle error in Runtime Loop phase.
        
        Args:
            phase: Phase name where error occurred
            error: Exception that occurred
            context: Additional context
            severity: Error severity
        
        Returns:
            Error handling result
        """
        self.error_count += 1
        
        error_info = {
            "phase": phase,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "severity": severity.value,
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": None
        }
        
        import time
        error_info["timestamp"] = time.time()
        
        # Log error
        log_level = {
            ErrorSeverity.LOW: logging.DEBUG,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(severity, logging.ERROR)
        
        logger.log(
            log_level,
            f"Error in {phase}: {error}",
            exc_info=True,
            extra={"context": context}
        )
        
        # Store in history
        self.error_history.append(error_info)
        
        # Return error handling result
        return {
            "handled": True,
            "phase": phase,
            "error_type": type(error).__name__,
            "action": "abort_cycle",  # Runtime Loop should abort current cycle
            "continue": True  # Continue to next input
        }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return {
            "total_errors": self.error_count,
            "recent_errors": self.error_history[-10:] if self.error_history else [],
            "error_by_phase": self._count_errors_by_phase(),
            "error_by_severity": self._count_errors_by_severity()
        }
    
    def _count_errors_by_phase(self) -> Dict[str, int]:
        """Count errors by phase."""
        counts = {}
        for error in self.error_history:
            phase = error.get("phase", "unknown")
            counts[phase] = counts.get(phase, 0) + 1
        return counts
    
    def _count_errors_by_severity(self) -> Dict[str, int]:
        """Count errors by severity."""
        counts = {}
        for error in self.error_history:
            severity = error.get("severity", "unknown")
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    def clear_history(self):
        """Clear error history."""
        self.error_history = []
        self.error_count = 0

