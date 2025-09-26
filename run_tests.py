"""
Test runner for Flite
Run all tests automatically
"""
import pytest
import sys
import os

def run_tests():
    """Run all Flite tests"""
    print("🧪 Running Flite Test Suite...")
    print("=" * 50)
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Change to project root
    os.chdir(current_dir)
    
    # Run tests with verbose output
    result = pytest.main([
        'tests/',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--color=yes',  # Colored output
        '--durations=10',  # Show slowest 10 tests
    ])
    
    if result == 0:
        print("\nAll tests passed!")
    else:
        print(f"\nTests failed with exit code: {result}")
    
    return result

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
