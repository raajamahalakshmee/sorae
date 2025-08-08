import unittest
from unittest.mock import patch, MagicMock
from utils import biometrics_simulator, risk_assessment, email_simulator
from utils.validators import (
    validate_email, validate_token, validate_recovery_code, 
    validate_typing_pattern, validate_device_id, is_token_expired,
    sanitize_input, validate_user_input
)
from utils.logger import setup_logger, log_auth_event, log_security_event
from datetime import datetime, timedelta

class TestBiometricsSimulator(unittest.TestCase):
    def test_typing_pattern_range(self):
        """Test that enrolled typing pattern is within valid range."""
        enrolled = biometrics_simulator.enroll_typing_pattern()
        self.assertTrue(0 <= enrolled <= 1)
    
    def test_match_typing_pattern_success(self):
        """Test successful typing pattern matching."""
        p1 = 0.5
        p2 = 0.55
        threshold = 0.1
        self.assertTrue(biometrics_simulator.match_typing_pattern(p1, p2, threshold))
    
    def test_match_typing_pattern_failure(self):
        """Test failed typing pattern matching."""
        p1 = 0.5
        p2 = 0.8
        threshold = 0.1
        self.assertFalse(biometrics_simulator.match_typing_pattern(p1, p2, threshold))
    
    def test_simulate_typing_pattern_range(self):
        """Test that simulated typing pattern is within valid range."""
        pattern = biometrics_simulator.simulate_typing_pattern()
        self.assertTrue(0 <= pattern <= 1)

class TestRiskAssessment(unittest.TestCase):
    def test_assess_risk_new_device(self):
        """Test risk assessment for new device."""
        risk = risk_assessment.assess_risk("new_device", ["old_device"], 0)
        self.assertGreaterEqual(risk, 0.6)
    
    def test_assess_risk_known_device(self):
        """Test risk assessment for known device."""
        risk = risk_assessment.assess_risk("known_device", ["known_device"], 0)
        self.assertEqual(risk, 0.0)
    
    def test_assess_risk_failed_attempts(self):
        """Test risk assessment with failed attempts."""
        risk = risk_assessment.assess_risk("known_device", ["known_device"], 3)
        self.assertGreaterEqual(risk, 0.2)
    
    def test_assess_risk_combined(self):
        """Test risk assessment with both new device and failed attempts."""
        risk = risk_assessment.assess_risk("new_device", ["old_device"], 3)
        self.assertGreaterEqual(risk, 0.8)

class TestEmailSimulator(unittest.TestCase):
    def test_send_magic_link_no_exception(self):
        """Test that email simulator runs without exception."""
        try:
            email_simulator.send_magic_link("test@demo.com", "token42")
        except Exception as e:
            self.fail(f"Exception in send_magic_link: {e}")
    
    def test_send_magic_link_with_special_chars(self):
        """Test email simulator with special characters in email."""
        try:
            email_simulator.send_magic_link("test+tag@demo.com", "token42")
        except Exception as e:
            self.fail(f"Exception in send_magic_link with special chars: {e}")

