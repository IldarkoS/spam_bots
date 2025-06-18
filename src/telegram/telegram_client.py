import os.path

from telethon import TelegramClient

from src.config import settings
from src.domain.bot import Bot


def get_telegram_client(bot: Bot) -> TelegramClient:
    session_path = os.path.join(settings.SESSIONS_DIR, bot.phone)
    return TelegramClient(
        session=session_path,
        api_id=bot.api_id,
        api_hash=bot.api_hash,
    )
