"""File storage service interface."""

from abc import ABC, abstractmethod
from typing import Tuple


class IFileStorageService(ABC):
    """Abstract file storage service interface."""
    
    @abstractmethod
    async def save_file(self, contents: bytes, filename: str) -> Tuple[str, str]:
        """
        Save file contents and return (saved_filename, saved_path).
        
        Args:
            contents: File contents as bytes
            filename: Original filename
            
        Returns:
            Tuple of (timestamped_filename, full_file_path)
        """
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file and return success status."""
        pass
    
    @abstractmethod
    def is_valid_file_type(self, filename: str) -> bool:
        """Check if file type is supported."""
        pass
