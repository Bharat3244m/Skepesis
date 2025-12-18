"""
Centralized Logging Configuration for Skepesis

Provides consistent logging format across the entire application with:
- Timestamp with milliseconds
- Log level with color coding (for console)
- Module/file name and line number
- Function name
- Detailed error messages with stack traces
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from app.config import get_settings

settings = get_settings()


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m', # Bold Red
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    def __init__(self, fmt: str, datefmt: str = None, use_colors: bool = True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the record to avoid modifying the original
        # (which would break other formatters like FileFormatter)
        record = logging.makeLogRecord(record.__dict__)
        
        if self.use_colors:
            # Colorize level name
            color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{color}{record.levelname:8}{self.RESET}"
        
        return super().format(record)


class FileFormatter(logging.Formatter):
    """Formatter for file output (no colors, more details)"""
    
    def format(self, record: logging.LogRecord) -> str:
        # Add extra context for errors
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        return super().format(record)


def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        log_file: Optional file path for file logging
        
    Returns:
        Configured logging.Logger instance
        
    Usage:
        from app.logger import get_logger
        logger = get_logger(__name__)
        logger.info("This is an info message")
        logger.error("This is an error", exc_info=True)
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set log level based on debug setting
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(log_level)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Console format: timestamp | level | module:line | function | message
    console_format = (
        "%(asctime)s │ %(levelname)s │ %(filename)s:%(lineno)s │ %(funcName)s │ %(message)s"
    )
    console_formatter = ColoredFormatter(
        fmt=console_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        use_colors=sys.stdout.isatty()  # Only use colors if terminal supports it
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified or in production)
    if log_file or not settings.debug:
        file_path = log_file or "logs/skepesis.log"
        
        # Create logs directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        
        # File format: more detailed, no colors
        file_format = (
            "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
            "%(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s"
        )
        file_formatter = FileFormatter(
            fmt=file_format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def setup_app_logging(log_file: Optional[str] = None) -> None:
    """
    Configure logging for the entire application.
    Call this once at application startup.
    
    Args:
        log_file: Optional path for log file output
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = (
        "%(asctime)s │ %(levelname)-8s │ %(name)s │ %(filename)s:%(lineno)d │ %(message)s"
    )
    console_formatter = ColoredFormatter(
        fmt=console_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        use_colors=sys.stdout.isatty()
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file or not settings.debug:
        file_path = log_file or "logs/skepesis.log"
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = (
            "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
            "%(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s"
        )
        file_formatter = FileFormatter(fmt=file_format, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


class LoggerMixin:
    """
    Mixin class to add logging capability to any class.
    
    Usage:
        class MyService(LoggerMixin):
            def do_something(self):
                self.logger.info("Doing something")
    """
    
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__module__)
        return self._logger


# Convenience function for quick logging without setup
def log_error(message: str, exc: Exception = None, **kwargs) -> None:
    """Quick error logging with optional exception"""
    logger = get_logger("skepesis")
    if exc:
        logger.error(f"{message}: {exc}", exc_info=True, **kwargs)
    else:
        logger.error(message, **kwargs)


def log_info(message: str, **kwargs) -> None:
    """Quick info logging"""
    logger = get_logger("skepesis")
    logger.info(message, **kwargs)


def log_warning(message: str, **kwargs) -> None:
    """Quick warning logging"""
    logger = get_logger("skepesis")
    logger.warning(message, **kwargs)


def log_debug(message: str, **kwargs) -> None:
    """Quick debug logging"""
    logger = get_logger("skepesis")
    logger.debug(message, **kwargs)
