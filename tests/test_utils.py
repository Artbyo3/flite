"""
Tests for Flite utilities
"""
import pytest
import os
from flite.utils import print_success, print_error, print_info, print_warning, ensure_directory
from .test_base import TestBase

class TestUtils(TestBase):
    """Test utility functions"""
    
    def test_ensure_directory(self):
        """Test directory creation"""
        test_dir = 'test_directory'
        ensure_directory(test_dir)
        self.assert_directory_exists(test_dir)
        
        # Test nested directory
        nested_dir = 'test_directory/nested/deep'
        ensure_directory(nested_dir)
        self.assert_directory_exists(nested_dir)
    
    def test_print_functions(self):
        """Test print functions don't crash"""
        # These should not raise exceptions
        print_success("Test success message")
        print_error("Test error message")
        print_info("Test info message")
        print_warning("Test warning message")
        
        # If we get here, the functions work
        assert True
