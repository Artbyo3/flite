"""
Tests for Flite CLI commands
"""
import pytest
import subprocess
import sys
import os
from .test_base import TestBase

class TestCLI(TestBase):
    """Test CLI commands"""
    
    def test_version_command(self):
        """Test version command"""
        result = subprocess.run([sys.executable, '-m', 'flite', '--version'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert '1.0.1' in result.stdout
    
    def test_help_command(self):
        """Test help command"""
        result = subprocess.run([sys.executable, '-m', 'flite', '--help'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert 'Flite - Flask Project Generator' in result.stdout
        assert 'create' in result.stdout
        assert 'run' in result.stdout
        assert 'build' in result.stdout
        assert 'init' in result.stdout
        assert 'interactive' in result.stdout
    
    def test_create_command_basic(self):
        """Test basic project creation"""
        result = subprocess.run([sys.executable, '-m', 'flite', 'create', 'test_basic'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        self.assert_directory_exists('test_basic')
        self.assert_file_exists('test_basic/app/__init__.py')
        self.assert_file_exists('test_basic/run.py')
        self.assert_file_exists('test_basic/requirements.txt')
    
    def test_create_command_with_options(self):
        """Test project creation with options"""
        result = subprocess.run([
            sys.executable, '-m', 'flite', 'create', 'test_api', 
            '--template', 'api', '--database', 'sqlite', '--api'
        ], capture_output=True, text=True)
        assert result.returncode == 0
        self.assert_directory_exists('test_api')
        self.assert_file_exists('test_api/app/routes.py')
        self.assert_file_exists('test_api/app/api_routes.py')
    
    def test_create_command_invalid_name(self):
        """Test project creation with invalid name"""
        result = subprocess.run([sys.executable, '-m', 'flite', 'create', '123invalid'], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert 'Invalid project name' in result.stdout
    
    def test_create_command_existing_directory(self):
        """Test project creation when directory exists"""
        # Create directory first
        os.makedirs('existing_project')
        result = subprocess.run([sys.executable, '-m', 'flite', 'create', 'existing_project'], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert 'already exists' in result.stdout
    
    def test_init_command(self):
        """Test init command"""
        # Create a test directory
        test_dir = 'init_test'
        os.makedirs(test_dir)
        os.chdir(test_dir)
        
        result = subprocess.run([sys.executable, '-m', 'flite', 'init'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        self.assert_file_exists('app/__init__.py')
        self.assert_file_exists('run.py')
        self.assert_file_exists('requirements.txt')
    
    def test_build_command(self):
        """Test build command"""
        # First create a project
        subprocess.run([sys.executable, '-m', 'flite', 'create', 'build_test'], 
                      capture_output=True, text=True)
        os.chdir('build_test')
        
        result = subprocess.run([sys.executable, '-m', 'flite', 'build'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        self.assert_file_exists('wsgi.py')
    
    def test_build_command_no_project(self):
        """Test build command without project"""
        result = subprocess.run([sys.executable, '-m', 'flite', 'build'], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert 'requirements.txt not found' in result.stdout
