from datetime import datetime
from typing import Protocol

from pydantic import BaseModel


class Bot(BaseModel):
    id: int | None = None
    api_id: int
    api_hash: str
    name: str
    phone: str
    is_active: bool = True
    last_seen: datetime | None = None
    created_at: datetime | None = None


class BotRepositoryProtocol(Protocol):
    async def add(self, bot: Bot) -> Bot: ...

    async def delete(self, id: int) -> None: ...

    async def get_by_id(self, id: int) -> Bot | None: ...

    async def update(self, bot: Bot) -> Bot: ...

    async def get_all(self) -> list[Bot]: ...


class BotUseCaseProtocol(Protocol):
    async def create(self, bot: Bot) -> Bot: ...

    async def delete(self, id: int) -> None: ...

    async def get_by_id(self, id: int) -> Bot: ...

    async def update(self, bot: Bot) -> Bot: ...

    async def get_all(self) -> list[Bot]: ...
