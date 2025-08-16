"""Dependency injection setup."""

from functools import lru_cache
from pymongo import MongoClient
from app.core.config import settings
from app.repositories import MongoDocumentRepository, IDocumentRepository
from app.services import (
    LocalFileStorageService, 
    IFileStorageService,
    QwenOCRService,
    IOCRService,
    DocumentService
)


@lru_cache()
def get_mongo_client() -> MongoClient:
    """Get MongoDB client instance."""
    return MongoClient(settings.mongo_uri)


def get_document_repository() -> IDocumentRepository:
    """Get document repository instance."""
    client = get_mongo_client()
    return MongoDocumentRepository(client)


def get_file_storage_service() -> IFileStorageService:
    """Get file storage service instance."""
    return LocalFileStorageService()


def get_ocr_service() -> IOCRService:
    """Get OCR service instance."""
    return QwenOCRService()


def get_document_service() -> DocumentService:
    """Get document service instance."""
    return DocumentService(
        repository=get_document_repository(),
        file_storage=get_file_storage_service(),
        ocr_service=get_ocr_service()
    )
