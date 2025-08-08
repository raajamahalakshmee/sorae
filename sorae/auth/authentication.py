from utils.biometrics_simulator import simulate_typing_pattern, match_typing_pattern
from utils.risk_assessment import assess_risk
from utils.validators import validate_token, validate_typing_pattern, is_token_expired, sanitize_input
from utils.logger import logger, log_auth_event, log_security_event
from ui.messaging import empathetic_login_greeting, error_message
from config import BIOMETRIC_THRESHOLD, RISK_SCORE_THRESHOLD, MAX_FAILED_ATTEMPTS, MAGIC_LINK_EXPIRY_SECONDS, DEMO_MODE
from datetime import datetime
from typing import Dict, Any, Optional

def check_rate_limit(user: Dict[str, Any]) -> bool:
    """Check if user has exceeded rate limits."""
    failed_attempts = user.get('failed_attempts', 0)
    return failed_attempts < MAX_FAILED_ATTEMPTS

def check_token_expiry(user: Dict[str, Any]) -> bool:
    """Check if the magic link token has expired."""
    token_created_at = user.get('token_created_at')
    if not token_created_at:
        return False
    
    return not is_token_expired(token_created_at, MAGIC_LINK_EXPIRY_SECONDS)

def login_user(user: Dict[str, Any]) -> bool:
    """Authenticate user with improved validation and security features."""
    try:
        logger.info(f"Starting authentication for user: {user.get('user_id')}")
        
        # Check rate limiting
        if not check_rate_limit(user):
            logger.warning(f"Rate limit exceeded for user: {user.get('user_id')}")
            print("🔒 Too many failed attempts. Please try again later or use account recovery.")
            return False
        
        # Check token expiry
        if not check_token_expiry(user):
            logger.warning(f"Token expired for user: {user.get('user_id')}")
            print("⏰ Your magic link has expired. Please request a new one.")
            return False
        
        print(empathetic_login_greeting(user['email']))
        
        # Simulate device ID (here, always device1 for demo)
        device_id = user['current_device']
        known_devices = user['known_devices']
        
        # Magic link flow with validation
        max_token_attempts = 3
        for attempt in range(max_token_attempts):
            token_input = input("Enter the magic link token from your inbox: ").strip()
            token_attempt = sanitize_input(token_input)
            
            is_valid, error = validate_token(token_attempt)
            if not is_valid:
                print(f"❌ {error}")
                if attempt < max_token_attempts - 1:
                    print(f"Please try again. ({max_token_attempts - attempt - 1} attempts remaining)")
                continue
            
            if token_attempt != user['token']:
                print(error_message("token"))
                user['failed_attempts'] += 1
                
                # Log failed attempt
                log_auth_event(
                    logger,
                    "login_failed_token",
                    user_id=user.get('user_id'),
                    email=user.get('email'),
                    success=False,
                    details=f"Attempt {attempt + 1}/{max_token_attempts}"
                )
                
                if attempt < max_token_attempts - 1:
                    print(f"Please try again. ({max_token_attempts - attempt - 1} attempts remaining)")
                else:
                    print("❌ Maximum token attempts reached.")
                    return False
            else:
                break
        else:
            return False
        
        # Simulate typing biometrics capture
        print("Let's quickly verify your typing pattern for enhanced security.")
        new_pattern = simulate_typing_pattern()
        
        # Validate typing pattern
        is_valid, error = validate_typing_pattern(new_pattern)
        if not is_valid:
            logger.error(f"Invalid typing pattern generated: {new_pattern}")
            print("❌ Failed to capture typing pattern. Please try again.")
            return False
        
        # DEMO_MODE: Always succeed biometrics for demo/testing
        if DEMO_MODE:
            is_pattern_valid = True  # Always succeed in demo mode
        else:
            is_pattern_valid = match_typing_pattern(user['typing_profile'], new_pattern, BIOMETRIC_THRESHOLD)
        
        # Assess risk
        risk = assess_risk(device_id, known_devices, user['failed_attempts'])
        
        # Log risk assessment
        if risk > RISK_SCORE_THRESHOLD:
            log_security_event(
                logger,
                "high_risk_login",
                user_id=user.get('user_id'),
                risk_score=risk,
                details=f"Device: {device_id}, Failed attempts: {user['failed_attempts']}"
            )
            print("⚠️ New device or unusual activity detected. We'll ask for extra verification next time.")
        
        if is_pattern_valid:
            # Reset failed attempts on successful login
            user['failed_attempts'] = 0
            user['last_login'] = datetime.now()
            
            # Log successful login
            log_auth_event(
                logger,
                "login_successful",
                user_id=user.get('user_id'),
                email=user.get('email'),
                success=True,
                details=f"Device: {device_id}, Risk score: {risk:.2f}"
            )
            
            print("✅ Typing pattern matched! Secure, smooth login. 🟢")
            return True
        else:
            user['failed_attempts'] += 1
            
            # Log failed biometrics
            log_auth_event(
                logger,
                "login_failed_biometrics",
                user_id=user.get('user_id'),
                email=user.get('email'),
                success=False,
                details=f"Pattern difference: {abs(user['typing_profile'] - new_pattern):.2f}"
            )
            
            print(error_message("biometrics"))
            return False
            
    except KeyboardInterrupt:
        print("\n\n👋 Login cancelled. Come back anytime!")
        logger.info("User cancelled login process")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        print("❌ An unexpected error occurred during login. Please try again.")
        return False

def validate_user_session(user: Dict[str, Any]) -> bool:
    """Validate that user session data is complete and valid."""
    required_fields = [
        'user_id', 'email', 'typing_profile', 'known_devices', 
        'current_device', 'token', 'token_created_at', 'failed_attempts'
    ]
    
    for field in required_fields:
        if field not in user:
            logger.error(f"Missing required field in user session: {field}")
            return False
    
    # Validate specific fields
    if user['failed_attempts'] < 0:
        logger.error("Invalid failed attempts count in user session")
        return False
    
    if not 0 <= user['typing_profile'] <= 1:
        logger.error("Invalid typing profile in user session")
        return False
    
    return True
