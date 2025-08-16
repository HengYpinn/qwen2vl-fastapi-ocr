"""Custom exceptions for the application."""

from typing import Optional


class DocumentProcessingError(Exception):
    """Base exception for document processing errors."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class UnsupportedFileTypeError(DocumentProcessingError):
    """Raised when an unsupported file type is uploaded."""
    pass


class FileProcessingError(DocumentProcessingError):
    """Raised when file processing fails."""
    pass


class OCRProcessingError(DocumentProcessingError):
    """Raised when OCR processing fails."""
    pass


class DatabaseError(DocumentProcessingError):
    """Raised when database operations fail."""
    pass


class FileStorageError(DocumentProcessingError):
    """Raised when file storage operations fail."""
    pass
