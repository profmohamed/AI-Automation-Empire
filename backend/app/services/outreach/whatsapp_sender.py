"""
WhatsApp messaging via Twilio
"""
from typing import Dict, Any
from twilio.rest import Client
from loguru import logger
from app.core.config import settings


class WhatsAppSender:
    """Send WhatsApp messages via Twilio"""

    def __init__(self):
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            logger.warning("Twilio credentials not configured")
            self.client = None
        else:
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    async def send_message(
        self,
        to_number: str,
        message: str,
        media_url: str = None,
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message

        Args:
            to_number: Recipient phone number (format: whatsapp:+1234567890)
            message: Message content
            media_url: Optional media URL

        Returns:
            Dict with status and message_sid
        """
        if not self.client:
            return {"status": "error", "message": "Twilio not configured"}

        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"

            from_number = settings.TWILIO_WHATSAPP_NUMBER
            if not from_number.startswith("whatsapp:"):
                from_number = f"whatsapp:{from_number}"

            message_kwargs = {
                "body": message,
                "from_": from_number,
                "to": to_number,
            }

            if media_url:
                message_kwargs["media_url"] = [media_url]

            msg = self.client.messages.create(**message_kwargs)

            logger.info(f"WhatsApp message sent to {to_number}, SID: {msg.sid}")

            return {
                "status": "sent",
                "message_sid": msg.sid,
                "to": to_number,
            }

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return {
                "status": "error",
                "message": str(e),
                "to": to_number,
            }
