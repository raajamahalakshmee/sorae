import os
from typing import Dict, Any

# Authentication Settings
MAGIC_LINK_EXPIRY_SECONDS = int(os.getenv('MAGIC_LINK_EXPIRY_SECONDS', 900))  # 15 min
MAX_FAILED_ATTEMPTS = int(os.getenv('MAX_FAILED_ATTEMPTS', 5))
BIOMETRIC_THRESHOLD = float(os.getenv('BIOMETRIC_THRESHOLD', 0.15))  # Lower threshold is more strict
RISK_SCORE_THRESHOLD = float(os.getenv('RISK_SCORE_THRESHOLD', 0.5))  # If risk exceeds this, step up security

# Security Settings
RATE_LIMIT_ATTEMPTS = int(os.getenv('RATE_LIMIT_ATTEMPTS', 3))
RATE_LIMIT_WINDOW_MINUTES = int(os.getenv('RATE_LIMIT_WINDOW_MINUTES', 15))
SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))

# Recovery Settings
RECOVERY_CODE_LENGTH = int(os.getenv('RECOVERY_CODE_LENGTH', 6))
BACKUP_CODES_COUNT = int(os.getenv('BACKUP_CODES_COUNT', 5))

# Email Settings
EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@sorae.com')
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'Your Sorae Magic Link')

# Demo Mode
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'

# Validation
def validate_config() -> Dict[str, Any]:
    """Validate configuration values and return any issues."""
    issues = []
    
    if MAGIC_LINK_EXPIRY_SECONDS < 60:
        issues.append("MAGIC_LINK_EXPIRY_SECONDS should be at least 60 seconds")
    
    if MAX_FAILED_ATTEMPTS < 1:
        issues.append("MAX_FAILED_ATTEMPTS should be at least 1")
    
    if not 0 < BIOMETRIC_THRESHOLD < 1:
        issues.append("BIOMETRIC_THRESHOLD should be between 0 and 1")
    
    if not 0 < RISK_SCORE_THRESHOLD < 1:
        issues.append("RISK_SCORE_THRESHOLD should be between 0 and 1")
    
    return {"valid": len(issues) == 0, "issues": issues}

# Get all config as dict
def get_config() -> Dict[str, Any]:
    """Return all configuration as a dictionary."""
    return {
        'magic_link_expiry_seconds': MAGIC_LINK_EXPIRY_SECONDS,
        'max_failed_attempts': MAX_FAILED_ATTEMPTS,
        'biometric_threshold': BIOMETRIC_THRESHOLD,
        'risk_score_threshold': RISK_SCORE_THRESHOLD,
        'rate_limit_attempts': RATE_LIMIT_ATTEMPTS,
        'rate_limit_window_minutes': RATE_LIMIT_WINDOW_MINUTES,
        'session_timeout_minutes': SESSION_TIMEOUT_MINUTES,
        'recovery_code_length': RECOVERY_CODE_LENGTH,
        'backup_codes_count': BACKUP_CODES_COUNT,
        'email_from': EMAIL_FROM,
        'email_subject': EMAIL_SUBJECT,
        'demo_mode': DEMO_MODE
    }
