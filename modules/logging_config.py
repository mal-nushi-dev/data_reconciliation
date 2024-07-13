import logging
import coloredlogs
from modules.get_config import get_config


class Logger:
    """
    Custom Logger class that supports both console and file logging with colored output.

    Attr:
        logger (logging.Logger): The logger instance.
    """

    def __init__(self, name=None, level=None, log_to_file=False, log_filename='app.log'):
        """
        Initializes the Logger instance.

        Args:
            name (str, optional): The name of the logger. Defaults to None.
            level (str, optional): The logging level. Defaults to None.
            log_to_file (bool, optional): Whether to log to a file. Defaults to False.
            log_filename (str, optional): The filename for the log file. Defaults to 'app.log'.
        """

        if level is None:
            level = get_config('LOGGING', 'LOG_LEVEL')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)  # Set the minimum logging level

        coloredlogs_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        coloredlogs.install(level=level, logger=self.logger, fmt=coloredlogs_format)

        if log_to_file:
            file_handler = logging.FileHandler(log_filename)
            file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Logs a critical message."""
        self.logger.critical(message)


if __name__ == "__main__":
    logger = Logger(__name__)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
