"""
Runtime Error Handling Tests

Purpose: Test error handling in Runtime Loop
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from runtime.error_handler import RuntimeErrorHandler, ErrorSeverity
except ImportError:
    # Fallback: import directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "error_handler",
        project_root / "runtime" / "error_handler.py"
    )
    error_handler_module = importlib.util.module_from_spec(spec)
    sys.modules["runtime.error_handler"] = error_handler_module
    spec.loader.exec_module(error_handler_module)
    RuntimeErrorHandler = error_handler_module.RuntimeErrorHandler
    ErrorSeverity = error_handler_module.ErrorSeverity


class TestErrorHandler(unittest.TestCase):
    """Test Error Handler"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.error_handler = RuntimeErrorHandler()
    
    def test_error_handling(self):
        """Test error handling."""
        error = ValueError("Test error")
        
        result = self.error_handler.handle_error(
            phase="TEST_PHASE",
            error=error,
            context={"test": "data"},
            severity=ErrorSeverity.MEDIUM
        )
        
        self.assertTrue(result["handled"])
        self.assertEqual(result["phase"], "TEST_PHASE")
        self.assertEqual(result["error_type"], "ValueError")
        self.assertEqual(result["action"], "abort_cycle")
        self.assertTrue(result["continue"])
    
    def test_error_counting(self):
        """Test error counting."""
        initial_count = self.error_handler.error_count
        
        self.error_handler.handle_error(
            phase="TEST",
            error=ValueError("Test"),
            severity=ErrorSeverity.LOW
        )
        
        self.assertEqual(self.error_handler.error_count, initial_count + 1)
    
    def test_error_summary(self):
        """Test error summary."""
        # Add some errors
        self.error_handler.handle_error(
            phase="PHASE_1",
            error=ValueError("Error 1"),
            severity=ErrorSeverity.LOW
        )
        
        self.error_handler.handle_error(
            phase="PHASE_2",
            error=RuntimeError("Error 2"),
            severity=ErrorSeverity.HIGH
        )
        
        summary = self.error_handler.get_error_summary()
        
        self.assertEqual(summary["total_errors"], 2)
        self.assertIn("error_by_phase", summary)
        self.assertIn("error_by_severity", summary)
        self.assertEqual(summary["error_by_phase"]["PHASE_1"], 1)
        self.assertEqual(summary["error_by_phase"]["PHASE_2"], 1)
    
    def test_error_history(self):
        """Test error history."""
        self.error_handler.handle_error(
            phase="TEST",
            error=ValueError("Test"),
            severity=ErrorSeverity.MEDIUM
        )
        
        self.assertEqual(len(self.error_handler.error_history), 1)
        self.assertEqual(self.error_handler.error_history[0]["phase"], "TEST")
    
    def test_clear_history(self):
        """Test clearing error history."""
        self.error_handler.handle_error(
            phase="TEST",
            error=ValueError("Test"),
            severity=ErrorSeverity.LOW
        )
        
        self.assertEqual(self.error_handler.error_count, 1)
        
        self.error_handler.clear_history()
        
        self.assertEqual(self.error_handler.error_count, 0)
        self.assertEqual(len(self.error_handler.error_history), 0)


if __name__ == "__main__":
    unittest.main()

