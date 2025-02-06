import configparser
from pytz import timezone
from pathlib import Path
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os


class Logger:
    def __init__(self, name):
        """
        Initialize the logger by reading the log file path from the config file.
        Set up the logger with a rotating file handler to avoid growing file size.
        """
        self.config_file = Path("config_.ini")
        parser = configparser.ConfigParser()
        # Read the log file path from the config file
        self.log_path = Path(os.getcwd()) / "app_logs.json" # But what to do if there is no config file yet??? name the file app_logs.json
        self.log_path = Path(self.log_path)

        # Ensure the log file exists
        self.log_path.touch(exist_ok=True)

        # Set up logger with rotating file handler
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler to limit the size of the log file to 10MB
        self.handler = RotatingFileHandler(
            self.log_path, maxBytes=10 * 1024 * 1024, backupCount=3
        )
        self.handler.setLevel(logging.DEBUG)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(self.handler)

    def log_status(self, info, status):
        """
        Log a status message with the specified level (INFO, ERROR, etc.).
        
        Args:
            info (str): The log message.
            status (str): The severity level of the log (INFO, ERROR, etc.).
        """
        from utils import show_error
        
        log_message = {
            "timestamp": datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S"),
            "level": status,
            "message": info,
            "module": __name__
        }

        try:
            if status == "INFO":
                self.logger.info(info)
            elif status == "ERROR":
                self.logger.error(info)
            elif status == "WARNING":
                self.logger.warning(info)
            elif status == "CRITICAL":
                self.logger.critical(info)
            elif status == "DEBUG":
                self.logger.debug(info)
            else:
                self.logger.info(info)  # Default to INFO if the status is not recognized
        except Exception as e:
            show_error(f"Error while logging message: {e}")

    def log_exception(self, exception):
        """
        Log an exception with full traceback.
        
        Args:
            exception (Exception): The exception object.
        """
        self.logger.error("An exception occurred", exc_info=exception)


# # Example usage function
# def example_function():
#     """
#     Example function to demonstrate how to use the Logger class.
#     """
#     log = Logger()
#     try:
#         log.log_status("Starting the example function", "INFO")
#         # Simulate some logic
#         x = 1 / 0  # This will raise a ZeroDivisionError
#     except Exception as e:
#         log.log_exception(e)
#         log.log_status(f"Error occurred in example_function: {str(e)}", "ERROR")
#     finally:
#         log.log_status("Finished the example function", "INFO")



