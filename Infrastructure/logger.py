import logging
import os
from datetime import datetime
import traceback


class Logger:
    """
    A class for managing logs in an application with advanced features.
    """

    def __init__(self, log_folder="logs", log_level=logging.INFO):
        """
        Initializes a logging system with a log folder and basic settings.

        Args:
            log_folder (str): The folder to save log files.
            log_level: The base log level.
        """
        # Ensure that the log folder exists
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Create a log file name with date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(log_folder, f"app_log_{current_time}.log")

        # Define the log format
        log_format = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        # Set up the main logger
        self.logger = logging.getLogger('data_analyzer')
        self.logger.setLevel(log_level)

        # Set up file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.logger.info(f"Logging initialized. Log file: {log_file}")

    def info(self, message):
        """Logs an informational message"""
        self.logger.info(message)

    def debug(self, message):
        """Logs a debug message"""
        self.logger.debug(message)

    def warning(self, message):
        """Logs a warning message"""
        self.logger.warning(message)

    def error(self, message, include_traceback=True):
        """
        Logs an error message

        Args:
            message: The error message
            include_traceback: Whether to include traceback information
        """
        if include_traceback:
            self.logger.error(f"{message}\n{traceback.format_exc()}")
        else:
            self.logger.error(message)

    def critical(self, message, include_traceback=True):
        """
        Logs a critical error message

        Args:
            message: The critical error message
            include_traceback: Whether to include traceback information
        """
        if include_traceback:
            self.logger.critical(f"{message}\n{traceback.format_exc()}")
        else:
            self.logger.critical(message)

    def log_user_action(self, action, details=None):
        """
        Logs a user action

        Args:
            action: The type of action performed
            details: Additional details about the action
        """
        message = f"USER ACTION: {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)

    def log_data_operation(self, operation, rows_affected=None, details=None):
        """
        Logs a data operation

        Args:
            operation: The type of operation
            rows_affected: The number of rows affected
            details: Additional details
        """
        message = f"DATA: {operation}"
        if rows_affected is not None:
            message += f" - Rows affected: {rows_affected}"
        if details:
            message += f" - {details}"
        self.logger.info(message)

    def log_query(self, query, execution_time=None, result_size=None):
        """
        Logs a query

        Args:
            query: The query text
            execution_time: The execution time in milliseconds
            result_size: The size of the result (number of rows)
        """
        message = f"QUERY: {query}"
        if execution_time is not None:
            message += f" - Execution time: {execution_time}ms"
        if result_size is not None:
            message += f" - Results: {result_size} rows"
        self.logger.info(message)

    def get_logger(self):
        """Returns the logger object"""
        return self.logger
