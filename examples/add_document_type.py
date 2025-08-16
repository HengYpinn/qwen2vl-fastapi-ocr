"""
Migration script example - shows how to add new document types easily.

This demonstrates the extensibility of the new architecture.
"""

from app.models.enums import DocumentType
from app.api.endpoints.documents import router, process_document_endpoint
from app.services import DocumentService
from app.api.dependencies import get_document_service
from fastapi import Depends, File, UploadFile


def add_new_document_type():
    """
    Example of how to add a new document type without modifying existing code.
    
    Steps:
    1. Add to DocumentType enum
    2. Add prompt to prompts.py  
    3. Add endpoint (shown below)
    4. Add any specific post-processing to QwenOCRService
    """
    
    # Step 1: Add to enum (would be done in models/enums.py)
    # class DocumentType(str, Enum):
    #     ...
    #     DRIVING_LICENSE = "driving_license"
    
    # Step 3: Add endpoint
    @router.post("/driving-license", response_model=DocumentResponse)
    async def extract_driving_license(
        file: UploadFile = File(...),
        service: DocumentService = Depends(get_document_service)
    ):
        """Extract fields from driving license."""
        return await process_document_endpoint(file, DocumentType.DRIVING_LICENSE, service)


if __name__ == "__main__":
    print("This is an example of how to extend the system with new document types.")
    print("The new architecture makes it easy to add features without modifying existing code.")
