from datetime import datetime

from pydantic import BaseModel

from src.domain.entity import Bot


class BotCreateRequest(BaseModel):
    api_id: int
    api_hash: str
    name: str
    phone: str

    def to_entity(self) -> Bot:
        return Bot(
            api_id=self.api_id,
            api_hash=self.api_hash,
            name=self.name,
            phone=self.phone,
        )


class BotCreateResponse(BaseModel):
    id: int
    api_id: int
    api_hash: str
    name: str
    phone: str
    is_active: bool
    last_seen: datetime | None
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Bot):
        return cls(
            id=entity.id,
            api_id=entity.api_id,
            api_hash=entity.api_hash,
            name=entity.name,
            phone=entity.phone,
            is_active=entity.is_active,
            last_seen=entity.last_seen,
            created_at=entity.created_at,
        )


class BotUpdateRequest(BaseModel):
    api_id: int
    api_hash: str
    name: str
    phone: str
    is_active: bool

    def to_entity(self, bot_id: int) -> Bot:
        return Bot(
            id=bot_id,
            api_id=self.api_id,
            api_hash=self.api_hash,
            name=self.name,
            phone=self.phone,
            is_active=self.is_active,
        )
