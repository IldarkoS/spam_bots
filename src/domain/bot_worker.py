from typing import Protocol

from src.domain.bot import Bot


class BotWorkerUseCaseProtocol(Protocol):
    async def run(self): ...
