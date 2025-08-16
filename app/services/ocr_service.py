"""OCR processing service interface."""

from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from app.models import ProcessingResult, DocumentType


class IOCRService(ABC):
    """Abstract OCR service interface."""
    
    @abstractmethod
    async def process_images(
        self, 
        images: List[Image.Image], 
        document_type: DocumentType
    ) -> List[ProcessingResult]:
        """Process images and extract information."""
        pass
    
    @abstractmethod
    async def process_file_contents(
        self, 
        contents: bytes, 
        document_type: DocumentType
    ) -> List[ProcessingResult]:
        """Process file contents (image or PDF) and extract information."""
        pass
