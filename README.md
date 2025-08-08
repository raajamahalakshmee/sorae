# Sorae - Empathy-Driven Passwordless Authentication

Sorae is a secure, user-friendly passwordless authentication system that prioritizes user experience while maintaining robust security standards. The system uses magic links, biometric typing patterns, and backup recovery codes to provide a seamless authentication experience.

## 🌟 Features

### Security Features
- **Magic Link Authentication**: Secure, time-limited tokens sent via email
- **Biometric Typing Patterns**: Continuous authentication through typing behavior analysis
- **Risk Assessment**: Real-time security evaluation based on device, location, and behavior
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Comprehensive validation and sanitization of all user inputs
- **Backup Recovery Codes**: Secure fallback authentication method

### User Experience Features
- **Empathetic Messaging**: User-friendly, supportive communication throughout the process
- **Graceful Error Handling**: Clear, helpful error messages and recovery options
- **Progressive Security**: Step-up authentication for high-risk scenarios
- **Session Management**: Secure session handling with configurable timeouts

### Developer Features
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Extensive Testing**: Full test coverage with pytest
- **Configuration Management**: Environment-based configuration with validation
- **Type Hints**: Full type annotation for better code maintainability
- **Demo Mode**: Instantly succeed at biometrics for demos/testing (see below)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sorae
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Configuration

The application uses environment variables for configuration. You can set these in your environment or create a `.env` file:

```bash
# Authentication Settings
MAGIC_LINK_EXPIRY_SECONDS=900
MAX_FAILED_ATTEMPTS=5
BIOMETRIC_THRESHOLD=0.15
RISK_SCORE_THRESHOLD=0.5

# Security Settings
RATE_LIMIT_ATTEMPTS=3
RATE_LIMIT_WINDOW_MINUTES=15
SESSION_TIMEOUT_MINUTES=30

# Recovery Settings
RECOVERY_CODE_LENGTH=6
BACKUP_CODES_COUNT=5

# Email Settings
EMAIL_FROM=noreply@sorae.com
EMAIL_SUBJECT=Your Sorae Magic Link

# DEMO MODE (set to 'true' to always succeed at biometrics)
DEMO_MODE=true
```

## 🖥️ Demo Mode

**Demo Mode** allows you to always succeed at the typing pattern (biometrics) step, making it easy to demonstrate or test the full login flow without random failures.

- To enable demo mode, set the environment variable:
  ```bash
  # PowerShell
  $env:DEMO_MODE="true"
  # Command Prompt
  set DEMO_MODE=true
  # .env file
  DEMO_MODE=true
  ```
- When enabled, the biometrics check will always pass if the magic link is correct.
- Set `DEMO_MODE=false` (or unset) to return to realistic, random biometrics.

## 📁 Project Structure

```
sorae/
├── auth/                    # Authentication modules
│   ├── __init__.py
│   ├── authentication.py    # Login and session management
│   ├── onboarding.py       # User registration and setup
│   └── recovery.py         # Account recovery functionality
├── ui/                     # User interface components
│   ├── __init__.py
│   └── messaging.py        # Empathetic user messages
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── biometrics_simulator.py  # Typing pattern simulation
│   ├── email_simulator.py       # Email sending simulation
│   ├── risk_assessment.py       # Security risk evaluation
│   ├── validators.py            # Input validation utilities
│   └── logger.py               # Logging configuration
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_auth.py        # Authentication tests
│   └── test_utils.py       # Utility tests
├── config.py               # Configuration management
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test Files
```bash
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_utils.py -v
```

## 🔧 Development

### Code Quality Tools

1. **Format code with Black**
   ```bash
   black .
   ```

2. **Lint code with flake8**
   ```bash
   flake8 .
   ```

3. **Type checking with mypy**
   ```bash
   mypy .
   ```

### Adding New Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first** (TDD approach)
   ```bash
   # Add tests in tests/test_auth.py or tests/test_utils.py
   ```

3. **Implement the feature**
   ```bash
   # Add your code in the appropriate module
   ```

4. **Run tests and quality checks**
   ```bash
   python -m pytest tests/ -v
   black .
   flake8 .
   mypy .
   ```

## 🔒 Security Considerations

### Authentication Flow
1. **Onboarding**: User provides email, system enrolls typing pattern
2. **Magic Link**: Secure token sent to user's email
3. **Biometric Verification**: Typing pattern validation during login
4. **Risk Assessment**: Real-time security evaluation
5. **Recovery**: Backup codes for account recovery

### Security Features
- **Input Sanitization**: All user inputs are sanitized to prevent injection attacks
- **Rate Limiting**: Failed attempts are tracked and limited
- **Token Expiration**: Magic links expire after configurable time
- **Session Management**: Secure session handling with timeouts
- **Comprehensive Logging**: All security events are logged for monitoring

## 📊 Monitoring and Logging

The application provides comprehensive logging for monitoring and debugging:

- **Authentication Events**: Login attempts, successes, and failures
- **Security Events**: Risk assessments and security violations
- **System Events**: Application startup, configuration validation
- **Error Logging**: Detailed error information for debugging

Logs are written to both console and file (`logs/sorae_YYYYMMDD.log`).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Implement your feature
5. Run all tests and quality checks
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the logs for error details
2. Review the configuration settings
3. Run the test suite to verify functionality
4. Create an issue with detailed information about the problem

## 🔮 Future Enhancements

- [ ] Web interface with Flask
- [ ] Database integration for user persistence
- [ ] Real email service integration
- [ ] Advanced biometric authentication
- [ ] Multi-factor authentication support
- [ ] API endpoints for integration
- [ ] Docker containerization
- [ ] Kubernetes deployment support
