"""
Utility functions for Flite CLI
"""

import os
import sys
from .colors import UI

def print_success(message):
    """Print success message with styling"""
    print(UI.success(message))

def print_error(message):
    """Print error message with styling"""
    print(UI.error(message))

def print_info(message):
    """Print info message with styling"""
    print(UI.info(message))

def print_warning(message):
    """Print warning message with styling"""
    print(UI.warning(message))

def ensure_directory(path):
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)

def get_template_path(template_name):
    """Get the path to a template file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'templates', template_name)

def copy_template_file(template_name, destination, context=None):
    """Copy a template file to destination with optional context substitution"""
    template_path = get_template_path(template_name)
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_name}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if context:
        content = content.format(**context)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(content)
