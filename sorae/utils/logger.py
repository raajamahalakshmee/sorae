import logging
import sys
from datetime import datetime
from typing import Optional

def setup_logger(name: str = "sorae", level: int = logging.INFO) -> logging.Logger:
    """Setup and configure logger for the application."""
    logger = logging.getLogger(name)
    
    if logger.handlers:  # Avoid adding handlers multiple times
        return logger
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # File handler
    try:
        file_handler = logging.FileHandler(f'logs/sorae_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except FileNotFoundError:
        # Create logs directory if it doesn't exist
        import os
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler(f'logs/sorae_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.addHandler(console_handler)
    
    return logger

def log_auth_event(logger: logging.Logger, event: str, user_id: Optional[str] = None, 
                   email: Optional[str] = None, success: bool = True, details: Optional[str] = None):
    """Log authentication events with consistent formatting."""
    message = f"AUTH_EVENT: {event} | User: {user_id or 'unknown'} | Email: {email or 'unknown'} | Success: {success}"
    if details:
        message += f" | Details: {details}"
    
    if success:
        logger.info(message)
    else:
        logger.warning(message)

def log_security_event(logger: logging.Logger, event: str, user_id: Optional[str] = None,
                      risk_score: Optional[float] = None, details: Optional[str] = None):
    """Log security events with consistent formatting."""
    message = f"SECURITY_EVENT: {event} | User: {user_id or 'unknown'}"
    if risk_score is not None:
        message += f" | Risk Score: {risk_score:.2f}"
    if details:
        message += f" | Details: {details}"
    
    logger.warning(message)

# Create default logger instance
logger = setup_logger()
