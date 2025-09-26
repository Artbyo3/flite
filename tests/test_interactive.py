"""
Tests for Flite interactive mode
"""
import pytest
import os
from flite.simple_interactive import SimpleInteractiveMode
from .test_base import TestBase

class TestInteractiveMode(TestBase):
    """Test interactive mode functionality"""
    
    def test_init(self):
        """Test SimpleInteractiveMode initialization"""
        interactive = SimpleInteractiveMode()
        assert interactive.project_config == {}
    
    def test_get_template_selection(self):
        """Test template selection method exists"""
        interactive = SimpleInteractiveMode()
        # Just test that the method exists and is callable
        assert hasattr(interactive, 'get_template_selection')
        assert callable(interactive.get_template_selection)
    
    def test_get_database_selection(self):
        """Test database selection method exists"""
        interactive = SimpleInteractiveMode()
        # Just test that the method exists and is callable
        assert hasattr(interactive, 'get_database_selection')
        assert callable(interactive.get_database_selection)
    
    def test_get_project_name(self):
        """Test project name method exists"""
        interactive = SimpleInteractiveMode()
        # Just test that the method exists and is callable
        assert hasattr(interactive, 'get_project_name')
        assert callable(interactive.get_project_name)
    
    def test_show_menu(self):
        """Test show menu method exists"""
        interactive = SimpleInteractiveMode()
        # Just test that the method exists and is callable
        assert hasattr(interactive, 'show_menu')
        assert callable(interactive.show_menu)
