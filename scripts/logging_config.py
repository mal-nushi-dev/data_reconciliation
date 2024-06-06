import logging
import coloredlogs
from scripts.get_config import get_config


def setup_logger(name=None, level=None, log_to_file=False, log_filename='app.log'):
    if level is None:
        level = get_config('LOGGING', 'LOG_LEVEL')

    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the minimum logging level

    # Create a coloredlogs format
    coloredlogs_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configure coloredlogs
    coloredlogs.install(level=level, logger=logger, fmt=coloredlogs_format)

    if log_to_file:
        file_handler = logging.FileHandler(log_filename)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def get_logger(name=None):
    return setup_logger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
