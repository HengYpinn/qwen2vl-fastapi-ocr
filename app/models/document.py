from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.with_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema(),
        )
    
    @classmethod
    def validate(cls, v, info=None):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
            raise ValueError(f"Invalid ObjectId: {v}")
        raise ValueError(f"Invalid ObjectId type: {type(v)}")
    
    def __str__(self):
        return str(super())


class DocumentRecord(BaseModel):
    """Document record stored in MongoDB"""
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    filename: str
    file_path: str
    content_type: str
    document_type: str
    results: List[Dict[str, Any]]
    upload_time: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }


class ProcessingResult(BaseModel):
    """Result of document processing."""
    
    data: Dict[str, Any]
    page: Optional[int] = None
    blur_intensity: Optional[float] = None
    glare_intensity: Optional[float] = None


class DocumentResponse(BaseModel):
    """API response for document processing"""
    
    status: str
    document_id: str
    results: List[Dict[str, Any]]


class DocumentListItem(BaseModel):
    """Document list item for API responses."""
    
    document_id: str
    filename: str
    upload_time: datetime
    preview: List[Dict[str, Any]]


class UploadRequest(BaseModel):
    """Base upload request model."""
    
    file_size: Optional[int] = None
    content_type: Optional[str] = None


class DocumentListResponse(BaseModel):
    """API response for document listing"""
    
    documents: List[DocumentRecord]
    total: int
    page: int
    page_size: int