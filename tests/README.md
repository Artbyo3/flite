# Flite Test Suite

## Overview
This directory contains a comprehensive test suite for Flite CLI tool that automatically tests all functionality.

## Test Structure

### Test Files
- `test_base.py` - Base test class with common utilities
- `test_cli.py` - Tests for CLI commands
- `test_generator.py` - Tests for ProjectGenerator class
- `test_utils.py` - Tests for utility functions
- `test_colors.py` - Tests for color and UI components
- `test_interactive.py` - Tests for interactive mode

### Configuration Files
- `pytest.ini` - Pytest configuration
- `requirements.txt` - Test dependencies
- `run_tests.py` - Test runner script

## Running Tests

### Quick Test Run
```bash
python run_tests.py
```

### Using Pytest Directly
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_cli.py

# Run specific test
pytest tests/test_cli.py::TestCLI::test_version_command

# Run with coverage
pytest --cov=flite --cov-report=html
```

### Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

### What's Tested
- ✅ CLI commands (create, run, build, init, interactive)
- ✅ ProjectGenerator class methods
- ✅ Input validation functions
- ✅ File generation
- ✅ Directory structure creation
- ✅ Error handling
- ✅ Color and UI components
- ✅ Interactive mode functionality
- ✅ Utility functions

### Test Types
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test complete workflows
- **CLI Tests**: Test command-line interface
- **Error Tests**: Test error handling and edge cases

## Test Environment

### Setup
Each test runs in an isolated temporary directory to avoid conflicts.

### Cleanup
All test artifacts are automatically cleaned up after each test.

## Continuous Integration

### GitHub Actions
Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Multiple operating systems (Ubuntu, Windows, macOS)

### Coverage Reports
- HTML coverage reports generated
- Coverage uploaded to Codecov
- Coverage badges in README

## Adding New Tests

### Test Structure
```python
from tests.test_base import TestBase

class TestNewFeature(TestBase):
    def test_feature_name(self):
        """Test description"""
        # Test implementation
        assert condition
```

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Assertions
Use the base class assertions:
- `self.assert_file_exists(path)`
- `self.assert_file_contains(path, content)`
- `self.assert_directory_exists(path)`

## Debugging Tests

### Verbose Output
```bash
pytest -v -s
```

### Debug Mode
```bash
pytest --pdb
```

### Specific Test
```bash
pytest tests/test_cli.py::TestCLI::test_create_command_basic -v -s
```

## Test Data

### Temporary Files
Tests create temporary files and directories that are automatically cleaned up.

### Mock Data
Use pytest-mock for mocking external dependencies.

## Performance

### Parallel Testing
```bash
pytest -n auto  # Run tests in parallel
```

### Slow Tests
Mark slow tests with `@pytest.mark.slow`

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure flite package is installed
2. **Permission Errors**: Check file permissions in test directory
3. **Path Issues**: Use absolute paths in tests

### Test Failures
1. Check test output for specific error messages
2. Run individual tests to isolate issues
3. Check test environment setup

## Best Practices

### Test Design
- One assertion per test when possible
- Clear test names and descriptions
- Use setup/teardown methods
- Test both success and failure cases

### Test Data
- Use realistic test data
- Test edge cases and boundary conditions
- Clean up test artifacts

### Maintenance
- Keep tests up to date with code changes
- Remove obsolete tests
- Add tests for new features
- Monitor test performance
