"""
Project Generator for Flite CLI
"""

import os
import sys
import subprocess
from pathlib import Path
from .utils import ensure_directory, copy_template_file, print_info, print_error

class ProjectGenerator:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    def create_project(self, project_name, template='basic', database='sqlite', 
                      auth=False, api=False, frontend='bootstrap'):
        """Create a new Flask project"""
        try:
            # Create project directory
            project_path = Path(project_name)
            if project_path.exists():
                print_error(f"❌ El directorio '{project_name}' ya existe")
                sys.exit(1)
            
            project_path.mkdir()
            os.chdir(project_path)
            
            print_info(f"📁 Creating project '{project_name}'...")
            
            # Create project structure
            self._create_directory_structure()
            
            # Generate files based on template
            self._generate_files(project_name, template, database, auth, api, frontend)
            
            # Create virtual environment
            self._create_virtual_environment()
            
            # Install dependencies
            self._install_dependencies()
            
            print_info("✅ Project created successfully!")
            
        except Exception as e:
            print_error(f"❌ Error creating project: {str(e)}")
            raise
    
    def init_project(self):
        """Initialize Flask project in current directory"""
        try:
            print_info("📁 Initializing Flask project in current directory...")
            
            # Create project structure
            self._create_directory_structure()
            
            # Generate basic files
            self._generate_files("myapp", "basic", "sqlite", False, False, "bootstrap")
            
            print_info("✅ Project initialized successfully!")
            
        except Exception as e:
            print_error(f"❌ Error initializing project: {str(e)}")
            raise
    
    def _create_directory_structure(self):
        """Create the minimal Flask project directory structure"""
        directories = [
            'app',
            'app/static/css',
            'app/static/js',
            'app/static/images',
            'app/templates'
        ]
        
        for directory in directories:
            ensure_directory(directory)
    
    def _generate_files(self, project_name, template, database, auth, api, frontend):
        """Generate all project files"""
        
        # Project configuration
        config = {
            'project_name': project_name,
            'project_title': project_name.replace('_', ' ').title(),
            'template': template,
            'database': database,
            'auth': auth,
            'api': api,
            'frontend': frontend
        }
        
        # Generate main application files
        self._generate_app_init(config)
        self._generate_routes(config)
        self._generate_config(config)
        self._generate_run_file(config)
        self._generate_requirements(config)
        self._generate_env_file(config)
        self._generate_gitignore()
        
        # Generate templates based on template type
        if config['template'] == 'basic':
            self._generate_basic_templates(config)
        else:
            self._generate_api_templates(config)
        
        # Generate static files based on template type
        if config['template'] == 'basic':
            self._generate_minimal_static_files(config)
        else:
            # API projects don't need static files
            pass
        
        # Generate additional files based on options
        if auth:
            self._generate_auth_files(config)
        
        if api:
            self._generate_api_files(config)
    
    def _generate_app_init(self, config):
        """Generate app/__init__.py"""
        
        # Check if database is enabled
        has_database = config['database'] != 'none'
        
        if has_database:
            content = f'''"""
{config['project_title']} - Flask Application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
'''
        else:
            content = f'''"""
{config['project_title']} - Flask Application
"""

from flask import Flask
from config import Config

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
'''
        
        with open('app/__init__.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_routes(self, config):
        """Generate app/routes.py"""
        
        # Check if template is basic or API
        if config['template'] == 'basic':
            # Super minimal basic web application
            content = f'''"""
Main routes for {config['project_title']}
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')
'''
        else:
            # API template with more functionality
            has_database = config['database'] != 'none'
            
            if has_database:
                content = f'''"""
API routes for {config['project_title']}
"""

from flask import Blueprint, jsonify, request
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """API root endpoint"""
    return jsonify({{'message': 'Welcome to {config['project_title']} API', 'version': '1.0.0'}})

@main_bp.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({{'status': 'ok', 'message': 'API is running'}})
'''
            else:
                content = f'''"""
API routes for {config['project_title']}
"""

from flask import Blueprint, jsonify, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """API root endpoint"""
    return jsonify({{'message': 'Welcome to {config['project_title']} API', 'version': '1.0.0'}})

@main_bp.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({{'status': 'ok', 'message': 'API is running'}})
'''
        
        with open('app/routes.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_config(self, config):
        """Generate config.py"""
        
        # Check if database is enabled
        has_database = config['database'] != 'none'
        
        if has_database:
            database_urls = {
                'sqlite': 'sqlite:///app.db',
                'postgresql': 'postgresql://user:password@localhost/dbname',
                'mysql': 'mysql://user:password@localhost/dbname'
            }
            database_url = database_urls.get(config['database'], 'sqlite:///app.db')
            
            content = f'''"""
Configuration settings for {config['project_title']}
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or '{database_url}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {{
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}}
'''
        else:
            # No database configuration
            content = f'''"""
Configuration settings for {config['project_title']}
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {{
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}}
'''
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_run_file(self, config):
        """Generate run.py"""
        
        # Check if database is enabled
        has_database = config['database'] != 'none'
        
        if has_database:
            content = f'''"""
Run script for {config['project_title']}
"""

from app import create_app
from app import db

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")

if __name__ == '__main__':
    import sys
    
    # Parse command line arguments
    host = '127.0.0.1'
    port = 5000
    debug = False
    
    if '--host' in sys.argv:
        host = sys.argv[sys.argv.index('--host') + 1]
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    if '--debug' in sys.argv:
        debug = True
    
    app.run(host=host, port=port, debug=debug)
'''
        else:
            # No database version
            content = f'''"""
Run script for {config['project_title']}
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    import sys
    
    # Parse command line arguments
    host = '127.0.0.1'
    port = 5000
    debug = False
    
    if '--host' in sys.argv:
        host = sys.argv[sys.argv.index('--host') + 1]
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    if '--debug' in sys.argv:
        debug = True
    
    app.run(host=host, port=port, debug=debug)
'''
        
        with open('run.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_requirements(self, config):
        """Generate requirements.txt"""
        requirements = [
            'Flask>=2.3.0',
            'python-dotenv>=1.0.0',
            'Werkzeug>=2.3.0'
        ]
        
        # Add database dependencies only if database is enabled
        if config['database'] != 'none':
            requirements.extend([
                'Flask-SQLAlchemy>=3.0.0',
                'Flask-Migrate>=4.0.0'
            ])
        
        # Add specific database drivers
        if config['database'] == 'postgresql':
            requirements.append('psycopg2-binary>=2.9.0')
        elif config['database'] == 'mysql':
            requirements.append('PyMySQL>=1.0.0')
        
        content = '\n'.join(requirements)
        
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_env_file(self, config):
        """Generate .env file"""
        
        # Check if database is enabled
        has_database = config['database'] != 'none'
        
        if has_database:
            content = f'''# Environment variables for {config['project_title']}

# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database configuration
DATABASE_URL={self._get_database_url(config['database'])}
'''
        else:
            content = f'''# Environment variables for {config['project_title']}

# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
'''
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_database_url(self, database):
        """Get database URL based on type"""
        urls = {
            'sqlite': 'sqlite:///app.db',
            'none': '',  # No database
            'postgresql': 'postgresql://user:password@localhost/dbname',
            'mysql': 'mysql://user:password@localhost/dbname'
        }
        return urls.get(database, urls['sqlite'])
    
    def _generate_gitignore(self):
        """Generate .gitignore file"""
        content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
'''
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_basic_templates(self, config):
        """Generate minimal templates for basic web app"""
        self._generate_minimal_base_template(config)
        self._generate_minimal_index_template(config)
    
    def _generate_api_templates(self, config):
        """Generate templates for API projects (minimal or none)"""
        # API projects typically don't need HTML templates
        # Just create a simple index template for documentation
        self._generate_api_index_template(config)
    
    def _generate_minimal_base_template(self, config):
        """Generate minimal base.html template"""
        content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    {{% block content %}}{{% endblock %}}
</body>
</html>
'''.format(title=config['project_title'])
        
        with open('app/templates/base.html', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_minimal_index_template(self, config):
        """Generate minimal index.html template"""
        content = '''{% extends "base.html" %}

{% block content %}
<!-- Remove from here to 'until here' comment if you don't want this page -->
<div class="container-3d" id="container3d">
    <div class="content-3d">
        <h1 class="title-3d" id="title3d">Flite</h1>
        <p class="subtitle-3d" id="subtitle3d">Flask Project Generator</p>
        <div class="status-3d">
            <h3>Project Ready</h3>
            <p>Your Flask application is running successfully</p>
        </div>
    </div>
</div>

<script>
// 3D Mouse Tracking - Remove this entire script if you don't want the 3D effect
document.addEventListener('mousemove', function(e) {
    const rect = document.getElementById('container3d').getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    const rotateX = (y / rect.height) * 30;
    const rotateY = (x / rect.width) * -30;
    
    document.getElementById('title3d').style.transform = 'rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
    document.getElementById('subtitle3d').style.transform = 'rotateX(' + (rotateX * 0.7) + 'deg) rotateY(' + (rotateY * 0.7) + 'deg)';
    document.querySelector('.status-3d').style.transform = 'rotateX(' + (rotateX * 0.3) + 'deg) rotateY(' + (rotateY * 0.3) + 'deg)';
});
</script>
<!--until here-->

{% endblock %}
'''
        
        with open('app/templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_api_index_template(self, config):
        """Generate minimal template for API projects"""
        content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['project_title']} API</title>
    <style>
        body {{
            font-family: monospace;
            margin: 0;
            padding: 40px;
            background-color: #1e1e1e;
            color: #d4d4d4;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
        }}
        .code {{
            background: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{config['project_title']} API</h1>
        <p>REST API generated with Flite CLI</p>
        <div class="code">
            <p>GET / - API root</p>
            <p>GET /api/health - Health check</p>
        </div>
        <p>Built with Flite CLI by Artbyo3</p>
    </div>
</body>
</html>
'''
        
        with open('app/templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
    
    
    
    
    
    def _generate_minimal_static_files(self, config):
        """Generate minimal static files for basic projects"""
        # Create empty directories for user to add their own files
        ensure_directory('app/static/css')
        ensure_directory('app/static/js')
        ensure_directory('app/static/images')
        
        # Create fire 3D CSS
        css_content = '''/* Flite style.css */

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: radial-gradient(circle, #ff4500 0%, #ff6b35 25%, #ff8c00 50%, #ff1744 100%);
    min-height: 100vh;
    color: #fff;
    overflow: hidden;
    perspective: 1000px;
}

.container-3d {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px;
}

.content-3d {
    text-align: center;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
}

.title-3d {
    font-size: 6rem;
    font-weight: 900;
    background: linear-gradient(45deg, #ff4500, #ff6b35, #ffff00, #ff8c00, #ff4500);
    background-size: 300% 300%;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fire-gradient 3s infinite;
    text-shadow: 0 0 30px rgba(255, 69, 0, 0.8), 0 0 60px rgba(255, 140, 0, 0.6);
    margin-bottom: 20px;
    letter-spacing: 10px;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
}

.subtitle-3d {
    font-size: 1.8rem;
    color: #ffff00;
    margin-bottom: 40px;
    text-shadow: 0 0 20px #ff8c00, 0 0 40px #ff4500;
    font-weight: 300;
    letter-spacing: 3px;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
}

.status-3d {
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid #ff6b35;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 0 30px rgba(255, 107, 53, 0.4);
    max-width: 500px;
    margin: 0 auto;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
}

.status-3d h3 {
    color: #ffff00;
    font-size: 1.5rem;
    margin-bottom: 15px;
    text-shadow: 0 0 15px #ff8c00;
    font-weight: 600;
}

.status-3d p {
    color: #ffcc99;
    font-size: 1.1rem;
    line-height: 1.4;
}

@keyframes fire-gradient {
    0%, 100% { background-position: 0% 50%; filter: hue-rotate(0deg); }
    25% { background-position: 50% 0%; filter: hue-rotate(10deg); }
    50% { background-position: 100% 50%; filter: hue-rotate(20deg); }
    75% { background-position: 50% 100%; filter: hue-rotate(10deg); }
}

@media (max-width: 768px) {
    .title-3d { font-size: 4rem; letter-spacing: 5px; }
    .subtitle-3d { font-size: 1.3rem; letter-spacing: 2px; }
    .status-3d { padding: 20px; margin: 20px; }
}

/* Add your custom CSS here */
'''
        with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Create a minimal JS file
        js_content = '''// Custom JavaScript for your Flask app

// Add your custom JavaScript here
console.log('Flask app loaded');
'''
        with open('app/static/js/main.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    
    
    
    def _generate_auth_files(self, config):
        """Generate authentication related files"""
        # This would include user models, auth routes, login templates, etc.
        pass
    
    def _generate_api_files(self, config):
        """Generate API related files"""
        # This would include API routes, serializers, etc.
        pass
    
    def _create_virtual_environment(self):
        """Create virtual environment"""
        try:
            print_info("Creating virtual environment...")
            # Use shell=True and capture output to prevent new window
            result = subprocess.run(
                [sys.executable, '-m', 'venv', '.venv'], 
                check=True, 
                capture_output=True, 
                text=True,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            print_info("Virtual environment created")
        except subprocess.CalledProcessError as e:
            print_error(f"Error creating virtual environment: {e.stderr if e.stderr else str(e)}")
            raise
    
    def _install_dependencies(self):
        """Install project dependencies"""
        try:
            print_info("Installing dependencies...")
            
            # Determine the correct pip command based on OS
            if os.name == 'nt':  # Windows
                pip_cmd = os.path.join('.venv', 'Scripts', 'pip')
            else:  # Unix/Linux/Mac
                pip_cmd = os.path.join('.venv', 'bin', 'pip')
            
            # Use capture_output and proper subprocess settings to prevent new window
            result = subprocess.run(
                [pip_cmd, 'install', '-r', 'requirements.txt'], 
                check=True, 
                capture_output=True, 
                text=True,
                shell=False,  # Don't use shell to prevent new window
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            print_info("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print_error(f"Error installing dependencies: {e.stderr if e.stderr else str(e)}")
            raise
