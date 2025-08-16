"""Test document service."""

import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import UploadFile
from app.models import DocumentType, DocumentResponse, ProcessingResult
from app.services import DocumentService


class TestDocumentService:
    """Test cases for DocumentService."""
    
    @pytest.mark.asyncio
    async def test_process_document_success(self, document_service, mock_file_storage, mock_ocr_service, mock_repository):
        """Test successful document processing."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"
        mock_file.read = AsyncMock(return_value=b"fake image data")
        
        mock_file_storage.is_valid_file_type.return_value = True
        mock_file_storage.save_file.return_value = ("saved_name.jpg", "/path/to/saved_name.jpg")
        
        mock_processing_result = ProcessingResult(
            data={"name": "John Doe", "id": "123456"},
            blur_intensity=0.1,
            glare_intensity=0.2
        )
        mock_ocr_service.process_file_contents.return_value = [mock_processing_result]
        
        mock_repository.save.return_value = "document_id_123"
        
        # Act
        result = await document_service.process_document(mock_file, DocumentType.IC)
        
        # Assert
        assert isinstance(result, DocumentResponse)
        assert result.status == "success"
        assert result.document_id == "document_id_123"
        assert len(result.results) == 1
        
        # Verify service calls
        mock_file_storage.is_valid_file_type.assert_called_once_with("test.jpg")
        mock_file_storage.save_file.assert_called_once()
        mock_ocr_service.process_file_contents.assert_called_once()
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_document_invalid_file_type(self, document_service, mock_file_storage):
        """Test processing with invalid file type."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.txt"
        mock_file_storage.is_valid_file_type.return_value = False
        
        # Act & Assert
        with pytest.raises(Exception):  # Should raise UnsupportedFileTypeError
            await document_service.process_document(mock_file, DocumentType.IC)
