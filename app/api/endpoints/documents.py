"""Document processing API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api.dependencies import get_document_service
from app.core.exceptions import DocumentProcessingError
from app.core.logging import get_logger
from app.models import DocumentResponse, DocumentListItem, DocumentType
from app.services import DocumentService

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["documents"])


async def process_document_endpoint(
    file: UploadFile,
    document_type: DocumentType,
    service: DocumentService = Depends(get_document_service)
) -> DocumentResponse:
    """Generic document processing endpoint."""
    try:
        return await service.process_document(file, document_type)
    except DocumentProcessingError as e:
        logger.error(f"Document processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/ic", response_model=DocumentResponse)
async def extract_ic(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from Malaysian IC."""
    return await process_document_endpoint(file, DocumentType.IC, service)


@router.post("/passport", response_model=DocumentResponse)
async def extract_passport(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from international passport."""
    return await process_document_endpoint(file, DocumentType.PASSPORT, service)


@router.post("/cash-deposit", response_model=DocumentResponse)
async def extract_cash_deposit(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from cash deposit receipt."""
    return await process_document_endpoint(file, DocumentType.CASH_DEPOSIT, service)


@router.post("/bank-transfer", response_model=DocumentResponse)
async def extract_bank_transfer(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from bank transfer receipt."""
    return await process_document_endpoint(file, DocumentType.BANK_TRANSFER, service)


@router.post("/ssm-form-d", response_model=DocumentResponse)
async def extract_ssm_form_d(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from SSM Form D."""
    return await process_document_endpoint(file, DocumentType.SSM_FORM_D, service)


@router.post("/utility-bill", response_model=DocumentResponse)
async def extract_utility_bill(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """Extract fields from Malaysia utility bills."""
    return await process_document_endpoint(file, DocumentType.UTILITY_BILL, service)


@router.get("/documents", response_model=List[DocumentListItem])
async def list_documents(
    limit: int = 100,
    skip: int = 0,
    service: DocumentService = Depends(get_document_service)
):
    """List all processed documents."""
    try:
        documents = await service.get_documents(limit=limit, skip=skip)
        return [
            DocumentListItem(
                document_id=str(doc.id),
                filename=doc.filename,
                upload_time=doc.upload_time,
                preview=doc.results[:1]  # First result only
            )
            for doc in documents
        ]
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Get a specific document by ID."""
    try:
        document = await service.get_document_by_id(document_id)
        return {
            "document_id": str(document.id),
            "filename": document.filename,
            "upload_time": document.upload_time,
            "document_type": document.document_type,
            "results": document.results
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Delete a document."""
    try:
        success = await service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"status": "deleted", "document_id": document_id}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
