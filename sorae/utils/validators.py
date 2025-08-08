import re
from typing import Tuple, Optional
from datetime import datetime, timedelta

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format."""
    if not email:
        return False, "Email cannot be empty"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, None

def validate_token(token: str, expected_length: int = 8) -> Tuple[bool, Optional[str]]:
    """Validate magic link token format."""
    if not token:
        return False, "Token cannot be empty"
    
    if len(token) != expected_length:
        return False, f"Token must be {expected_length} characters long"
    
    # Check if token contains only alphanumeric characters
    if not re.match(r'^[a-zA-Z0-9]+$', token):
        return False, "Token contains invalid characters"
    
    return True, None

def validate_recovery_code(code: str, expected_length: int = 6) -> Tuple[bool, Optional[str]]:
    """Validate recovery code format."""
    if not code:
        return False, "Recovery code cannot be empty"
    
    if len(code) != expected_length:
        return False, f"Recovery code must be {expected_length} digits"
    
    # Check if code contains only digits
    if not re.match(r'^\d+$', code):
        return False, "Recovery code must contain only digits"
    
    return True, None

def validate_typing_pattern(pattern: float) -> Tuple[bool, Optional[str]]:
    """Validate typing pattern value."""
    if not isinstance(pattern, (int, float)):
        return False, "Typing pattern must be a number"
    
    if not 0 <= pattern <= 1:
        return False, "Typing pattern must be between 0 and 1"
    
    return True, None

def validate_device_id(device_id: str) -> Tuple[bool, Optional[str]]:
    """Validate device ID format."""
    if not device_id:
        return False, "Device ID cannot be empty"
    
    if len(device_id) < 3:
        return False, "Device ID must be at least 3 characters"
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', device_id):
        return False, "Device ID contains invalid characters"
    
    return True, None

def is_token_expired(created_at: datetime, expiry_seconds: int) -> bool:
    """Check if a token has expired."""
    if not created_at:
        return True
    
    expiry_time = created_at + timedelta(seconds=expiry_seconds)
    return datetime.now() > expiry_time

def sanitize_input(input_str: str, max_length: int = 100) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not input_str:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_user_input(input_data: dict) -> Tuple[bool, Optional[str]]:
    """Validate all user input data."""
    required_fields = ['email']
    
    for field in required_fields:
        if field not in input_data or not input_data[field]:
            return False, f"Missing required field: {field}"
    
    # Validate email
    is_valid, error = validate_email(input_data['email'])
    if not is_valid:
        return False, error
    
    # Validate optional fields if present
    if 'device_id' in input_data and input_data['device_id']:
        is_valid, error = validate_device_id(input_data['device_id'])
        if not is_valid:
            return False, error
    
    return True, None
