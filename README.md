# Flite - Flask Project Generator

🚀 **Flite** is a CLI tool that generates Flask projects automatically. Creates projects with modern structure, automatic configuration, and production-ready setup.

## ✨ Features

- 🏗️ Generates Flask projects with professional structure
- ⚙️ Automatic virtual environment configuration
- 📦 Pre-configured dependencies
- 🎨 Modern HTML/CSS/JS templates
- 🔧 Automatic environment variables
- 📁 Standard folder structure
- 🚀 Commands for development and production
- 🗄️ Support for SQLite database or no database

## 🚀 Installation

### Install from source

```bash
# Clone the repository
git clone https://github.com/artbyo3/flite.git
cd flite

# Install in development mode
pip install -e .
```

### Install with pip (when available on PyPI)

```bash
pip install flite
```

## 📖 Usage

### Interactive mode (recommended)

```bash
flite interactive
# or simply
flite create
```

### Command line mode

```bash
# Basic project
flite create my-project --template basic --database sqlite

# REST API project  
flite create my-project --template api --database none

# Run project
cd my-project
flite run

# Build for production
flite build
```

## 🏗️ Generated structure

### Basic template
```
my-project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── routes.py            # Main routes (index only)
│   ├── static/
│   │   ├── css/style.css    # Minimal custom styles
│   │   └── js/main.js       # Minimal custom JavaScript
│   └── templates/
│       ├── base.html        # Base template
│       └── index.html       # Simple page with "Flite"
├── .venv/                   # Virtual environment (hidden)
├── .env                     # Environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── config.py               # Application configuration
└── run.py                  # Execution script
```

### API template
```
my-project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── routes.py            # API endpoints
│   └── templates/
│       └── index.html       # API documentation page
├── .venv/                   # Virtual environment (hidden)
├── .env                     # Environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── config.py               # Application configuration
└── run.py                  # Execution script
```

## 🛠️ Technologies included

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM (when database enabled)
- **Flask-Migrate** - Database migrations (when database enabled)

### Frontend
- **HTML5** - Semantic structure
- **CSS3** - Modern styles
- **JavaScript** - Basic interactivity

### Database
- **SQLite** - Local database (optional)
- **No Database** - Static files only

## 🚀 Examples

### Basic web application
```bash
flite create my-blog --template basic --database sqlite
cd my-blog
flite run
# Visit http://127.0.0.1:5000
```

### REST API
```bash
flite create my-api --template api --database none
cd my-api
flite run
# Visit http://127.0.0.1:5000 for API documentation
```

## 🔧 Configuration

### Environment variables

The `.env` file is generated automatically with basic configuration:

```env
# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database configuration (if enabled)
DATABASE_URL=sqlite:///app.db
```

### Customization

You can customize your project by editing:
- `config.py` - Application configuration
- `app/static/css/style.css` - Custom styles
- `app/static/js/main.js` - Custom JavaScript
- `app/templates/` - HTML templates

## 🚀 Deployment

### Development
```bash
flite run --debug
```

### Production
```bash
# Build for production
flite build

# Use with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is under the MIT License. See the `LICENSE` file for more details.

## 🙏 Acknowledgments

- Flask team for the excellent framework
- Python community for the amazing libraries