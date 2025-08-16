"""Logging configuration."""

import logging
import sys
from typing import Dict, Any
from app.core.config import settings


def setup_logging() -> None:
    """Configure application logging."""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    loggers = {
        "uvicorn": logging.INFO,
        "uvicorn.error": logging.INFO,
        "uvicorn.access": logging.INFO,
        "pymongo": logging.WARNING,
    }
    
    for logger_name, level in loggers.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
