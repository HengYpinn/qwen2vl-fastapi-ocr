"""Core module initialization."""

from .config import settings
from .exceptions import *
from .logging import setup_logging, get_logger

__all__ = [
    "settings",
    "setup_logging", 
    "get_logger",
    "DocumentProcessingError",
    "UnsupportedFileTypeError",
    "FileProcessingError",
    "OCRProcessingError",
    "DatabaseError",
    "FileStorageError"
]
