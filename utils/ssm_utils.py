import re
from typing import Dict, Any, Optional

def normalize_ssm_registration_numbers(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize SSM Form D registration numbers.
    
    This is a post-processing guard/sanitizer that properly splits the registration
    numbers that may be incorrectly combined by the AI model.
    
    Expected patterns:
    - "201934234321 (RT0069300-M)" -> registrationNumber: "201934234321", oldRegistrationNumber: "RT0069300-M"
    - "123456789012 (AB1234567-X)" -> registrationNumber: "123456789012", oldRegistrationNumber: "AB1234567-X"
    
    Args:
        data: Dictionary containing SSM form data
        
    Returns:
        Updated dictionary with normalized registration numbers
    """
    # Create a copy to avoid modifying the original
    normalized_data = data.copy()
    
    # Get the registration number field
    reg_num = normalized_data.get("registrationNumber")
    old_reg_num = normalized_data.get("oldRegistrationNumber")
    
    # Pattern to match: "12-digit number (OLD_FORMAT)"
    # Example: "201934234321 (RT0069300-M)"
    pattern = r'^(\d{12})\s*\(([^)]+)\)$'
    
    # Check if registrationNumber contains the combined format
    if reg_num and isinstance(reg_num, str):
        match = re.match(pattern, reg_num.strip())
        if match:
            new_reg_num = match.group(1)  # The 12-digit number
            old_reg_num_extracted = match.group(2)  # The part in parentheses
            
            normalized_data["registrationNumber"] = new_reg_num
            normalized_data["oldRegistrationNumber"] = old_reg_num_extracted
    
    # Also check oldRegistrationNumber in case it has the same issue
    elif old_reg_num and isinstance(old_reg_num, str):
        match = re.match(pattern, old_reg_num.strip())
        if match:
            new_reg_num = match.group(1)  # The 12-digit number
            old_reg_num_extracted = match.group(2)  # The part in parentheses
            
            normalized_data["registrationNumber"] = new_reg_num
            normalized_data["oldRegistrationNumber"] = old_reg_num_extracted
    
    return normalized_data

def clean_ssm_registration_number(reg_num: Optional[str]) -> Optional[str]:
    """
    Clean individual registration number by removing extra formatting.
    
    Args:
        reg_num: Raw registration number string
        
    Returns:
        Cleaned registration number or None if empty
    """
    if not reg_num:
        return None
    
    # Remove extra whitespace
    cleaned = str(reg_num).strip()
    
    # If it's just the old format in parentheses, extract it
    # Example: "(RT0069300-M)" -> "RT0069300-M"
    if cleaned.startswith('(') and cleaned.endswith(')'):
        cleaned = cleaned[1:-1]
    
    return cleaned if cleaned else None
