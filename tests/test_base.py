"""
Test configuration and utilities for Flite tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import flite
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

class TestBase:
    """Base class for all Flite tests"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_project(self, name="test_project"):
        """Create a test project directory"""
        project_path = Path(self.test_dir) / name
        project_path.mkdir()
        return project_path
    
    def assert_file_exists(self, file_path):
        """Assert that a file exists"""
        assert os.path.exists(file_path), f"File {file_path} does not exist"
    
    def assert_file_contains(self, file_path, content):
        """Assert that a file contains specific content"""
        self.assert_file_exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            assert content in file_content, f"Content '{content}' not found in {file_path}"
    
    def assert_directory_exists(self, dir_path):
        """Assert that a directory exists"""
        assert os.path.exists(dir_path) and os.path.isdir(dir_path), f"Directory {dir_path} does not exist"
