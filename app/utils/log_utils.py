"""Logging utilities.

This module provides a function to get a logger object with a defined
logging level and formatting.

Example:
    logger = get_module_logger(__name__)
    logger.debug('Module %s initiated.', __name__)
"""

import json
import logging.config
import os

from app.config.config import CONFIG


def print_logger_settings(logger):
    """Print the settings of a logger.

    Args:
        logger (logging.Logger): Logger to print settings of.
    """
    print(f'Logger name: {logger.name}')
    print(f'Logger level: {logging.getLevelName(logger.level)}')
    print('Handlers:')
    for loghandler in logger.handlers:
        print(f'    Handler: {loghandler}')
        print(f'    Level: {logging.getLevelName(loghandler.level)}')
        print(f'    Formatter: {loghandler.formatter}')


def get_module_logger(module, level: str = None) -> logging.Logger:
    """Return a logger object.

    Currently just a StreamHandler with a defined Formatting of
    '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s' will be returned.

    Example:
        logger = get_module_logger(__name__)

    Args:
        module (str): Name of the requesting module. Recommended: __name__
        level (str): Logging Level. Default: None

    Returns:
        logging.Logger: Logger object.
    """
    with open('app/config/logging.json') as cfgfile:
        config = json.load(cfgfile)

    if CONFIG.VERBOSE:
        config['handlers']['console']['level'] = 'DEBUG'
        config['loggers']['root']['level'] = 'DEBUG'

    logging.config.dictConfig(config)

    logger = logging.getLogger(module)
    # loglevel = level if level else os.environ.get('DEBUG_LEVEL', 'DEBUG')
    # logger.setLevel(loglevel)

    return logger
