#!/usr/bin/env python3
"""
Flite CLI - Main command line interface
"""

import click
import os
import sys
import subprocess
from pathlib import Path
from .generator import ProjectGenerator
from .utils import print_success, print_error, print_info, print_warning
from .simple_interactive import SimpleInteractiveMode as InteractiveMode

@click.group()
@click.version_option(version="1.0.1")
def main():
    """Flite - Flask Project Generator
    
    A CLI tool to generate Flask projects automatically.
    
    To get started, use: flite interactive
    """
    pass

@main.command()
@click.argument('project_name', required=False)
@click.option('--template', '-t', default='basic', help='Template to use (basic, api, full)')
@click.option('--database', '-d', default='sqlite', help='Database type (sqlite, postgresql, mysql)')
@click.option('--auth', '-a', is_flag=True, help='Include authentication system')
@click.option('--api', is_flag=True, help='Include API endpoints')
@click.option('--frontend', '-f', default='bootstrap', help='Frontend framework (bootstrap, tailwind, none)')
@click.option('--interactive', '-i', is_flag=True, help='Use interactive mode')
def create(project_name, template, database, auth, api, frontend, interactive):
    """Create a new Flask project"""
    try:
        generator = ProjectGenerator()
        
        if interactive or not project_name:
            # Use interactive mode
            interactive_mode = InteractiveMode()
            config = interactive_mode.get_project_configuration()
            
            if not config:
                return
            
            generator.create_project(
                project_name=config['project_name'],
                template=config['template'],
                database=config['database'],
                auth=config['auth'],
                api=config['api'],
                frontend=config['frontend']
            )
            
            interactive_mode.show_project_created_message(
                config['project_name'], 
                config['project_name']
            )
        else:
            # Use command line arguments
            generator.create_project(
                project_name=project_name,
                template=template,
                database=database,
                auth=auth,
                api=api,
                frontend=frontend
            )
            print_success(f"Project '{project_name}' created successfully!")
            print_info(f"Location: {os.path.abspath(project_name)}")
            print_info("To run the project:")
            print_info(f"   cd {project_name}")
            print_info("   flite run")
    except Exception as e:
        print_error(f" Error creating project: {str(e)}")
        sys.exit(1)

@main.command()
@click.option('--host', default='127.0.0.1', help='Host to run on')
@click.option('--port', default=5000, help='Port to run on')
@click.option('--debug', is_flag=True, help='Run in debug mode')
@click.option('--interactive', '-i', is_flag=True, help='Use interactive mode')
def run(host, port, debug, interactive):
    """Run the current Flask project"""
    try:
        if not os.path.exists('run.py'):
            print_error(" run.py not found. Make sure you're in a valid Flask project.")
            sys.exit(1)
        
        if interactive:
            # Use interactive mode for run options
            interactive_mode = InteractiveMode()
            run_options = interactive_mode.get_run_options()
            
            if run_options:
                host = run_options['host']
                port = run_options['port']
                debug = run_options['debug']
        
        print_info(f"Starting Flask server at http://{host}:{port}")
        print_info("Press Ctrl+C to stop the server")
        
        # Detect and use .venv automatically
        if os.name == 'nt':  # Windows
            python_cmd = os.path.join('.venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/Mac
            python_cmd = os.path.join('.venv', 'bin', 'python')
        
        # Fallback to system python if .venv doesn't exist
        if not os.path.exists(python_cmd):
            python_cmd = "python"
            print_warning(".venv not found, using system Python")
        else:
            from .colors import Colors
            print_info(f"Using virtual environment {Colors.BRIGHT_GREEN}(.venv){Colors.BRIGHT_CYAN} Python")
        
        # Build command with venv python
        cmd = [python_cmd, "run.py", f"--host={host}", f"--port={port}"]
        if debug:
            cmd.append("--debug")
        
        subprocess.run(cmd, shell=False)
    except Exception as e:
        print_error(f" Error running project: {str(e)}")
        sys.exit(1)

@main.command()
def build():
    """Build the project for production"""
    try:
        print_info("Building project for production...")
        
        # Verify we're in a valid project
        if not os.path.exists('requirements.txt'):
            print_error(" requirements.txt not found. Make sure you're in a valid Flask project.")
            sys.exit(1)
        
        # Create production file
        with open('wsgi.py', 'w') as f:
            f.write("""from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
""")
        
        print_success("Project built for production!")
        print_info("wsgi.py file created")
        print_info("To deploy to production, use a WSGI server like Gunicorn")
    except Exception as e:
        print_error(f" Error building project: {str(e)}")
        sys.exit(1)

@main.command()
def init():
    """Initialize a Flask project in the current directory"""
    try:
        if os.path.exists('app') or os.path.exists('run.py'):
            print_warning("A Flask project already exists in this directory")
            if not click.confirm("Continue anyway?"):
                return
        
        generator = ProjectGenerator()
        generator.init_project()
        print_success("Flask project initialized in current directory!")
    except Exception as e:
        print_error(f" Error initializing project: {str(e)}")
        sys.exit(1)

@main.command()
def interactive():
    """Interactive mode - Create project with dropdown menus"""
    try:
        interactive_mode = InteractiveMode()
        config = interactive_mode.get_project_configuration()
        
        if not config:
            return
        
        generator = ProjectGenerator()
        generator.create_project(
            project_name=config['project_name'],
            template=config['template'],
            database=config['database'],
            auth=config['auth'],
            api=config['api'],
            frontend=config['frontend']
        )
        
        interactive_mode.show_project_created_message(
            config['project_name'], 
            config['project_name']
        )
    except Exception as e:
        print_error(f" Error creating project: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
