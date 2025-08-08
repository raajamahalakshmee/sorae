from utils.biometrics_simulator import enroll_typing_pattern
from utils.email_service import email_service
from utils.validators import validate_email, sanitize_input, validate_user_input
from utils.logger import logger, log_auth_event
from config import RECOVERY_CODE_LENGTH, BACKUP_CODES_COUNT, get_config
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

def generate_backup_codes(count: int = 5, length: int = 6) -> list:
    """Generate backup recovery codes."""
    import random
    codes = []
    for _ in range(count):
        code = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        codes.append(code)
    return codes

def start_onboarding() -> Optional[Dict[str, Any]]:
    """Start the user onboarding process with improved validation and error handling."""
    try:
        logger.info("Starting user onboarding process")
        
        # Get user email with validation
        while True:
            email_input = input("Enter your email to begin onboarding: ").strip()
            email = sanitize_input(email_input)
            
            is_valid, error = validate_email(email)
            if is_valid:
                break
            else:
                print(f"❌ {error}")
                print("Please enter a valid email address.")
        
        # Enroll typing pattern
        print("Enrolling your unique typing pattern for passwordless security…")
        typing_profile = enroll_typing_pattern()
        
        # Validate typing profile
        if not 0 <= typing_profile <= 1:
            logger.error(f"Invalid typing profile generated: {typing_profile}")
            print("❌ Failed to enroll typing pattern. Please try again.")
            return None
        
        # Generate user ID and device info
        user_id = str(uuid.uuid4())
        device_id = "device1"  # Normally, you'd detect this from the environment
        
        # Generate magic link token
        token = str(uuid.uuid4())[:8]
        token_created_at = datetime.now()
        
        # Generate backup codes
        backup_codes = generate_backup_codes(BACKUP_CODES_COUNT, RECOVERY_CODE_LENGTH)
        
        # Send magic link using email service
        try:
            email_sent = email_service.send_magic_link(email, token)
            if email_sent:
                print(f"\n📧 Magic link sent to {email}. Please check your inbox!")
                print(f"🔑 Your backup codes: {', '.join(backup_codes)}")
                print("💡 Keep these codes safe - you'll need them if you lose access to your email.")
            else:
                print("❌ Failed to send magic link. Please try again.")
                return None
        except Exception as e:
            logger.error(f"Failed to send magic link: {e}")
            print("❌ Failed to send magic link. Please try again.")
            return None
        
        # Create user profile
        user_profile = {
            "user_id": user_id,
            "email": email,
            "typing_profile": typing_profile,
            "known_devices": [device_id],
            "current_device": device_id,
            "token": token,
            "token_created_at": token_created_at,
            "failed_attempts": 0,
            "backup_codes": backup_codes,
            "created_at": datetime.now(),
            "last_login": None
        }
        
        # Log successful onboarding
        log_auth_event(
            logger, 
            "onboarding_completed", 
            user_id=user_id, 
            email=email, 
            success=True,
            details=f"Device: {device_id}, Backup codes generated: {len(backup_codes)}"
        )
        
        print("✅ Onboarding completed successfully!")
        return user_profile
        
    except KeyboardInterrupt:
        print("\n\n👋 Onboarding cancelled. Come back anytime!")
        logger.info("User cancelled onboarding process")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during onboarding: {e}")
        print("❌ An unexpected error occurred. Please try again.")
        return None

def validate_onboarding_data(user_data: Dict[str, Any]) -> bool:
    """Validate the user data created during onboarding."""
    required_fields = [
        'user_id', 'email', 'typing_profile', 'known_devices', 
        'current_device', 'token', 'token_created_at', 'failed_attempts',
        'backup_codes', 'created_at'
    ]
    
    for field in required_fields:
        if field not in user_data:
            logger.error(f"Missing required field in user data: {field}")
            return False
    
    # Validate specific fields
    if not validate_email(user_data['email'])[0]:
        logger.error("Invalid email in user data")
        return False
    
    if not 0 <= user_data['typing_profile'] <= 1:
        logger.error("Invalid typing profile in user data")
        return False
    
    if user_data['failed_attempts'] < 0:
        logger.error("Invalid failed attempts count in user data")
        return False
    
    return True
