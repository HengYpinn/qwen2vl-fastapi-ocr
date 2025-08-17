"""MongoDB document repository implementation."""

from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from app.core.config import settings
from app.core.exceptions import DatabaseError
from app.core.logging import get_logger
from app.models import DocumentRecord
from app.repositories.base import IDocumentRepository

logger = get_logger(__name__)


class MongoDocumentRepository(IDocumentRepository):
    """MongoDB implementation of document repository."""
    
    def __init__(self, mongo_client: MongoClient):
        self._client = mongo_client
        self._db = self._client[settings.database_name]
        self._collection = self._db[settings.collection_name]
    
    async def save(self, record: DocumentRecord) -> str:
        """Save a document record and return its ID."""
        try:
            # Convert to dict and handle ObjectId
            doc_dict = record.model_dump(by_alias=True, exclude_unset=True)
            if "_id" in doc_dict and doc_dict["_id"] is None:
                doc_dict.pop("_id")
            
            result = self._collection.insert_one(doc_dict)
            logger.info(f"Document saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save document: {e}")
            raise DatabaseError(f"Failed to save document: {e}")
    
    async def find_by_id(self, document_id: str) -> Optional[DocumentRecord]:
        """Find a document by its ID."""
        try:
            if not ObjectId.is_valid(document_id):
                return None
            
            doc = self._collection.find_one({"_id": ObjectId(document_id)})
            if doc:
                return DocumentRecord.model_validate(doc)
            return None
        except Exception as e:
            logger.error(f"Failed to find document {document_id}: {e}")
            raise DatabaseError(f"Failed to find document: {e}")
    
    async def find_all(self, limit: int = 100, skip: int = 0) -> List[DocumentRecord]:
        """Find all documents with pagination."""
        try:
            cursor = self._collection.find().sort("upload_time", -1).skip(skip).limit(limit)
            documents = []
            for doc in cursor:
                documents.append(DocumentRecord.model_validate(doc))
            return documents
        except Exception as e:
            logger.error(f"Failed to find documents: {e}")
            raise DatabaseError(f"Failed to find documents: {e}")
    
    async def delete_by_id(self, document_id: str) -> bool:
        """Delete a document by its ID."""
        try:
            if not ObjectId.is_valid(document_id):
                return False
            
            result = self._collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            raise DatabaseError(f"Failed to delete document: {e}")
