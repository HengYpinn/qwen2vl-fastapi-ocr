"""Test configuration and fixtures."""

import pytest
from unittest.mock import Mock
from app.repositories import IDocumentRepository
from app.services import IFileStorageService, IOCRService, DocumentService


@pytest.fixture
def mock_repository():
    """Mock document repository."""
    return Mock(spec=IDocumentRepository)


@pytest.fixture
def mock_file_storage():
    """Mock file storage service."""
    return Mock(spec=IFileStorageService)


@pytest.fixture
def mock_ocr_service():
    """Mock OCR service."""
    return Mock(spec=IOCRService)


@pytest.fixture
def document_service(mock_repository, mock_file_storage, mock_ocr_service):
    """Document service with mocked dependencies."""
    return DocumentService(
        repository=mock_repository,
        file_storage=mock_file_storage,
        ocr_service=mock_ocr_service
    )
