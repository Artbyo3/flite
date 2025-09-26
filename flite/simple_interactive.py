"""
Simple Interactive mode for Flite CLI
Provides interactive menus using only Python standard library
"""

import os
import re
import sys
import msvcrt  # For Windows keyboard input
from .utils import print_success, print_error, print_info, print_warning
from .colors import UI, Colors

class SimpleInteractiveMode:
    def __init__(self):
        self.project_config = {}
    
    def _clear_lines(self, count):
        """Clear the last 'count' lines from terminal"""
        for _ in range(count):
            sys.stdout.write('\033[F')  # Move cursor up one line
            sys.stdout.write('\033[K')  # Clear line
        sys.stdout.flush()
    
    def _get_key(self):
        """Get a single key press (Windows compatible)"""
        if os.name == 'nt':  # Windows
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'up'
                elif key == b'P':  # Down arrow
                    return 'down'
            elif key == b'\r':  # Enter
                return 'enter'
            elif key.lower() == b'w':
                return 'up'
            elif key.lower() == b's':
                return 'down'
            elif key == b' ':  # Space
                return 'space'
            elif key == b'\x1b':  # ESC
                return 'esc'
        else:  # Unix/Linux/Mac
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                key = sys.stdin.read(1)
                if key == '\x1b':  # ESC sequence
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':
                        return 'up'
                    elif key == '\x1b[B':
                        return 'down'
                elif key == '\r' or key == '\n':
                    return 'enter'
                elif key.lower() == 'w':
                    return 'up'
                elif key.lower() == 's':
                    return 'down'
                elif key == ' ':  # Space
                    return 'space'
                elif key == '\x1b':
                    return 'esc'
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
    
    def get_project_name(self):
        """Get project name with validation"""
        while True:
            print(UI.section_title("Project Name"))
            print(UI.key_hint("Enter", "Type your project name"))
            project_name = input(f"{UI.prompt('Project name')}: ").strip()
            
            if not project_name:
                print_error(" Project name is required")
                continue
            
            # Validate project name
            if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
                print_error(" Name can only contain letters, numbers, hyphens and underscores")
                continue
            
            if len(project_name) < 2:
                print_error(" Name must be at least 2 characters long")
                continue
            
            if len(project_name) > 50:
                print_error(" Name cannot be longer than 50 characters")
                continue
            
            # Check if directory already exists
            if os.path.exists(project_name):
                print_warning(f"  Directory '{project_name}' already exists")
                overwrite_options = {
                    'yes': 'Yes - Overwrite existing directory',
                    'no': 'No - Choose a different name'
                }
                overwrite_choice = self.show_menu("Do you want to overwrite it?", overwrite_options)
                if overwrite_choice == 'yes':
                    return project_name
            else:
                return project_name
    
    def show_menu(self, title, options):
        """Show an interactive menu with arrow key navigation"""
        print(UI.section_title(title))
        print(UI.key_hint("↑↓ or W/S", "Navigate") + " " + UI.key_hint("Enter", "Select") + " " + UI.key_hint("ESC", "Cancel"))
        print(UI.separator(60))
        
        option_keys = list(options.keys())
        option_descriptions = list(options.values())
        selected_index = 0
        
        def display_options():
            for i, description in enumerate(option_descriptions):
                print(UI.menu_item(description, selected=i == selected_index))
        
        # Initial display
        display_options()
        
        while True:
            key = self._get_key()
            
            if key == 'up':
                selected_index = (selected_index - 1) % len(option_keys)
                self._clear_lines(len(option_keys))
                display_options()
            elif key == 'down':
                selected_index = (selected_index + 1) % len(option_keys)
                self._clear_lines(len(option_keys))
                display_options()
            elif key == 'enter':
                print(f"\n{UI.success(f'Selected: {option_descriptions[selected_index]}')}")
                return option_keys[selected_index]
            elif key == 'esc':
                print(f"\n{UI.warning('Selection cancelled')}")
                return None
    
    def get_template_selection(self):
        """Get template selection"""
        options = {
            'basic': 'Basic - Simple web application',
            'api': 'REST API - Only API endpoints'
        }
        return self.show_menu("What type of project do you want to create?", options)
    
    def get_database_selection(self):
        """Get database selection"""
        options = {
            'sqlite': 'SQLite - Local database',
            'none': 'No Database - Static files only'
        }
        return self.show_menu("What database do you want to use?", options)
    
    def get_frontend_selection(self):
        """Get frontend framework selection"""
        # Only custom CSS option available now
        return 'none'
    
    def get_additional_features(self):
        """Simplified - no additional features for now"""
        return []
    
    def get_project_configuration(self):
        """Get complete project configuration interactively"""
        print(UI.logo())
        print(UI.header("Welcome to Flite! Let's create your Flask project", 70))
        
        # Get project name
        project_name = self.get_project_name()
        
        # Get template
        template = self.get_template_selection()
        
        # Get database
        database = self.get_database_selection()
        
        # Get frontend
        frontend = self.get_frontend_selection()
        
        # Get additional features
        features = self.get_additional_features()
        
        # Build configuration
        config = {
            'project_name': project_name,
            'project_title': project_name.replace('_', ' ').replace('-', ' ').title(),
            'template': template,
            'database': database,
            'frontend': frontend,
            'auth': 'auth' in features,
            'api': 'api' in features,
            'email': 'email' in features,
            'admin': 'admin' in features,
            'tests': 'tests' in features
        }
        
        # Show configuration summary
        self._show_configuration_summary(config)
        
        # Confirm configuration with arrow key selection
        confirm_options = {
            'yes': 'Yes - Create the project',
            'no': 'No - Cancel and exit'
        }
        
        confirm_choice = self.show_menu("Proceed with this configuration?", confirm_options)
        
        if confirm_choice == 'no' or confirm_choice is None:
            print_info("Configuration cancelled. You can try again with 'flite create'")
            return None
        
        return config
    
    def _show_configuration_summary(self, config):
        """Show configuration summary"""
        summary_content = f"""Project name: {UI.highlight(config['project_name'])}
Template type: {UI.highlight(config['template'])}
Database: {UI.highlight(config['database'])}
Frontend: {UI.highlight(config['frontend'])}"""
        
        print(UI.box(summary_content, "Configuration Summary", 50))
    
    def get_run_options(self):
        """Get run options interactively"""
        print(UI.section_title("Run Options"))
        
        host = input(f"{UI.prompt('Host (Enter for 127.0.0.1)')}: ").strip() or '127.0.0.1'
        
        while True:
            port_input = input(f"{UI.prompt('Port (Enter for 5000)')}: ").strip() or '5000'
            try:
                port = int(port_input)
                if 1 <= port <= 65535:
                    break
                else:
                    print_error("Port must be between 1 and 65535")
            except ValueError:
                print_error("Port must be a valid number")
        
        debug_options = {
            'yes': 'Yes - Enable debug mode',
            'no': 'No - Production mode'
        }
        debug_choice = self.show_menu("Run in debug mode?", debug_options)
        debug = debug_choice == 'yes'
        
        return {
            'host': host,
            'port': port,
            'debug': debug
        }
    
    def show_project_created_message(self, project_name, project_path):
        """Show project created success message"""
        success_content = f"""Project: {UI.highlight(project_name)}
Location: {UI.highlight(os.path.abspath(project_path))}

Next Steps:
  1. cd {project_name}
  2. flite run
  3. Visit http://127.0.0.1:5000

Virtual Environment:
  Created as .venv/ (hidden folder)

Useful Commands:
  flite run --debug    # Run in debug mode
  flite build          # Build for production  
  flite --help         # See all commands"""
        
        print(f"\n{UI.success('Project created successfully!')}")
        print(UI.box(success_content, "Project Ready!", 50))
