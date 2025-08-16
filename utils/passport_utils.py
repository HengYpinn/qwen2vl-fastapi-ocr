import re
from typing import Optional

def normalize_passport_number(num: str, country_code: Optional[str] = None) -> Optional[str]:
    """
    Normalize passport number according to ICAO standards.
    
    This is a post-processing guard/sanitizer that cleans up passport numbers
    that may contain extra information returned by the AI model.
    
    Args:
        num: Raw passport number string from OCR/AI extraction
        country_code: Optional 3-letter country code to strip from end
        
    Returns:
        Normalized passport number (max 9 chars) or None if empty
    """
    if not num:
        return None
    
    # Remove non-alphanumeric characters except '<' (MRZ filler)
    s = re.sub(r'[^A-Z0-9<]', '', str(num).upper())
    
    # Strip MRZ fillers just in case
    s = s.replace('<', '')
    
    # Strip trailing nationality (e.g., USA) if present
    if country_code and isinstance(country_code, str) and s.endswith(country_code):
        s = s[: -len(country_code)]
    
    # Strip trailing single check digit if length==10
    if len(s) == 10 and s[-1].isdigit():
        s = s[:-1]
    
    # Keep only first 9 chars (ICAO field length)
    return s[:9] if s else None
