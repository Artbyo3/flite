"""
Tests for Flite colors and UI
"""
import pytest
from flite.colors import Colors, UI
from .test_base import TestBase

class TestColors(TestBase):
    """Test color and UI functionality"""
    
    def test_colors_available(self):
        """Test that color constants are available"""
        assert Colors.RED is not None
        assert Colors.GREEN is not None
        assert Colors.BLUE is not None
        assert Colors.YELLOW is not None
        assert Colors.BRIGHT_RED is not None
        assert Colors.BRIGHT_GREEN is not None
        assert Colors.BRIGHT_BLUE is not None
        assert Colors.BRIGHT_YELLOW is not None
        assert Colors.RESET is not None
    
    def test_ui_logo(self):
        """Test logo generation"""
        logo = UI.logo()
        assert logo is not None
        # Check for ASCII art characters instead of exact text due to color codes
        assert '███████╗' in logo  # First line of FLITE ASCII art
        assert 'Flask Project Generator' in logo
    
    def test_ui_header(self):
        """Test header generation"""
        header = UI.header("Test Header")
        assert header is not None
        assert 'Test Header' in header
        assert '╔' in header  # Box drawing characters
        assert '╗' in header
        assert '╚' in header
        assert '╝' in header
    
    def test_ui_header_auto_width(self):
        """Test header with auto width"""
        long_text = "This is a very long header text that should auto-adjust width"
        header = UI.header(long_text)
        assert header is not None
        assert long_text in header
    
    def test_ui_section_title(self):
        """Test section title generation"""
        title = UI.section_title("Test Section")
        assert title is not None
        assert 'Test Section' in title
        assert '─' in title  # Underline characters
    
    def test_ui_box(self):
        """Test box generation"""
        content = "Test content\nSecond line"
        box = UI.box(content, "Test Title")
        assert box is not None
        assert 'Test Title' in box
        assert 'Test content' in box
        assert 'Second line' in box
        assert '┌' in box  # Box drawing characters
        assert '┐' in box
        assert '└' in box
        assert '┘' in box
    
    def test_ui_box_no_title(self):
        """Test box generation without title"""
        content = "Test content"
        box = UI.box(content)
        assert box is not None
        assert 'Test content' in box
    
    def test_ui_menu_item(self):
        """Test menu item generation"""
        # Test unselected item
        item = UI.menu_item("Test Item")
        assert item is not None
        assert 'Test Item' in item
        
        # Test selected item
        selected_item = UI.menu_item("Test Item", selected=True)
        assert selected_item is not None
        assert 'Test Item' in selected_item
        assert '>' in selected_item
    
        # Test success message styling - should contain either Unicode or ASCII version
        message = UI.success("Test success")
        assert message is not None
        assert 'Test success' in message
        assert ('✓' in message or '[OK]' in message)
    
    def test_ui_error(self):
        """Test error message styling - should contain either Unicode or ASCII version"""
        message = UI.error("Test error")
        assert message is not None
        assert 'Test error' in message
        assert ('✗' in message or '[ERROR]' in message)
    
    def test_ui_warning(self):
        """Test warning message styling - should contain either Unicode or ASCII version"""
        message = UI.warning("Test warning")
        assert message is not None
        assert 'Test warning' in message
        assert ('⚠' in message or '[WARNING]' in message)
    
    def test_ui_info(self):
        """Test info message styling - should contain either Unicode or ASCII version"""
        message = UI.info("Test info")
        assert message is not None
        assert 'Test info' in message
        assert ('ℹ' in message or '[INFO]' in message)
    
    def test_ui_prompt(self):
        """Test prompt styling - should contain either Unicode or ASCII version"""
        message = UI.prompt("Test prompt")
        assert message is not None
        assert 'Test prompt' in message
        assert ('►' in message or '>' in message)
    
    def test_ui_highlight(self):
        """Test highlight styling"""
        message = UI.highlight("Test highlight")
        assert message is not None
        assert 'Test highlight' in message
    
    def test_ui_dimmed(self):
        """Test dimmed styling"""
        message = UI.dimmed("Test dimmed")
        assert message is not None
        assert 'Test dimmed' in message
    
    def test_ui_progress_bar(self):
        """Test progress bar generation"""
        progress = UI.progress_bar(50, 100)
        assert progress is not None
        assert '50.0%' in progress
        assert '█' in progress or '░' in progress
    
    def test_ui_separator(self):
        """Test separator generation"""
        separator = UI.separator()
        assert separator is not None
        assert '─' in separator
    
    def test_ui_key_hint(self):
        """Test key hint styling"""
        hint = UI.key_hint("Ctrl+C", "Cancel")
        assert hint is not None
        assert 'Ctrl+C' in hint
        assert 'Cancel' in hint
