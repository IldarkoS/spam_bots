from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.bot import Bot


class FilterParams(BaseModel):
    offset: int | None = Field(0, ge=0)
    limit: int | None = Field(20, ge=0, le=100)


class BotCreate(BaseModel):
    api_id: int
    api_hash: str
    phone: str
    name: str

    def to_entity(self) -> Bot:
        return Bot(
            api_id=self.api_id,
            api_hash=self.api_hash,
            name=self.name,
            phone=self.phone,
        )


class BotRead(BaseModel):
    id: int
    name: str
    phone: str
    is_active: bool
    is_authorized: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Bot):
        return cls(
            id=entity.id,
            name=entity.name,
            phone=entity.phone,
            is_active=entity.is_active,
            is_authorized=entity.is_authorized,
            created_at=entity.created_at,
        )


class BotUpdate(BotCreate):

    def to_entity(self, bot_id) -> Bot:
        return Bot(
            id=bot_id,
            api_id=self.api_id,
            api_hash=self.api_hash,
            name=self.name,
            phone=self.phone,
        )
