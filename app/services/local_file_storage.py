"""Local file storage service implementation."""

import os
from datetime import datetime
from typing import Tuple
from app.core.config import settings
from app.core.exceptions import FileStorageError, UnsupportedFileTypeError
from app.core.logging import get_logger
from app.services.file_storage import IFileStorageService

logger = get_logger(__name__)


class LocalFileStorageService(IFileStorageService):
    """Local file system storage implementation."""
    
    def __init__(self, upload_dir: str = None):
        self.upload_dir = upload_dir if upload_dir is not None else settings.upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_file(self, contents: bytes, filename: str) -> Tuple[str, str]:
        """Save file contents and return (saved_filename, saved_path)."""
        try:
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            saved_name = f"{timestamp}_{filename}"
            saved_path = os.path.join(self.upload_dir, saved_name)
            
            # Write file
            with open(saved_path, "wb") as f:
                f.write(contents)
            
            logger.info(f"File saved: {saved_path}")
            return saved_name, saved_path
            
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {e}")
            raise FileStorageError(f"Failed to save file: {e}")
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file and return success status."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            raise FileStorageError(f"Failed to delete file: {e}")
    
    def is_valid_file_type(self, filename: str) -> bool:
        """Check if file type is supported."""
        ext = os.path.splitext(filename.lower())[1]
        return ext in settings.allowed_extensions
