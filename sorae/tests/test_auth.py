import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from auth.onboarding import start_onboarding, validate_onboarding_data, generate_backup_codes
from auth.authentication import login_user, check_rate_limit, check_token_expiry, validate_user_session
from auth.recovery import recover_account, check_backup_codes_status, generate_new_backup_codes
from utils.validators import validate_email, validate_token, validate_recovery_code, is_token_expired

class TestOnboarding(unittest.TestCase):
    def test_generate_backup_codes(self):
        """Test backup code generation."""
        codes = generate_backup_codes(3, 4)
        self.assertEqual(len(codes), 3)
        for code in codes:
            self.assertEqual(len(code), 4)
            self.assertTrue(code.isdigit())
    
    def test_validate_onboarding_data_valid(self):
        """Test validation of valid onboarding data."""
        user_data = {
            'user_id': 'test-id',
            'email': 'test@example.com',
            'typing_profile': 0.5,
            'known_devices': ['device1'],
            'current_device': 'device1',
            'token': '12345678',
            'token_created_at': datetime.now(),
            'failed_attempts': 0,
            'backup_codes': ['123456', '654321'],
            'created_at': datetime.now()
        }
        self.assertTrue(validate_onboarding_data(user_data))
    
    def test_validate_onboarding_data_invalid(self):
        """Test validation of invalid onboarding data."""
        user_data = {
            'user_id': 'test-id',
            'email': 'invalid-email',
            'typing_profile': 1.5,  # Invalid
            'known_devices': ['device1'],
            'current_device': 'device1',
            'token': '12345678',
            'token_created_at': datetime.now(),
            'failed_attempts': -1,  # Invalid
            'backup_codes': ['123456', '654321'],
            'created_at': datetime.now()
        }
        self.assertFalse(validate_onboarding_data(user_data))

class TestAuthentication(unittest.TestCase):
    def test_check_rate_limit_valid(self):
        """Test rate limit check with valid attempts."""
        user = {'failed_attempts': 2}
        self.assertTrue(check_rate_limit(user))
    
    def test_check_rate_limit_exceeded(self):
        """Test rate limit check with exceeded attempts."""
        user = {'failed_attempts': 6}
        self.assertFalse(check_rate_limit(user))
    
    def test_check_token_expiry_valid(self):
        """Test token expiry check with valid token."""
        user = {'token_created_at': datetime.now()}
        self.assertTrue(check_token_expiry(user))
    
    def test_check_token_expiry_expired(self):
        """Test token expiry check with expired token."""
        user = {'token_created_at': datetime.now() - timedelta(hours=1)}
        self.assertFalse(check_token_expiry(user))
    
    def test_validate_user_session_valid(self):
        """Test user session validation with valid data."""
        user = {
            'user_id': 'test-id',
            'email': 'test@example.com',
            'typing_profile': 0.5,
            'known_devices': ['device1'],
            'current_device': 'device1',
            'token': '12345678',
            'token_created_at': datetime.now(),
            'failed_attempts': 0
        }
        self.assertTrue(validate_user_session(user))
    
    def test_validate_user_session_invalid(self):
        """Test user session validation with invalid data."""
        user = {
            'user_id': 'test-id',
            'email': 'test@example.com',
            'typing_profile': 1.5,  # Invalid
            'known_devices': ['device1'],
            'current_device': 'device1',
            'token': '12345678',
            'token_created_at': datetime.now(),
            'failed_attempts': -1  # Invalid
        }
        self.assertFalse(validate_user_session(user))

class TestRecovery(unittest.TestCase):
    def test_check_backup_codes_status_good(self):
        """Test backup codes status with good number of codes."""
        user = {'backup_codes': ['123456', '654321', '789012']}
        status = check_backup_codes_status(user)
        self.assertEqual(status['total_codes'], 3)
        self.assertEqual(status['status'], 'good')
    
    def test_check_backup_codes_status_low(self):
        """Test backup codes status with low number of codes."""
        user = {'backup_codes': ['123456']}
        status = check_backup_codes_status(user)
        self.assertEqual(status['total_codes'], 1)
        self.assertEqual(status['status'], 'low')
    
    def test_check_backup_codes_status_critical(self):
        """Test backup codes status with no codes."""
        user = {'backup_codes': []}
        status = check_backup_codes_status(user)
        self.assertEqual(status['total_codes'], 0)
        self.assertEqual(status['status'], 'critical')

class TestValidators(unittest.TestCase):
    def test_validate_email_valid(self):
        """Test email validation with valid email."""
        is_valid, error = validate_email('test@example.com')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid email."""
        is_valid, error = validate_email('invalid-email')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_token_valid(self):
        """Test token validation with valid token."""
        is_valid, error = validate_token('12345678')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_token_invalid(self):
        """Test token validation with invalid token."""
        is_valid, error = validate_token('123')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_recovery_code_valid(self):
        """Test recovery code validation with valid code."""
        is_valid, error = validate_recovery_code('123456')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_recovery_code_invalid(self):
        """Test recovery code validation with invalid code."""
        is_valid, error = validate_recovery_code('123')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_is_token_expired_valid(self):
        """Test token expiry check with valid token."""
        created_at = datetime.now()
        self.assertFalse(is_token_expired(created_at, 900))
    
    def test_is_token_expired_expired(self):
        """Test token expiry check with expired token."""
        created_at = datetime.now() - timedelta(hours=1)
        self.assertTrue(is_token_expired(created_at, 900))

if __name__ == "__main__":
    unittest.main()
