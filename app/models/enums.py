"""Document types enumeration."""

from enum import Enum


class DocumentType(str, Enum):
    """Supported document types."""
    
    IC = "ic"
    PASSPORT = "passport"
    CASH_DEPOSIT = "cash_deposit"
    BANK_TRANSFER = "bank_transfer"
    SSM_FORM_D = "ssm_form_d"
    UTILITY_BILL = "utility_bill"


class FileExtension(str, Enum):
    """Supported file extensions."""
    
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    PDF = ".pdf"
