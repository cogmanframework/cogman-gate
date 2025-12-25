"""
CLI Safety Checks

Hard CLI-level safety checks before any operations
"""

import sys
import os
from typing import List, Tuple


class SafetyChecker:
    """CLI-level safety checker."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def check(self) -> bool:
        """
        Run all safety checks.
        
        Returns:
            True if all checks pass, False otherwise
        """
        self.errors.clear()
        self.warnings.clear()
        
        # Check 1: Python version
        self._check_python_version()
        
        # Check 2: Required modules
        self._check_required_modules()
        
        # Check 3: Kernel availability
        self._check_kernel_availability()
        
        # Check 4: File permissions (if needed)
        self._check_file_permissions()
        
        # Print warnings
        if self.warnings:
            for warning in self.warnings:
                print(f"WARNING: {warning}", file=sys.stderr)
        
        # Return success if no errors
        return len(self.errors) == 0
    
    def _check_python_version(self) -> None:
        """Check Python version."""
        if sys.version_info < (3, 7):
            self.errors.append(
                f"Python 3.7+ required, got {sys.version_info.major}.{sys.version_info.minor}"
            )
    
    def _check_required_modules(self) -> None:
        """Check required Python modules."""
        required_modules = ['argparse']  # Built-in, but check anyway
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.errors.append(f"Required module not found: {module}")
        
        # Optional but recommended modules
        optional_modules = {
            'tabulate': 'Table output formatting',
            'yaml': 'YAML config support'
        }
        
        for module, description in optional_modules.items():
            try:
                __import__(module)
            except ImportError:
                self.warnings.append(
                    f"Optional module not found: {module} ({description})"
                )
    
    def _check_kernel_availability(self) -> None:
        """Check kernel availability."""
        try:
            from bridge import KernelBridge
            # Try to load library (will fail if not built)
            try:
                bridge = KernelBridge()
                # Success - kernel is available
            except Exception as e:
                self.warnings.append(
                    f"Kernel bridge available but library not loaded: {e}"
                )
        except ImportError:
            self.warnings.append(
                "Kernel bridge not available (some commands may not work)"
            )
    
    def _check_file_permissions(self) -> None:
        """Check file permissions for common directories."""
        # Check if we can write to current directory
        try:
            test_file = '.cogman_cli_test'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (OSError, PermissionError):
            self.warnings.append(
                "Cannot write to current directory (some commands may fail)"
            )
    
    def get_errors(self) -> List[str]:
        """Get list of errors."""
        return self.errors.copy()
    
    def get_warnings(self) -> List[str]:
        """Get list of warnings."""
        return self.warnings.copy()

