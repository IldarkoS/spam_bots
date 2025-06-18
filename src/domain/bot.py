from datetime import datetime
from typing import Protocol, Any

from pydantic import BaseModel, Field


class QueryParams(BaseModel):
    offset: int | None = Field(0, ge=0)
    limit: int | None = Field(20, ge=0, le=100)


class Bot(BaseModel):
    id: int | None = None
    api_id: int
    api_hash: str
    name: str
    phone: str
    phone_code_hash: str | None = None
    is_active: bool = False
    is_authorized: bool = False
    created_at: datetime | None = None


class BotRepositoryProtocol(Protocol):
    async def create(self, bot: Bot) -> Bot: ...

    async def delete(self, id: int) -> None: ...

    async def get_by_fields(self, filters: dict[str, Any]) -> Bot | None: ...

    async def update(self, bot: Bot) -> Bot: ...

    async def get_all_bots(self, params: QueryParams) -> list[Bot]: ...


class BotUseCaseProtocol(Protocol):
    async def create_bot(self, bot: Bot) -> Bot: ...

    async def delete_bot(self, id: int) -> None: ...

    async def get_bot_by_field(self, filters: dict[str, Any]) -> Bot | None: ...

    async def update_bot(self, bot: Bot) -> Bot: ...

    async def get_bots_list(self, params: QueryParams) -> list[Bot]: ...

    async def get_bot_by_id(self, id: int) -> Bot: ...
