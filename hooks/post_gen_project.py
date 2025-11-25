#!/usr/bin/env python
"""Post-generation hook for cookiecutter template."""

import os
import subprocess
from pathlib import Path


def main():
    """Run post-generation tasks."""
    use_pyenv = "{{ cookiecutter.use_pyenv }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    python_version = "{{ cookiecutter.python_version }}"
    
    if use_pyenv != "yes":
        # Remove .python-version file if not using pyenv
        python_version_file = Path(".python-version")
        if python_version_file.exists():
            python_version_file.unlink()
            print("  • Removed .python-version (use_pyenv=no)")
    else:
        # Try to create pyenv virtualenv
        pyenv_path = os.popen("which pyenv").read().strip()
        if pyenv_path:
            print(f"  • pyenv found, attempting to create virtualenv '{project_slug}'...")
            try:
                # Check if Python version is installed
                result = subprocess.run(
                    ["pyenv", "versions", "--bare"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                installed_versions = result.stdout.strip().split('\n')
                
                if python_version not in installed_versions:
                    print(f"  • Python {python_version} not installed, installing...")
                    subprocess.run(["pyenv", "install", python_version], check=True)
                
                # Create virtualenv
                subprocess.run(["pyenv", "virtualenv", python_version, project_slug], check=True)
                # Set local version
                subprocess.run(["pyenv", "local", project_slug], check=True)
                print(f"  ✓ Created pyenv virtualenv '{project_slug}' and set as local version")
            except subprocess.CalledProcessError as e:
                print(f"  ! pyenv virtualenv creation failed: {e}")
                print(f"  ! You can manually create it with: pyenv virtualenv {python_version} {project_slug}")
        else:
            print("  ! pyenv not found")
            print(f"  ! Install pyenv to use: pyenv virtualenv {python_version} {project_slug}")


if __name__ == "__main__":
    main()
