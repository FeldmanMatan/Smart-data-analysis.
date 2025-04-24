import time
import psutil
import threading
import os
import platform
from datetime import datetime


class PerformanceMonitor:
    """
    A class for monitoring the performance of the application.
    """

    def __init__(self, log_interval=30):
        """
        Initializes a performance monitor

        Args:
            log_interval (int): The time interval in seconds between log entries.
        """
        self.log_interval = log_interval
        self.is_monitoring = False
        self.monitor_thread = None
        self.process = psutil.Process(os.getpid())
        self.start_time = time.time()
        self.operation_times = {}
        self.logger = None

    def set_logger(self, logger):
        """
        Sets the logger to be used

        Args:
            logger: Logger object
        """
        self.logger = logger

    def start_monitoring(self):
        """Starts the performance monitoring"""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_task)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        if self.logger:
            self.logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stops the performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None

        if self.logger:
            self.logger.info("Performance monitoring stopped")

    def _monitoring_task(self):
        """Background task that monitors the performance"""
        while self.is_monitoring:
            try:
                self.log_system_info()
                time.sleep(self.log_interval)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in performance monitoring: {str(e)}")
                break

    def log_system_info(self):
        """Logs system and application performance data"""
        if not self.logger:
            return

        try:
            # Memory usage information
            memory_info = self.process.memory_info()
            memory_usage_mb = memory_info.rss / 1024 / 1024

            # CPU usage
            cpu_percent = self.process.cpu_percent(interval=1.0)

            # Uptime
            uptime = time.time() - self.start_time
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

            # Operating system information
            system_info = f"{platform.system()} {platform.release()}"

            # Log message
            log_message = (
                f"PERFORMANCE: "
                f"Memory: {memory_usage_mb:.2f} MB | "
                f"CPU: {cpu_percent:.1f}% | "
                f"Uptime: {uptime_str} | "
                f"OS: {system_info}"
            )

            self.logger.info(log_message)
        except Exception as e:
            self.logger.error(f"Error logging system info: {str(e)}")

    def start_timer(self, operation_name):
        """
        Starts a timer for a specific operation

        Args:
            operation_name (str): The name of the operation to time

        Returns:
            str: A unique identifier for this timer
        """
        timer_id = f"{operation_name}_{datetime.now().strftime('%H%M%S%f')}"
        self.operation_times[timer_id] = time.time()
        return timer_id

    def end_timer(self, timer_id, additional_info=None):
        """
        Ends a timer and logs the result

        Args:
            timer_id (str): The timer identifier returned by start_timer
            additional_info (str, optional): Additional info to log

        Returns:
            float: The elapsed time in milliseconds
        """
        if timer_id not in self.operation_times:
            if self.logger:
                self.logger.warning(f"Timer ID not found: {timer_id}")
            return 0

        elapsed_time = (time.time() - self.operation_times[timer_id]) * 1000
        del self.operation_times[timer_id]

        if self.logger:
            operation_name = timer_id.split('_')[0]
            log_message = f"TIMER: {operation_name} completed in {elapsed_time:.2f} ms"
            if additional_info:
                log_message += f" - {additional_info}"
            self.logger.info(log_message)

        return elapsed_time
