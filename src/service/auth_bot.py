import logging
import os

from telethon import TelegramClient
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    PasswordHashInvalidError,
)

from src.config import settings
from src.domain.auth_bot import AuthBotUseCaseProtocol
from src.domain.bot import Bot, BotRepositoryProtocol
from src.exceptions import (
    CodeNotRequestedError,
    InvalidPhoneError,
    InvalidCodeError,
    CodeExpiredError,
    InvalidPasswordError,
)


class AuthBotUseCaseImpl(AuthBotUseCaseProtocol):
    def __init__(
        self,
        bot_repository: BotRepositoryProtocol,
        session_dir: str = settings.SESSIONS_DIR,
    ):
        self.session_dir = session_dir
        os.makedirs(self.session_dir, exist_ok=True)
        self.phone_code_hash_store = dict()
        self.bot_repository = bot_repository

    def _get_client(self, bot: Bot) -> TelegramClient:
        session = self._get_session_dir(bot.phone)
        return TelegramClient(session=session, api_id=bot.api_id, api_hash=bot.api_hash)

    def _get_session_dir(self, phone: str) -> str:
        return os.path.join(self.session_dir, phone)

    async def _authorize(self, bot: Bot):
        bot.is_authorized = True
        await self.bot_repository.update(bot=bot)

    async def request_code(self, bot: Bot):
        client = self._get_client(bot=bot)
        await client.connect()
        try:
            if await client.is_user_authorized():
                await client.disconnect()
                raise Exception(f"Bot ({bot.name}:{bot.phone}) already authorized")
            code_request = await client.send_code_request(bot.phone)
            bot.phone_code_hash = code_request.phone_code_hash
            await self.bot_repository.update(bot=bot)
            logging.info(f"Bot ({bot.name}:{bot.phone}) code sended")
        except PhoneNumberInvalidError:
            raise InvalidPhoneError()
        finally:
            await client.disconnect()

    async def submit_code(self, bot: Bot, code: str):
        client = self._get_client(bot=bot)
        await client.connect()
        try:
            await client.sign_in(
                phone=bot.phone,
                code=code,
                phone_code_hash=bot.phone_code_hash,
            )
            logging.info(f"Bot ({bot.name}:{bot.phone}) code submitted")
            await self._authorize(bot=bot)
            return "Signed in"
        except SessionPasswordNeededError:
            logging.info(f"Bot ({bot.name}:{bot.phone}) need 2FA")
            return "Password required"
        except PhoneCodeInvalidError:
            raise InvalidCodeError()
        except PhoneCodeExpiredError:
            raise CodeExpiredError()
        finally:
            await client.disconnect()

    async def submit_password(self, bot: Bot, password: str):
        client = self._get_client(bot=bot)
        await client.connect()
        try:
            await client.sign_in(
                phone=bot.phone,
                password=password,
            )
            logging.info(f"Bot ({bot.name}:{bot.phone}) password submitted")
            await self._authorize(bot=bot)
            return "Signed in"
        except PasswordHashInvalidError:
            raise InvalidPasswordError()
        finally:
            await client.disconnect()
