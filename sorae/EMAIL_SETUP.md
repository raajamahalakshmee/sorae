# Email Setup Guide for Sorae

This guide will help you configure real email functionality for the Sorae authentication system.

## 🔧 Setup Options

### Option 1: Gmail SMTP (Recommended for testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Set Environment Variables**:

```bash
# Windows PowerShell
$env:EMAIL_FROM="your-email@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"

# Windows Command Prompt
set EMAIL_FROM=your-email@gmail.com
set EMAIL_PASSWORD=your-app-password
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587

# Linux/Mac
export EMAIL_FROM="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

### Option 2: Outlook/Hotmail SMTP

```bash
# Windows PowerShell
$env:EMAIL_FROM="your-email@outlook.com"
$env:EMAIL_PASSWORD="your-password"
$env:SMTP_SERVER="smtp-mail.outlook.com"
$env:SMTP_PORT="587"
```

### Option 3: Custom SMTP Server

```bash
# Windows PowerShell
$env:EMAIL_FROM="noreply@yourdomain.com"
$env:EMAIL_PASSWORD="your-smtp-password"
$env:SMTP_SERVER="smtp.yourdomain.com"
$env:SMTP_PORT="587"
```

## 🚀 Testing the Setup

1. **Set your environment variables** (see options above)
2. **Run the application**:
   ```bash
   python main.py
   ```
3. **Enter your email** during onboarding
4. **Check your inbox** for the magic link email

## 🔍 Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check your email and password
   - Ensure 2FA is enabled for Gmail
   - Use App Password, not your regular password

2. **"Connection refused"**
   - Check SMTP server and port
   - Ensure firewall allows SMTP connections
   - Try different ports (587, 465, 25)

3. **"No email received"**
   - Check spam folder
   - Verify email address is correct
   - Check SMTP credentials

### Debug Mode:

To see detailed email sending logs, the system will automatically log all email operations. Check the console output for any error messages.

## 🔒 Security Notes

- **Never commit email passwords** to version control
- **Use environment variables** for sensitive data
- **Consider using a dedicated email service** for production
- **Enable 2FA** on your email account
- **Use App Passwords** instead of regular passwords

## 📧 Email Template

The system sends HTML emails with:
- Professional styling
- Clear token display
- Security warnings
- Expiration information

## 🎯 Current Status

- ✅ **Email service implemented**
- ✅ **SMTP configuration support**
- ✅ **Fallback to simulator** if email fails
- ✅ **Comprehensive error handling**
- ✅ **Security best practices**

## 🚀 Next Steps

1. **Configure your email settings** (see options above)
2. **Test the email functionality**
3. **Run the application** and try the full flow
4. **Check your inbox** for magic link emails

The system will automatically fall back to the simulator if email configuration is not set up, so you can still test the functionality!
