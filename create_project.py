#!/usr/bin/env python3
"""
Quick setup script for creating a new project from this boilerplate.
Alternative to using cookiecutter if you want a simpler approach.

Usage:
    python create_project.py
"""

import os
import shutil
import sys
from pathlib import Path


def get_user_input():
    """Get project configuration from user."""
    print("=" * 60)
    print("Python Boilerplate Project Setup")
    print("=" * 60)
    print()
    
    config = {}
    
    config['project_name'] = input("Project name: ").strip() or "My Python Project"
    config['project_slug'] = input(f"Project slug [{config['project_name'].lower().replace(' ', '-')}]: ").strip() or config['project_name'].lower().replace(' ', '-').replace('_', '-')
    config['author_name'] = input("Author name: ").strip() or "Your Name"
    config['author_email'] = input("Author email: ").strip() or "your.email@example.com"
    config['python_version'] = input("Python version [3.10]: ").strip() or "3.10"
    config['verbose_logging'] = input("Verbose logging? (True/False) [True]: ").strip() or "True"
    config['description'] = input("Short description: ").strip() or "A Python project"
    
    print()
    print("Configuration:")
    print("-" * 60)
    for key, value in config.items():
        print(f"  {key}: {value}")
    print("-" * 60)
    
    confirm = input("\nProceed with project creation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(0)
    
    return config


def create_project(config):
    """Create new project from boilerplate."""
    source_dir = Path(__file__).parent
    target_dir = source_dir.parent / config['project_slug']
    
    if target_dir.exists():
        print(f"\nError: Directory '{target_dir}' already exists!")
        sys.exit(1)
    
    print(f"\nCreating project at: {target_dir}")
    
    # Create target directory
    target_dir.mkdir(parents=True)
    
    # Copy directories
    dirs_to_copy = ['app', 'data', 'logs']
    for dir_name in dirs_to_copy:
        src = source_dir / dir_name
        dst = target_dir / dir_name
        if src.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.log'))
            print(f"  ✓ Copied {dir_name}/")
    
    # Copy and customize files
    files_to_copy = ['requirements.txt', 'LICENSE']
    for file_name in files_to_copy:
        src = source_dir / file_name
        if src.exists():
            shutil.copy2(src, target_dir / file_name)
            print(f"  ✓ Copied {file_name}")
    
    # Create main.py
    main_py_content = f'''"""{ config['project_name'] } - Main Entry Point."""

from app.cli import cli

if __name__ == '__main__':
    cli()
'''
    (target_dir / 'main.py').write_text(main_py_content)
    print(f"  ✓ Created main.py")
    
    # Create README.md
    readme_content = f'''# {config['project_name']}

## Overview

{config['description']}

### Requirements

* Python {config['python_version']}+
* Pip for dependency installation

### Setup

Clone the repository and change to directory.

```bash
cd {config['project_slug']}
```

(Recommended) Use a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Configuration is managed through `app/config/config.yml` using Pydantic.

Logging configuration is in `app/config/logging.json`.

### Execution

Run the application:

```bash
python main.py app-test
```

### Features

- **Modular Architecture**: Clean separation of concerns
- **Configuration Management**: Pydantic-based with YAML support
- **Logging**: JSON-based configuration
- **CLI Interface**: Click-based commands
- **Type Safety**: Type hints and validation

---

**Author:** {config['author_name']} ({config['author_email']})
'''
    (target_dir / 'README.md').write_text(readme_content)
    print(f"  ✓ Created README.md")
    
    # Update config.yml
    config_yml_path = target_dir / 'app' / 'config' / 'config.yml'
    if config_yml_path.exists():
        config_yml_content = config_yml_path.read_text()
        config_yml_content = config_yml_content.replace('VERBOSE: True', f"VERBOSE: {config['verbose_logging']}")
        config_yml_path.write_text(config_yml_content)
        print(f"  ✓ Updated config.yml")
    
    # Create .gitignore
    gitignore_content = '''# Logs
logs/*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Data
data/input/*
data/output/*
data/reports/*
!data/input/.gitkeep
!data/output/.gitkeep
!data/reports/.gitkeep
'''
    (target_dir / '.gitignore').write_text(gitignore_content)
    print(f"  ✓ Created .gitignore")
    
    # Create .gitkeep files
    for subdir in ['input', 'output', 'reports']:
        gitkeep_file = target_dir / 'data' / subdir / '.gitkeep'
        gitkeep_file.touch()
    print(f"  ✓ Created .gitkeep files")
    
    print()
    print("=" * 60)
    print("✓ Project created successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  cd {config['project_slug']}")
    print(f"  python -m venv venv")
    print(f"  source venv/bin/activate")
    print(f"  pip install -r requirements.txt")
    print(f"  python main.py app-test")
    print()


if __name__ == '__main__':
    try:
        config = get_user_input()
        create_project(config)
    except KeyboardInterrupt:
        print("\n\nAborted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
