"""Main application module."""

from app.utils.log_utils import get_module_logger

logger = get_module_logger(__name__)
logger.debug('Module %s initiated.', __name__)


def Application_Test():
    """A simple test function."""

    logger.info('Test function executed.')