"""Main document processing service."""

from typing import List
from fastapi import UploadFile
from app.core.exceptions import UnsupportedFileTypeError
from app.core.logging import get_logger
from app.models import DocumentRecord, DocumentResponse, DocumentType, ProcessingResult
from app.repositories import IDocumentRepository
from app.services.file_storage import IFileStorageService
from app.services.ocr_service import IOCRService

logger = get_logger(__name__)


class DocumentService:
    """Main service for document processing operations."""
    
    def __init__(
        self,
        repository: IDocumentRepository,
        file_storage: IFileStorageService,
        ocr_service: IOCRService
    ):
        self._repository = repository
        self._file_storage = file_storage
        self._ocr_service = ocr_service
    
    async def process_document(
        self, 
        file: UploadFile, 
        document_type: DocumentType
    ) -> DocumentResponse:
        """Process an uploaded document."""
        logger.info(f"Processing document: {file.filename} as {document_type.value}")
        
        # Validate file type
        if not self._file_storage.is_valid_file_type(file.filename):
            raise UnsupportedFileTypeError(f"Unsupported file type: {file.filename}")
        
        # Read file contents
        contents = await file.read()
        
        # Save file
        saved_name, saved_path = await self._file_storage.save_file(contents, file.filename)
        
        # Process with OCR
        processing_results = await self._ocr_service.process_file_contents(contents, document_type)
        
        # Convert processing results to dict format for storage
        results_dict = [
            {
                "data": result.data,
                "page": result.page,
                "blurIntensity": result.blur_intensity,
                "glareIntensity": result.glare_intensity
            }
            for result in processing_results
        ]
        
        # Create document record
        record = DocumentRecord(
            filename=saved_name,
            file_path=saved_path,
            content_type=file.content_type,
            document_type=document_type.value,
            results=results_dict
        )
        
        # Save to database
        document_id = await self._repository.save(record)
        
        logger.info(f"Document processed successfully: {document_id}")
        
        return DocumentResponse(
            status="success",
            document_id=document_id,
            results=results_dict
        )
    
    async def get_documents(self, limit: int = 100, skip: int = 0) -> List[DocumentRecord]:
        """Get list of documents."""
        return await self._repository.find_all(limit=limit, skip=skip)
    
    async def get_document_by_id(self, document_id: str) -> DocumentRecord:
        """Get a specific document by ID."""
        document = await self._repository.find_by_id(document_id)
        if not document:
            raise ValueError(f"Document not found: {document_id}")
        return document
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document and its associated file."""
        # Get document to find file path
        document = await self._repository.find_by_id(document_id)
        if not document:
            return False
        
        # Delete file
        await self._file_storage.delete_file(document.file_path)
        
        # Delete from database
        return await self._repository.delete_by_id(document_id)
