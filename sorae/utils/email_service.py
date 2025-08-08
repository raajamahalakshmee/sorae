import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from utils.logger import logger

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_from = os.getenv('EMAIL_FROM', 'noreply@sorae.com')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.email_subject = os.getenv('EMAIL_SUBJECT', 'Your Sorae Magic Link')
    
    def send_magic_link(self, email: str, token: str) -> bool:
        """Send a real magic link email."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = email
            msg['Subject'] = self.email_subject
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>🔐 Your Sorae Magic Link</h2>
                <p>Hello!</p>
                <p>You requested to log in to your Sorae account. Use the token below to complete your login:</p>
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 2px;">
                    {token}
                </div>
                <p><strong>This token will expire in 15 minutes.</strong></p>
                <p>If you didn't request this login, please ignore this email.</p>
                <p>Best regards,<br>The Sorae Team</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            if self.email_password:  # Only send if password is configured
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
                server.quit()
                
                logger.info(f"Magic link email sent to {email}")
                return True
            else:
                # Fallback to simulator if no email credentials
                logger.warning("No email password configured, falling back to simulator")
                return self._simulate_email(email, token)
                
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return self._simulate_email(email, token)
    
    def _simulate_email(self, email: str, token: str) -> bool:
        """Fallback email simulator."""
        print(f"📧 [Sorae Email Simulator] Magic login link sent to {email}:")
        print(f"    Use this token to login: {token}")
        return True

# Create global email service instance
email_service = EmailService()
