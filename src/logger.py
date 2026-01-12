import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict


class JSONLinesFormatter(logging.Formatter):
    """
    Custom formatter that outputs log records as JSON Lines (JSONL) format.
    Each log record is a single line of JSON.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON line.

        Args:
            record: The log record to format

        Returns:
            A JSON string representing the log record
        """
        log_data: Dict[str, Any] = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add any extra fields that were passed to the logger
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data, default=str)


def setup_logger(
    name: str = 'iracing',
    log_dir: str = 'logs',
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    level: int = logging.DEBUG,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up a JSON Lines logger with rotating file handler.

    Args:
        name: Name of the logger
        log_dir: Directory to store log files (relative to project root)
        max_bytes: Maximum size of each log file before rotation (default: 10 MB)
        backup_count: Number of backup files to keep (default: 5)
        level: Logging level (default: INFO)
        console_output: Whether to also output to console (default: True)

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Create dated log filename
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file = log_path / f'{name}_{date_str}.jsonl'

    # Create rotating file handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(JSONLinesFormatter())

    # Add file handler to logger
    logger.addHandler(file_handler)

    # Optionally add console handler for human-readable output
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        # Use standard formatter for console (more readable)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def log_telemetry(logger: logging.Logger, telemetry_data: Dict[str, Any]) -> None:
    """
    Helper function to log telemetry data with extra fields.

    Args:
        logger: The logger instance
        telemetry_data: Dictionary of telemetry data to log
    """
    # Create a log record with extra data
    logger.info(
        'Telemetry data',
        extra={'extra_data': telemetry_data}
    )


# Create a default logger instance
logger = setup_logger()


if __name__ == '__main__':
    # Example usage
    logger = setup_logger('test_logger', level=logging.DEBUG)

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')

    # Log with extra telemetry data
    telemetry = {
        'speed': 120.5,
        'rpm': 7500,
        'gear': 4,
        'lap': 3
    }
    log_telemetry(logger, telemetry)

    # Log an exception
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception('An error occurred')

    print(f'\nLogs written to: logs/test_logger_{datetime.now().strftime("%Y-%m-%d")}.jsonl')
