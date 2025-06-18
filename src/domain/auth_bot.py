from typing import Protocol

from src.domain.bot import Bot


class AuthBotUseCaseProtocol(Protocol):
    async def request_code(self, bot: Bot): ...

    async def submit_code(self, bot: Bot, code: str): ...

    async def submit_password(self, bot: Bot, password: str): ...
