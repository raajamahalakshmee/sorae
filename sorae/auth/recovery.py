from ui.messaging import empathy_recovery_intro, empathy_recovery_success
from utils.validators import validate_recovery_code, sanitize_input
from utils.logger import logger, log_auth_event
from config import RECOVERY_CODE_LENGTH
from typing import Dict, Any, Optional

def recover_account(user: Dict[str, Any]) -> bool:
    """Recover user account with improved validation and security."""
    try:
        logger.info(f"Starting account recovery for user: {user.get('user_id')}")
        
        print(empathy_recovery_intro(user['email']))
        
        # Get backup codes from user data
        backup_codes = user.get('backup_codes', [])
        if not backup_codes:
            logger.error(f"No backup codes found for user: {user.get('user_id')}")
            print("❌ No backup codes found. Please contact support.")
            return False
        
        # Allow multiple attempts for recovery
        max_attempts = 3
        for attempt in range(max_attempts):
            code_input = input(f"Enter your {RECOVERY_CODE_LENGTH}-digit recovery code: ").strip()
            recovery_code = sanitize_input(code_input)
            
            # Validate recovery code format
            is_valid, error = validate_recovery_code(recovery_code, RECOVERY_CODE_LENGTH)
            if not is_valid:
                print(f"❌ {error}")
                if attempt < max_attempts - 1:
                    print(f"Please try again. ({max_attempts - attempt - 1} attempts remaining)")
                continue
            
            # Check if code matches any backup code
            if recovery_code in backup_codes:
                # Log successful recovery
                log_auth_event(
                    logger,
                    "recovery_successful",
                    user_id=user.get('user_id'),
                    email=user.get('email'),
                    success=True,
                    details=f"Attempt {attempt + 1}/{max_attempts}"
                )
                
                print(empathy_recovery_success())
                user['failed_attempts'] = 0
                user['last_login'] = datetime.now()
                
                # Remove used backup code for security
                backup_codes.remove(recovery_code)
                user['backup_codes'] = backup_codes
                
                if len(backup_codes) < 2:
                    print("⚠️ You're running low on backup codes. Consider generating new ones.")
                
                return True
            else:
                # Log failed recovery attempt
                log_auth_event(
                    logger,
                    "recovery_failed",
                    user_id=user.get('user_id'),
                    email=user.get('email'),
                    success=False,
                    details=f"Attempt {attempt + 1}/{max_attempts}"
                )
                
                print("❌ That recovery code doesn't match. Please try again.")
                if attempt < max_attempts - 1:
                    print(f"Please try again. ({max_attempts - attempt - 1} attempts remaining)")
        
        # All attempts failed
        print("❌ Maximum recovery attempts reached. Please contact support.")
        return False
        
    except KeyboardInterrupt:
        print("\n\n👋 Recovery cancelled. Come back anytime!")
        logger.info("User cancelled recovery process")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during account recovery: {e}")
        print("❌ An unexpected error occurred during recovery. Please try again.")
        return False

def generate_new_backup_codes(user: Dict[str, Any], count: int = 5) -> bool:
    """Generate new backup codes for the user."""
    try:
        from auth.onboarding import generate_backup_codes
        
        new_codes = generate_backup_codes(count, RECOVERY_CODE_LENGTH)
        user['backup_codes'] = new_codes
        
        logger.info(f"Generated new backup codes for user: {user.get('user_id')}")
        print(f"🔑 New backup codes generated: {', '.join(new_codes)}")
        print("💡 Keep these codes safe and secure!")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate new backup codes: {e}")
        print("❌ Failed to generate new backup codes. Please try again.")
        return False

def check_backup_codes_status(user: Dict[str, Any]) -> Dict[str, Any]:
    """Check the status of user's backup codes."""
    backup_codes = user.get('backup_codes', [])
    total_codes = len(backup_codes)
    
    status = {
        'total_codes': total_codes,
        'codes_remaining': total_codes,
        'status': 'good' if total_codes >= 3 else 'low' if total_codes >= 1 else 'critical'
    }
    
    return status

# Import datetime for the recovery function
from datetime import datetime
