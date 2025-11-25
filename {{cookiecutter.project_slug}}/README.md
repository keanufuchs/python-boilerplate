# {{ cookiecutter.project_name }}

## Overview

{{ cookiecutter.project_short_description }}

### Requirements

* Python {{ cookiecutter.python_version }}+
* Pip for dependency installation
{% if cookiecutter.use_pyenv == "yes" -%}
* pyenv (recommended for virtual environment management)
{% endif %}

### Setup

Clone the repository and change to directory.

```bash
git clone <your-repo-url>
cd {{ cookiecutter.project_slug }}
```

{% if cookiecutter.use_pyenv == "yes" -%}
(Recommended) This project uses pyenv for Python version management. A `.python-version` file has been created with the virtualenv name `{{ cookiecutter.project_slug }}`.

If you have pyenv installed, the virtualenv should already be created. Activate it:

```bash
pyenv activate {{ cookiecutter.project_slug }}
```

If not created, run:

```bash
pyenv install {{ cookiecutter.python_version }}
pyenv virtualenv {{ cookiecutter.python_version }} {{ cookiecutter.project_slug }}
pyenv local {{ cookiecutter.project_slug }}
```
{% else -%}
(Recommended) Use a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
{% endif %}

#### Install dependencies

Install dependencies via Pip:

```bash
pip install -r requirements.txt
```

### Configuration

#### Application Configuration

All application-related configurations are handled through the `app/config/config.yml` file. This file uses Pydantic for configuration management and supports:

- Environment variables via `.env` files
- YAML-based configuration
- Type validation and settings

#### Logging Configuration

All configuration related to logging is set in `app/config/logging.json`. The application supports:

- **VERBOSE**: When set to `{{ cookiecutter.verbose_logging }}` in `config.yml`, all `DEBUG` logs will be sent to the console. If set to `False`, only `INFO` and higher levels will be shown.

```yaml
VERBOSE: {{ cookiecutter.verbose_logging }} # Set to False for higher log levels (INFO and above)
```

### Execution

Run the application using the CLI:

```bash
python main.py app-test
```

### Project Structure

```
{{ cookiecutter.project_slug }}/
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
└── README.md
```

### Features

- **Modular Architecture**: Clean separation of concerns with organized modules
- **Configuration Management**: Pydantic-based configuration with YAML support
- **Logging**: Comprehensive logging with JSON-based configuration
- **CLI Interface**: Click-based command-line interface
- **Type Safety**: Type hints and Pydantic validation

### Logs

Logs are automatically generated and stored in `logs/app.log`. Verbose logging can be controlled with the `VERBOSE` flag in the `config.yml`.

---

## Development

### Adding New Commands

To add new CLI commands, edit `app/cli.py`:

```python
@cli.command()
def your_command():
    """Your command description."""
    # Your implementation
    logger.info('Command executed.')
```

### Configuration

Add new configuration options to `app/config/config.yml` and define them in the `BaseConfig` class in `app/config/config.py`:

```python
class BaseConfig(BaseSettings):
    # Add your configuration fields
    YOUR_SETTING: str = "default_value"
```

---

**Author:** {{ cookiecutter.author_name }} ({{ cookiecutter.author_email }})
