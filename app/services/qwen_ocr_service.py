"""Qwen OCR service implementation."""

import io
from typing import List
from PIL import Image
from app.core.exceptions import OCRProcessingError, FileProcessingError
from app.core.logging import get_logger
from app.models import ProcessingResult, DocumentType
from app.services.ocr_service import IOCRService
from utils.image_quality import compute_blur_intensity, compute_glare_intensity
from utils.pdf_utils import convert_pdf_to_images
from utils.passport_utils import normalize_passport_number
from utils.ssm_utils import normalize_ssm_registration_numbers
from qwen_infer import extract_info_from_image
from prompts import PROMPTS

logger = get_logger(__name__)


class QwenOCRService(IOCRService):
    """Qwen OCR service implementation."""
    
    async def process_images(
        self, 
        images: List[Image.Image], 
        document_type: DocumentType
    ) -> List[ProcessingResult]:
        """Process images and extract information."""
        try:
            prompt = PROMPTS[document_type.value]
            results = []
            
            for idx, img in enumerate(images):
                # Run OCR inference
                data = extract_info_from_image(img, prompt)
                
                # Compute image quality metrics
                blur = compute_blur_intensity(img)
                glare = compute_glare_intensity(img)
                
                # Apply post-processing based on document type
                data = self._apply_post_processing(data, document_type)
                
                # Create result object
                result = ProcessingResult(
                    data=data,
                    page=idx + 1 if len(images) > 1 else None,
                    blur_intensity=blur,
                    glare_intensity=glare
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            raise OCRProcessingError(f"OCR processing failed: {e}")
    
    async def process_file_contents(
        self, 
        contents: bytes, 
        document_type: DocumentType
    ) -> List[ProcessingResult]:
        """Process file contents (image or PDF) and extract information."""
        try:
            # Determine if it's a PDF or image
            if contents[:4] == b"%PDF":
                images = convert_pdf_to_images(contents)
            else:
                img = Image.open(io.BytesIO(contents)).convert("RGB")
                images = [img]
            
            return await self.process_images(images, document_type)
            
        except Exception as e:
            logger.error(f"File processing failed: {e}")
            raise FileProcessingError(f"File processing failed: {e}")
    
    def _apply_post_processing(self, data: dict, document_type: DocumentType) -> dict:
        """Apply document-type specific post-processing."""
        if document_type == DocumentType.PASSPORT:
            # Apply passport number normalization
            if "passportNumber" in data and data["passportNumber"]:
                data["passportNumber"] = normalize_passport_number(
                    str(data["passportNumber"]), 
                    data.get("countryCode")
                )
        
        elif document_type == DocumentType.SSM_FORM_D:
            # Apply SSM registration number normalization
            data = normalize_ssm_registration_numbers(data)
        
        return data
