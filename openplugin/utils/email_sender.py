"""Email sending utility for email plugin."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import os


class EmailSender:
    """Handles email sending via SMTP."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: int = 587,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
        use_tls: bool = True
    ):
        """Initialize email sender.
        
        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port (default: 587)
            smtp_username: SMTP username (email address)
            smtp_password: SMTP password
            use_tls: Use TLS encryption (default: True)
        """
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = smtp_username or os.getenv("SMTP_USERNAME")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.use_tls = use_tls

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        is_html: bool = False
    ) -> Dict[str, Any]:
        """Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            from_email: Sender email (defaults to smtp_username)
            is_html: Whether body is HTML (default: False)
            
        Returns:
            Dictionary with success status and message
            
        Raises:
            ValueError: If email configuration is invalid
            smtplib.SMTPException: If sending fails
        """
        if not self.smtp_username or not self.smtp_password:
            raise ValueError("SMTP credentials not configured. Set SMTP_USERNAME and SMTP_PASSWORD environment variables.")
        
        from_email = from_email or self.smtp_username
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = subject
        
        # Add body
        part = MIMEText(body, 'html' if is_html else 'plain')
        msg.attach(part)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to}",
                "to": to,
                "subject": subject
            }
        except smtplib.SMTPException as e:
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}",
                "error": str(e)
            }
