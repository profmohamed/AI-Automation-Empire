"""
Email sending service using SendGrid
"""
from typing import List, Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from loguru import logger
from app.core.config import settings


class EmailSender:
    """Send emails via SendGrid"""

    def __init__(self):
        if not settings.SENDGRID_API_KEY:
            logger.warning("SendGrid API key not configured")
            self.client = None
        else:
            self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        from_email: Optional[str] = None,
        html_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a single email

        Args:
            to_email: Recipient email
            subject: Email subject
            content: Plain text content
            from_email: Sender email (defaults to settings)
            html_content: Optional HTML content

        Returns:
            Dict with status and message_id
        """
        if not self.client:
            logger.error("SendGrid client not initialized")
            return {"status": "error", "message": "SendGrid not configured"}

        try:
            from_email = from_email or settings.EMAIL_FROM
            if not from_email:
                return {"status": "error", "message": "From email not configured"}

            message = Mail(
                from_email=Email(from_email),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", content),
            )

            if html_content:
                message.add_content(Content("text/html", html_content))

            response = self.client.send(message)

            logger.info(f"Email sent to {to_email}, status: {response.status_code}")

            return {
                "status": "sent",
                "status_code": response.status_code,
                "message_id": response.headers.get("X-Message-Id"),
                "to": to_email,
            }

        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return {
                "status": "error",
                "message": str(e),
                "to": to_email,
            }

    async def send_bulk_emails(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        content_template: str,
        from_email: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Send bulk personalized emails

        Args:
            recipients: List of dicts with 'email' and 'name' keys
            subject: Email subject (can include {{name}} placeholder)
            content_template: Email template (can include {{name}} and other placeholders)
            from_email: Sender email

        Returns:
            List of send results
        """
        results = []

        for recipient in recipients:
            email = recipient.get("email")
            name = recipient.get("name", "")

            # Personalize content
            personalized_content = content_template.replace("{{name}}", name)
            personalized_subject = subject.replace("{{name}}", name)

            result = await self.send_email(
                to_email=email,
                subject=personalized_subject,
                content=personalized_content,
                from_email=from_email,
            )

            results.append(result)

        return results

    async def send_proposal_email(
        self,
        to_email: str,
        client_name: str,
        proposal_content: str,
        subject: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a proposal email"""
        if not subject:
            subject = f"Proposal for Your Project"

        email_body = f"""Hi {client_name},

I came across your project and I'm excited about the opportunity to help.

{proposal_content}

I'd love to discuss this further. When would be a good time to chat?

Best regards"""

        return await self.send_email(
            to_email=to_email,
            subject=subject,
            content=email_body,
        )
