# Python Boilerplate

## Overview

This is a Python boilerplate project that provides a well-structured foundation for building Python applications. It includes a modular architecture with configuration management, logging utilities, and a CLI interface using Click.

### Requirements

* Python 3.10+
* Poetry or Pip for dependency installation

Tested with:
* Python 3.12.8

### Setup

Clone the repository and change to directory.

   ```bash
   git clone <your-repo-url>
   cd python-boilerplate
   ```

(Recommended) Use a Python virtual environment. Pyenv example:

  ```bash
  pyenv virtualenv 3.12.8 python-boilerplate
  pyenv local python-boilerplate
  pyenv activate python-boilerplate
  ```

#### Poetry

Install dependencies via Poetry.

   ```bash
   poetry install
   ```

#### Pip

Install dependencies via Pip.

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

- **VERBOSE**: When set to `True` in `config.yml`, all `DEBUG` logs will be sent to the console. If set to `False`, only `INFO` and higher levels will be shown.

```yaml
VERBOSE: True # Set to False for higher log levels (INFO and above)
```

Refer to [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#custom-handling-of-levels) for more information on customizing logging behavior.

### Execution

Run the application using the CLI:

```bash
python main.py app-test
```

This will execute the test command defined in the CLI module.

### Project Structure

```
python-boilerplate/
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