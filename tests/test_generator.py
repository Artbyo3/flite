"""
Tests for ProjectGenerator class
"""
import pytest
import os
from flite.generator import ProjectGenerator
from .test_base import TestBase

class TestProjectGenerator(TestBase):
    """Test ProjectGenerator functionality"""
    
    def test_init(self):
        """Test ProjectGenerator initialization"""
        generator = ProjectGenerator()
        assert generator.templates_dir is not None
        assert generator.default_port == 5000
        assert generator.default_host == '127.0.0.1'
        assert generator.default_debug == True
    
    def test_validate_project_name(self):
        """Test project name validation"""
        generator = ProjectGenerator()
        
        # Valid names
        assert generator._validate_project_name('valid_project') == True
        assert generator._validate_project_name('valid-project') == True
        assert generator._validate_project_name('valid123') == True
        assert generator._validate_project_name('valid_project_123') == True
        
        # Invalid names
        assert generator._validate_project_name('123invalid') == False
        assert generator._validate_project_name('invalid name') == False
        assert generator._validate_project_name('invalid@name') == False
        assert generator._validate_project_name('') == False
        assert generator._validate_project_name('   ') == False
    
    def test_validate_template(self):
        """Test template validation"""
        generator = ProjectGenerator()
        
        # Valid templates
        assert generator._validate_template('basic') == True
        assert generator._validate_template('api') == True
        
        # Invalid templates
        assert generator._validate_template('invalid') == False
        assert generator._validate_template('') == False
    
    def test_validate_database(self):
        """Test database validation"""
        generator = ProjectGenerator()
        
        # Valid databases
        assert generator._validate_database('sqlite') == True
        assert generator._validate_database('postgresql') == True
        assert generator._validate_database('mysql') == True
        assert generator._validate_database('none') == True
        
        # Invalid databases
        assert generator._validate_database('invalid') == False
        assert generator._validate_database('') == False
    
    def test_validate_frontend(self):
        """Test frontend validation"""
        generator = ProjectGenerator()
        
        # Valid frontends
        assert generator._validate_frontend('bootstrap') == True
        assert generator._validate_frontend('tailwind') == True
        assert generator._validate_frontend('none') == True
        
        # Invalid frontends
        assert generator._validate_frontend('invalid') == False
        assert generator._validate_frontend('') == False
    
    def test_get_database_url(self):
        """Test database URL generation"""
        generator = ProjectGenerator()
        
        assert generator._get_database_url('sqlite') == 'sqlite:///app.db'
        assert generator._get_database_url('postgresql') == 'postgresql://user:password@localhost/dbname'
        assert generator._get_database_url('mysql') == 'mysql://user:password@localhost/dbname'
        assert generator._get_database_url('none') == ''
        assert generator._get_database_url('invalid') == 'sqlite:///app.db'  # Default fallback
    
    def test_generate_secret_key(self):
        """Test secret key generation"""
        generator = ProjectGenerator()
        
        key1 = generator._generate_secret_key()
        key2 = generator._generate_secret_key()
        
        assert len(key1) == 50
        assert len(key2) == 50
        assert key1 != key2  # Should be different each time
    
    def test_create_directory_structure(self):
        """Test directory structure creation"""
        generator = ProjectGenerator()
        generator._create_directory_structure()
        
        self.assert_directory_exists('app')
        self.assert_directory_exists('app/static')
        self.assert_directory_exists('app/static/css')
        self.assert_directory_exists('app/static/js')
        self.assert_directory_exists('app/static/images')
        self.assert_directory_exists('app/templates')
    
    def test_generate_files_basic(self):
        """Test basic file generation"""
        generator = ProjectGenerator()
        config = {
            'project_name': 'test_project',
            'project_title': 'Test Project',
            'template': 'basic',
            'database': 'sqlite',
            'auth': False,
            'api': False,
            'frontend': 'bootstrap'
        }
        
        generator._create_directory_structure()
        generator._generate_files('test_project', 'basic', 'sqlite', False, False, 'bootstrap')
        
        # Check main files
        self.assert_file_exists('app/__init__.py')
        self.assert_file_exists('app/routes.py')
        self.assert_file_exists('config.py')
        self.assert_file_exists('run.py')
        self.assert_file_exists('requirements.txt')
        self.assert_file_exists('.env')
        self.assert_file_exists('.gitignore')
        
        # Check templates
        self.assert_file_exists('app/templates/base.html')
        self.assert_file_exists('app/templates/index.html')
        
        # Check static files
        self.assert_file_exists('app/static/css/style.css')
        self.assert_file_exists('app/static/js/main.js')
    
    def test_generate_files_api(self):
        """Test API file generation"""
        generator = ProjectGenerator()
        config = {
            'project_name': 'test_api',
            'project_title': 'Test API',
            'template': 'api',
            'database': 'sqlite',
            'auth': False,
            'api': True,
            'frontend': 'none'
        }
        
        generator._create_directory_structure()
        generator._generate_files('test_api', 'api', 'sqlite', False, True, 'none')
        
        # Check API files
        self.assert_file_exists('app/api_routes.py')
        self.assert_file_exists('app/api_models.py')
        
        # Check requirements include API dependencies
        self.assert_file_contains('requirements.txt', 'Flask-RESTful')
        self.assert_file_contains('requirements.txt', 'Flask-CORS')
    
    def test_generate_files_auth(self):
        """Test auth file generation"""
        generator = ProjectGenerator()
        
        generator._create_directory_structure()
        generator._generate_files('test_auth', 'basic', 'sqlite', True, False, 'bootstrap')
        
        # Check auth files
        self.assert_file_exists('app/models.py')
        self.assert_file_exists('app/auth_routes.py')
        
        # Check requirements include auth dependencies
        self.assert_file_contains('requirements.txt', 'Flask-Login')
    
    def test_generate_requirements(self):
        """Test requirements.txt generation"""
        generator = ProjectGenerator()
        
        # Test basic requirements
        config = {'database': 'none', 'auth': False, 'api': False}
        generator._generate_requirements(config)
        self.assert_file_exists('requirements.txt')
        self.assert_file_contains('requirements.txt', 'Flask>=2.3.0')
        
        # Test with database
        config = {'database': 'sqlite', 'auth': False, 'api': False}
        generator._generate_requirements(config)
        self.assert_file_contains('requirements.txt', 'Flask-SQLAlchemy')
        self.assert_file_contains('requirements.txt', 'Flask-Migrate')
        
        # Test with PostgreSQL
        config = {'database': 'postgresql', 'auth': False, 'api': False}
        generator._generate_requirements(config)
        self.assert_file_contains('requirements.txt', 'psycopg2-binary')
        
        # Test with MySQL
        config = {'database': 'mysql', 'auth': False, 'api': False}
        generator._generate_requirements(config)
        self.assert_file_contains('requirements.txt', 'PyMySQL')
    
    def test_generate_env_file(self):
        """Test .env file generation"""
        generator = ProjectGenerator()
        
        # Test with database
        config = {'project_title': 'Test Project', 'database': 'sqlite'}
        generator._generate_env_file(config)
        self.assert_file_exists('.env')
        self.assert_file_contains('.env', 'FLASK_APP=run.py')
        self.assert_file_contains('.env', 'SECRET_KEY=')
        self.assert_file_contains('.env', 'DATABASE_URL=')
        
        # Test without database
        config = {'project_title': 'Test Project', 'database': 'none'}
        generator._generate_env_file(config)
        self.assert_file_exists('.env')
        self.assert_file_contains('.env', 'FLASK_APP=run.py')
        self.assert_file_contains('.env', 'SECRET_KEY=')
        # Should not contain DATABASE_URL
        with open('.env', 'r') as f:
            content = f.read()
            assert 'DATABASE_URL' not in content
