"""Function to run the CLI application."""

from app.cli import cli
from app.utils.log_utils import get_module_logger

logger = get_module_logger(__name__)
logger.debug('Module %s initiated.', __name__)

if __name__ == '__main__':
    try:
        cli()
    except Exception as err:
        logger.critical('An error occurred: %s', err, exc_info=True)
