# Flite CLI Commands Reference

## Overview
Flite is a CLI tool to generate Flask projects automatically. It provides both interactive and command-line modes for creating Flask applications.

## Installation Commands

### Install Flite
```bash
pip install flite
```

### Install from Source
```bash
git clone <repository-url>
cd flite
pip install -e .
```

## Main Commands

### 1. `flite --help`
**Description:** Show help information and available commands
**Usage:** `flite --help`

### 2. `flite --version`
**Description:** Show Flite version
**Usage:** `flite --version`

## Project Creation Commands

### 3. `flite create [PROJECT_NAME]`
**Description:** Create a new Flask project
**Usage:** `flite create myproject`

#### Options:
- `--template, -t` - Template to use (default: 'basic')
  - Options: `basic`, `api`
- `--database, -d` - Database type (default: 'sqlite')
  - Options: `sqlite`, `postgresql`, `mysql`, `none`
- `--auth, -a` - Include authentication system (flag)
- `--api` - Include API endpoints (flag)
- `--frontend, -f` - Frontend framework (default: 'bootstrap')
  - Options: `bootstrap`, `tailwind`, `none`
- `--interactive, -i` - Use interactive mode (flag)

#### Examples:
```bash
# Basic project
flite create myapp

# API project with PostgreSQL
flite create myapi --template api --database postgresql --api

# Project with authentication and Bootstrap
flite create mywebapp --auth --frontend bootstrap

# Interactive mode
flite create --interactive
flite create -i
```

### 4. `flite interactive`
**Description:** Interactive mode - Create project with dropdown menus
**Usage:** `flite interactive`

**Features:**
- Visual menu navigation
- Project name input
- Template selection (Basic, API)
- Database selection (SQLite, No Database)
- Frontend selection (Custom CSS)
- Configuration summary
- Confirmation before creation

## Project Management Commands

### 5. `flite run`
**Description:** Run the current Flask project
**Usage:** `flite run`

#### Options:
- `--host` - Host to run on (default: '127.0.0.1')
- `--port` - Port to run on (default: 5000)
- `--debug` - Run in debug mode (flag)
- `--interactive, -i` - Use interactive mode for run options (flag)

#### Examples:
```bash
# Run with default settings
flite run

# Run on specific host and port
flite run --host 0.0.0.0 --port 8080

# Run in debug mode
flite run --debug

# Interactive run options
flite run --interactive
```

### 6. `flite build`
**Description:** Build the project for production
**Usage:** `flite build`

**What it does:**
- Creates `wsgi.py` file for production deployment
- Validates project structure
- Provides deployment instructions

### 7. `flite init`
**Description:** Initialize a Flask project in the current directory
**Usage:** `flite init`

**What it does:**
- Creates Flask project structure in current directory
- Uses current directory name as project name
- Validates directory name
- Asks for confirmation if project already exists

## Interactive Mode Features

### Navigation Controls
- **Arrow Keys** or **W/S**: Navigate up/down
- **Enter**: Select option
- **Space**: Toggle checkbox
- **ESC**: Cancel/exit

### Configuration Options

#### Project Name
- Input validation (letters, numbers, hyphens, underscores only)
- Cannot start with numbers
- Cannot be empty

#### Template Types
- **Basic**: Standard web application with templates
- **API**: REST API with JSON responses

#### Database Options
- **SQLite**: Local file database (default)
- **No Database**: Static files only

#### Frontend Options
- **Custom CSS**: Basic styling (default)
- **Bootstrap**: Bootstrap framework (planned)
- **Tailwind**: Tailwind CSS (planned)

#### Additional Features (Planned)
- Authentication system
- API endpoints
- Email functionality
- Admin panel
- Testing framework

## Generated Project Structure

### Basic Template
```
project_name/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       └── index.html
├── .env
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── .venv/
```

### API Template
```
project_name/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── api_models.py
│   ├── api_routes.py
│   └── templates/
│       └── index.html
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Dependencies

### Core Dependencies
- Flask>=2.3.0
- python-dotenv>=1.0.0
- Werkzeug>=2.3.0

### Database Dependencies (if enabled)
- Flask-SQLAlchemy>=3.0.0
- Flask-Migrate>=4.0.0
- psycopg2-binary>=2.9.0 (PostgreSQL)
- PyMySQL>=1.0.0 (MySQL)

### Authentication Dependencies (if enabled)
- Flask-Login>=0.6.0

### API Dependencies (if enabled)
- Flask-RESTful>=0.3.10
- Flask-CORS>=4.0.0

## Environment Variables

### Generated .env File
```env
# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=<generated-secret-key>

# Database configuration (if enabled)
DATABASE_URL=sqlite:///app.db
```

## Error Handling

### Common Error Messages
- `❌ Directory 'project_name' already exists`
- `❌ Invalid project name. Use only letters, numbers, hyphens, and underscores.`
- `❌ Invalid template. Use 'basic' or 'api'.`
- `❌ Invalid database. Use 'sqlite', 'postgresql', 'mysql', or 'none'.`
- `❌ Invalid frontend. Use 'bootstrap', 'tailwind', or 'none'.`
- `❌ Permission denied creating directory`
- `❌ run.py not found. Make sure you're in a valid Flask project.`
- `❌ requirements.txt not found. Make sure you're in a valid Flask project.`

### Cleanup on Failure
- Automatic cleanup of created directories if project generation fails
- Warning messages if cleanup fails

## Tips and Best Practices

### Project Naming
- Use lowercase letters, numbers, hyphens, and underscores
- Don't start with numbers
- Avoid special characters and spaces

### Development Workflow
1. Create project: `flite create myproject`
2. Navigate to project: `cd myproject`
3. Run development server: `flite run`
4. Build for production: `flite build`

### Production Deployment
- Use `flite build` to create production files
- Deploy using WSGI servers like Gunicorn
- Set proper environment variables for production

## Troubleshooting

### Virtual Environment Issues
- Flite automatically creates and uses `.venv`
- If `.venv` not found, falls back to system Python
- Warning message displayed when using system Python

### Permission Issues
- Ensure write permissions in target directory
- Run with appropriate user permissions

### Project Validation
- All inputs are validated before processing
- Clear error messages for invalid inputs
- Automatic cleanup on failure

## Version Information
- Current Version: 1.0.1
- Python Requirements: >=3.8
- Supported Platforms: Windows, macOS, Linux
