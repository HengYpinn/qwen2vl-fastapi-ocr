"""Document repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.models import DocumentRecord


class IDocumentRepository(ABC):
    """Abstract document repository interface."""
    
    @abstractmethod
    async def save(self, record: DocumentRecord) -> str:
        """Save a document record and return its ID."""
        pass
    
    @abstractmethod
    async def find_by_id(self, document_id: str) -> Optional[DocumentRecord]:
        """Find a document by its ID."""
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 100, skip: int = 0) -> List[DocumentRecord]:
        """Find all documents with pagination."""
        pass
    
    @abstractmethod
    async def delete_by_id(self, document_id: str) -> bool:
        """Delete a document by its ID."""
        pass
