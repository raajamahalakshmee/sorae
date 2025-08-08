from auth.onboarding import start_onboarding, validate_onboarding_data
from auth.authentication import login_user, validate_user_session
from auth.recovery import recover_account, check_backup_codes_status
from ui.messaging import welcome_message
from config import validate_config, get_config
from utils.logger import logger
import sys
from typing import Optional, Dict, Any

def validate_environment() -> bool:
    """Validate the application environment and configuration."""
    try:
        # Validate configuration
        config_validation = validate_config()
        if not config_validation['valid']:
            print("❌ Configuration validation failed:")
            for issue in config_validation['issues']:
                print(f"   - {issue}")
            return False
        
        logger.info("Environment validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Environment validation failed: {e}")
        print(f"❌ Environment validation failed: {e}")
        return False

def display_config_summary():
    """Display a summary of the current configuration."""
    config = get_config()
    print("\n📋 Configuration Summary:")
    print(f"   • Magic link expiry: {config['magic_link_expiry_seconds']} seconds")
    print(f"   • Max failed attempts: {config['max_failed_attempts']}")
    print(f"   • Biometric threshold: {config['biometric_threshold']}")
    print(f"   • Risk score threshold: {config['risk_score_threshold']}")
    print(f"   • Recovery code length: {config['recovery_code_length']}")
    print(f"   • Backup codes count: {config['backup_codes_count']}")

def main() -> int:
    """Main application entry point with improved error handling."""
    try:
        # Setup logging
        logger.info("Starting Sorae authentication application")
        
        # Validate environment
        if not validate_environment():
            return 1
        
        # Display welcome and config
        print(welcome_message())
        display_config_summary()
        
        # Onboarding phase
        print("\n--- Onboarding Phase ---")
        user = start_onboarding()
        
        if not user:
            print("❌ Onboarding failed or was cancelled.")
            return 1
        
        # Validate onboarding data
        if not validate_onboarding_data(user):
            logger.error("Invalid user data after onboarding")
            print("❌ Invalid user data generated during onboarding.")
            return 1
        
        # Login phase
        print("\n--- Login Phase ---")
        is_authenticated = login_user(user)
        
        if is_authenticated:
            print("🎉 You're securely authenticated. Enjoy your session with Sorae!")
            
            # Check backup codes status
            status = check_backup_codes_status(user)
            if status['status'] == 'low':
                print(f"⚠️ You have {status['codes_remaining']} backup codes remaining.")
            elif status['status'] == 'critical':
                print("🚨 You're running low on backup codes. Consider generating new ones.")
            
            return 0
        else:
            print("🔒 Authentication failed. Consider account recovery.")
            
            # Offer recovery
            try:
                recovery_choice = input("Would you like to try account recovery? (y/n): ").strip().lower()
                if recovery_choice in ['y', 'yes']:
                    recovery_success = recover_account(user)
                    if recovery_success:
                        print("🎉 Account recovered successfully!")
                        return 0
                    else:
                        print("❌ Account recovery failed.")
                        return 1
                else:
                    print("👋 Goodbye! Come back anytime.")
                    return 0
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Come back anytime.")
                return 0
                
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error in main application: {e}")
        print(f"❌ An unexpected error occurred: {e}")
        print("Please check the logs for more details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