class TestValidators(unittest.TestCase):
    def test_validate_email_valid_formats(self):
        """Test email validation with various valid formats."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com"
        ]
        for email in valid_emails:
            is_valid, error = validate_email(email)
            self.assertTrue(is_valid, f"Email {email} should be valid")
            self.assertIsNone(error)
    
    def test_validate_email_invalid_formats(self):
        """Test email validation with various invalid formats."""
        invalid_emails = [
            "",
            "invalid-email",
            "@example.com",
            "test@",
            "test@.com",
            "test..test@example.com"
        ]
        for email in invalid_emails:
            is_valid, error = validate_email(email)
            self.assertFalse(is_valid, f"Email {email} should be invalid")
            self.assertIsNotNone(error)
    
    def test_validate_token_valid_formats(self):
        """Test token validation with valid formats."""
        valid_tokens = ["12345678", "abcdef12", "ABC12345"]
        for token in valid_tokens:
            is_valid, error = validate_token(token)
            self.assertTrue(is_valid, f"Token {token} should be valid")
            self.assertIsNone(error)
    
    def test_validate_token_invalid_formats(self):
        """Test token validation with invalid formats."""
        invalid_tokens = ["", "123", "123456789", "1234567@", "1234567 "]
        for token in invalid_tokens:
            is_valid, error = validate_token(token)
            self.assertFalse(is_valid, f"Token {token} should be invalid")
            self.assertIsNotNone(error)
    
    def test_validate_recovery_code_valid_formats(self):
        """Test recovery code validation with valid formats."""
        valid_codes = ["123456", "000000", "999999"]
        for code in valid_codes:
            is_valid, error = validate_recovery_code(code)
            self.assertTrue(is_valid, f"Code {code} should be valid")
            self.assertIsNone(error)
    
    def test_validate_recovery_code_invalid_formats(self):
        """Test recovery code validation with invalid formats."""
        invalid_codes = ["", "123", "1234567", "12345a", "12345 "]
        for code in invalid_codes:
            is_valid, error = validate_recovery_code(code)
            self.assertFalse(is_valid, f"Code {code} should be invalid")
            self.assertIsNotNone(error)
    
    def test_validate_typing_pattern_valid(self):
        """Test typing pattern validation with valid values."""
        valid_patterns = [0.0, 0.5, 1.0, 0.123]
        for pattern in valid_patterns:
            is_valid, error = validate_typing_pattern(pattern)
            self.assertTrue(is_valid, f"Pattern {pattern} should be valid")
            self.assertIsNone(error)
    
    def test_validate_typing_pattern_invalid(self):
        """Test typing pattern validation with invalid values."""
        invalid_patterns = [-0.1, 1.1, "0.5", None]
        for pattern in invalid_patterns:
            is_valid, error = validate_typing_pattern(pattern)
            self.assertFalse(is_valid, f"Pattern {pattern} should be invalid")
            self.assertIsNotNone(error)
    
    def test_validate_device_id_valid(self):
        """Test device ID validation with valid formats."""
        valid_ids = ["device1", "my-device", "device_123", "DEVICE1"]
        for device_id in valid_ids:
            is_valid, error = validate_device_id(device_id)
            self.assertTrue(is_valid, f"Device ID {device_id} should be valid")
            self.assertIsNone(error)
    
    def test_validate_device_id_invalid(self):
        """Test device ID validation with invalid formats."""
        invalid_ids = ["", "ab", "device@123", "device 123", "device#123"]
        for device_id in invalid_ids:
            is_valid, error = validate_device_id(device_id)
            self.assertFalse(is_valid, f"Device ID {device_id} should be invalid")
            self.assertIsNotNone(error)
    
    def test_is_token_expired(self):
        """Test token expiry checking."""
        now = datetime.now()
        
        # Valid token (not expired)
        self.assertFalse(is_token_expired(now, 900))
        
        # Expired token
        expired_time = now - timedelta(hours=1)
        self.assertTrue(is_token_expired(expired_time, 900))
        
        # No creation time
        self.assertTrue(is_token_expired(None, 900))
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        # Test removal of dangerous characters
        dangerous_input = "<script>alert('xss')</script>"
        sanitized = sanitize_input(dangerous_input)
        self.assertNotIn("<", sanitized)
        self.assertNotIn(">", sanitized)
        self.assertNotIn("'", sanitized)
        self.assertNotIn('"', sanitized)
        
        # Test length limiting
        long_input = "a" * 200
        sanitized = sanitize_input(long_input, max_length=100)
        self.assertEqual(len(sanitized), 100)
        
        # Test empty input
        self.assertEqual(sanitize_input(""), "")
        self.assertEqual(sanitize_input(None), "")
    
    def test_validate_user_input_valid(self):
        """Test user input validation with valid data."""
        valid_input = {"email": "test@example.com"}
        is_valid, error = validate_user_input(valid_input)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_user_input_invalid(self):
        """Test user input validation with invalid data."""
        invalid_inputs = [
            {},  # Missing email
            {"email": ""},  # Empty email
            {"email": "invalid-email"}  # Invalid email format
        ]
        for input_data in invalid_inputs:
            is_valid, error = validate_user_input(input_data)
            self.assertFalse(is_valid)
            self.assertIsNotNone(error)

class TestLogger(unittest.TestCase):
    def test_setup_logger(self):
        """Test logger setup."""
        logger = setup_logger("test_logger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")
    
    def test_log_auth_event(self):
        """Test authentication event logging."""
        logger = setup_logger("test_auth_logger")
        # This should not raise an exception
        log_auth_event(logger, "test_event", user_id="test_user", email="test@example.com", success=True)
    
    def test_log_security_event(self):
        """Test security event logging."""
        logger = setup_logger("test_security_logger")
        # This should not raise an exception
        log_security_event(logger, "test_event", user_id="test_user", risk_score=0.5)

if __name__ == "__main__":
    unittest.main()
