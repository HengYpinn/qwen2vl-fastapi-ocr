"""Data models for the application."""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId for Pydantic models."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentRecord(BaseModel):
    """Document record model."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    filename: str
    file_path: str
    content_type: str
    document_type: str
    results: List[Dict[str, Any]]
    upload_time: datetime = Field(default_factory=datetime.now)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProcessingResult(BaseModel):
    """Result of document processing."""
    
    data: Dict[str, Any]
    page: Optional[int] = None
    blur_intensity: Optional[float] = None
    glare_intensity: Optional[float] = None


class DocumentResponse(BaseModel):
    """API response for document processing."""
    
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
