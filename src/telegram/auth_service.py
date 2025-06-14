import logging
import os

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


class AuthService:
    def __init__(self, session_dir: str = "sessions"):
        self.session_dir = session_dir
        os.makedirs(self.session_dir, exist_ok=True)
        self.phone_code_hash_store = dict()

    def _get_session_dir(self, phone: str) -> str:
        return os.path.join(self.session_dir, phone)

    def get_client(self, phone: str, api_id: int, api_hash: str) -> TelegramClient:
        session = self._get_session_dir(phone)
        return TelegramClient(session=session, api_id=api_id, api_hash=api_hash)

    async def request_code(self, phone: str, api_id: int, api_hash: str):
        client = self.get_client(phone, api_id, api_hash)
        await client.connect()
        if await client.is_user_authorized():
            await client.disconnect()
            raise Exception(f"Bot {phone} already authorized")
        code_request = await client.send_code_request(phone)
        self.phone_code_hash_store[phone] = code_request.phone_code_hash
        await client.disconnect()
        logging.info(f"Bot {phone} code sended")

    async def submit_code(self, phone: str, code: str, api_id: int, api_hash: str):
        client = self.get_client(phone, api_id, api_hash)
        await client.connect()
        try:
            await client.sign_in(code=code, phone=phone, phone_code_hash=self.phone_code_hash_store[phone])
            logging.info(f"Bot {phone} code submitted")
            await client.disconnect()
            return "signed_in"
        except SessionPasswordNeededError:
            logging.info(f"Bot {phone} need 2FA")
            await client.disconnect()
            return "password_required"

    async def submit_password(self, phone: str, password: str, api_id: int, api_hash: str):
        client = self.get_client(phone, api_id, api_hash)
        await client.connect()
        await client.sign_in(password=password, phone=phone)
        await client.disconnect()
        logging.info(f"Bot {phone} password submitted")
        return "signed_in"