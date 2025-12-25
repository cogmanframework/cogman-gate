"""
Test Runner

Purpose: Run all tests
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def discover_tests():
    """Discover all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Discover tests in tests/ directory
    test_dir = Path(__file__).parent
    discovered = loader.discover(
        str(test_dir),
        pattern='test_*.py',
        top_level_dir=str(project_root)
    )
    
    suite.addTest(discovered)
    return suite


def main():
    """Run all tests."""
    suite = discover_tests()
    
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True
    )
    
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())

