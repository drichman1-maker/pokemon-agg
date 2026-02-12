import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.client = None
        if settings.SENDGRID_API_KEY:
            self.client = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        else:
            logger.warning("SendGrid API key not configured - email service disabled")

    def send_email(self, to_email: str, subject: str, content_str: str) -> bool:
        if not self.client:
            logger.error("SendGrid not configured - cannot send email")
            raise RuntimeError("Email service not configured")
            
        from_email = Email(settings.EMAIL_FROM)
        to_email_obj = To(to_email)
        content = Content("text/plain", content_str)
        mail = Mail(from_email, to_email_obj, subject, content)
        
        try:
            response = self.client.mail.send.post(request_body=mail.get())
            success = 200 <= response.status_code < 300
            
            if success:
                logger.info(f"Email sent successfully to {to_email}")
            else:
                logger.error(f"Email send failed with status {response.status_code}")
                raise RuntimeError(f"Email send failed: HTTP {response.status_code}")
            
            return success
        except Exception as e:
            logger.error(f"Email send error: {e}")
            raise RuntimeError(f"Failed to send email: {str(e)}")
