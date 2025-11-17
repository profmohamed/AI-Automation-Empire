"""
Telegram bot for notifications and outreach
"""
from typing import Dict, Any
from loguru import logger
from app.core.config import settings


class TelegramBot:
    """Telegram bot for sending messages"""

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.bot = None

        if self.token:
            try:
                # Import here to make it optional
                from telegram import Bot
                self.bot = Bot(token=self.token)
            except ImportError:
                logger.warning("python-telegram-bot not installed")

    async def send_message(
        self,
        chat_id: str,
        message: str,
        parse_mode: str = "Markdown",
    ) -> Dict[str, Any]:
        """Send message to Telegram chat"""
        if not self.bot:
            return {"status": "error", "message": "Telegram bot not configured"}

        try:
            result = await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )

            logger.info(f"Telegram message sent to {chat_id}")

            return {
                "status": "sent",
                "message_id": result.message_id,
                "chat_id": chat_id,
            }

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return {
                "status": "error",
                "message": str(e),
            }

    async def send_notification(
        self,
        chat_id: str,
        title: str,
        message: str,
    ) -> Dict[str, Any]:
        """Send formatted notification"""
        formatted_message = f"*{title}*\n\n{message}"
        return await self.send_message(chat_id, formatted_message)
