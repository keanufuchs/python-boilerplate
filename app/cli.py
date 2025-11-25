"""CLI module."""

from pathlib import Path

import click

from app.app import Application_Test
from app.utils.log_utils import get_module_logger

logger = get_module_logger(__name__)
logger.debug('Module %s initiated.', __name__)


@click.group()
def cli():
    """Run the CLI application."""
    logger.info('Application started.')
    logger.info('Debug mode is %s.', 'on' if logger.isEnabledFor(10) else 'off')
    logger.debug('Debugging test message.')


# Application_Test
@cli.command()
def app_test():
    """Run the application test function."""
    Application_Test()
    logger.info('Application test command executed.')