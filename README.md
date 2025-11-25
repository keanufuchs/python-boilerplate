# Python Boilerplate Template

A cookiecutter template for Python projects with a modular architecture, configuration management, logging utilities, and CLI interface.

## Quick Start

### Using Cookiecutter (Recommended)

Install cookiecutter:

```bash
pip install cookiecutter
```

Create a new project:

```bash
cookiecutter gh:keanufuchs/python-boilerplate
# Or locally:
cookiecutter path/to/python-boilerplate
```

You'll be prompted to enter:
- **project_name**: Your project's display name
- **project_slug**: Directory name (auto-generated from project_name)
- **project_short_description**: Brief description of your project
- **author_name**: Your name
- **author_email**: Your email address
- **python_version**: Python version to use (default: 3.10)
- **use_pyenv**: Create a pyenv virtualenv? (yes/no)
- **verbose_logging**: Enable verbose logging by default (True/False)

### Using the Setup Script (Alternative)

If you prefer not to use cookiecutter, run the included setup script:

```bash
python create_project.py
```

This will guide you through an interactive setup and create a new project directory.

---

## Features

The generated project includes:

- **Modular Architecture**: Clean separation of concerns with organized modules
- **Configuration Management**: Pydantic-based configuration with YAML support
- **Logging**: Comprehensive logging with JSON-based configuration and rotating file handlers
- **CLI Interface**: Click-based command-line interface for easy command creation
- **Type Safety**: Type hints and Pydantic validation throughout
- **Data Directories**: Pre-configured input/output/reports/static directories
- **Development Ready**: .gitignore, requirements.txt, and proper project structure

## Project Structure

The generated project will have this structure:

```
your-project/
├── app/
│   ├── __init__.py
│   ├── app.py              # Main application logic
│   ├── cli.py              # CLI commands using Click
│   ├── config/
│   │   ├── config.py       # Pydantic configuration management
│   │   ├── config.yml      # Application settings
│   │   └── logging.json    # Logging configuration
│   └── utils/
│       ├── log_utils.py    # Logging utilities
│       └── sheets_builder.py
├── data/
│   ├── input/              # Input data directory
│   ├── output/             # Output data directory
│   ├── reports/            # Reports directory
│   └── static/             # Static files
├── logs/                   # Application logs
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## After Project Creation

Once your project is created:

1. **Navigate to your project:**
   ```bash
   cd your-project-slug
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or with Poetry:
   poetry install
   ```

4. **Run the test command:**
   ```bash
   python main.py app-test
   ```

## Customizing Your Project

### Adding New CLI Commands

Edit `app/cli.py`:

```python
@cli.command()
def your_command():
    """Your command description."""
    # Your implementation
    logger.info('Command executed.')
```

### Adding Configuration Options

1. Add to `app/config/config.yml`:
   ```yaml
   YOUR_SETTING: "value"
   ```

2. Define in `app/config/config.py`:
   ```python
   class BaseConfig(BaseSettings):
       YOUR_SETTING: str = "default_value"
   ```

### Customizing Logging

Edit `app/config/logging.json` to:
- Change log levels
- Add new handlers
- Customize formatters
- Configure log rotation

## Requirements

- Python 3.10+
- cookiecutter (for template usage)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This template is available under the MIT License. See LICENSE file for details.

---

**Made with ❤️ for rapid Python project setup**
