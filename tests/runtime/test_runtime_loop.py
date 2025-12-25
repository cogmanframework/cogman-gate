"""
Runtime Loop Tests

Purpose: Test Runtime Loop with 9 canonical phases
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from runtime import RuntimeLoop, Phase
except ImportError:
    # Fallback: import directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "runtime",
        project_root / "runtime" / "__init__.py"
    )
    runtime_module = importlib.util.module_from_spec(spec)
    sys.modules["runtime"] = runtime_module
    spec.loader.exec_module(runtime_module)
    RuntimeLoop = runtime_module.RuntimeLoop
    Phase = runtime_module.Phase


class TestRuntimeLoop(unittest.TestCase):
    """Test Runtime Loop"""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create minimal Runtime Loop
        self.runtime_loop = RuntimeLoop()
    
    def test_phase_order(self):
        """Test that phases execute in canonical order."""
        phases_executed = []
        
        # Mock phase methods to track execution
        original_methods = {}
        for phase in Phase:
            method_name = f"_phase_{phase.name.lower()}"
            if hasattr(self.runtime_loop, method_name):
                original_methods[method_name] = getattr(self.runtime_loop, method_name)
                
                def make_tracker(phase_name):
                    def tracker(*args, **kwargs):
                        phases_executed.append(phase_name)
                        if original_methods.get(method_name):
                            return original_methods[method_name](*args, **kwargs)
                        return None
                    return tracker
                
                setattr(self.runtime_loop, method_name, make_tracker(phase.name))
        
        # Note: Full execution test would require all modules
        # This is a structure test
        self.assertEqual(len(Phase), 10)  # 0-9 phases
    
    def test_phase_enum(self):
        """Test Phase enum values."""
        self.assertEqual(Phase.IDLE.value, 0)
        self.assertEqual(Phase.INPUT_INTAKE.value, 1)
        self.assertEqual(Phase.SENSORY_ADAPTATION.value, 2)
        self.assertEqual(Phase.PERCEPTION_BOUNDARY.value, 3)
        self.assertEqual(Phase.TRAJECTORY_ADMISSION.value, 4)
        self.assertEqual(Phase.WORKING_MEMORY_CONTROL.value, 5)
        self.assertEqual(Phase.REASONING.value, 6)
        self.assertEqual(Phase.DECISION.value, 7)
        self.assertEqual(Phase.ACTION_OUTPUT.value, 8)
        self.assertEqual(Phase.POST_PROCESSING.value, 9)
    
    def test_runtime_loop_initialization(self):
        """Test Runtime Loop initialization."""
        self.assertFalse(self.runtime_loop.running)
        self.assertEqual(self.runtime_loop.current_phase, Phase.IDLE)
        self.assertEqual(self.runtime_loop.system_state, "running")
    
    def test_runtime_loop_start_stop(self):
        """Test Runtime Loop start/stop."""
        # Start loop (in background thread for testing)
        import threading
        import time
        
        thread = threading.Thread(target=self.runtime_loop.run, daemon=True)
        thread.start()
        
        time.sleep(0.1)  # Let it run briefly
        
        # Stop loop
        self.runtime_loop.stop()
        
        time.sleep(0.1)  # Let it stop
        
        self.assertFalse(self.runtime_loop.running)


class TestRuntimeLoopErrorHandling(unittest.TestCase):
    """Test Runtime Loop error handling"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.runtime_loop = RuntimeLoop()
    
    def test_error_in_phase_aborts_cycle(self):
        """Test that error in phase aborts current cycle."""
        # This would require mocking modules to raise errors
        # For now, test structure
        self.assertTrue(hasattr(self.runtime_loop, '_execute_cycle'))
    
    def test_blocked_trajectory_continues(self):
        """Test that blocked trajectory continues to next input."""
        # This would require full integration
        # For now, test that method exists
        self.assertTrue(hasattr(self.runtime_loop, '_phase_trajectory_admission'))


if __name__ == "__main__":
    unittest.main()

