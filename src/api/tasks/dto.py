from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from src.domain.task import Task


class TaskScope(str, Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class TaskStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class TaskCreate(BaseModel):
    channel: str
    scope: TaskScope
    bot_id: int | None = None

    def to_entity(self) -> Task:
        return Task(
            channel=self.channel,
            scope=self.scope,
            bot_id=self.bot_id,
        )


class TaskRead(TaskCreate):
    id: int
    created_at: datetime
    status: TaskStatus

    @classmethod
    def from_entity(cls, entity: Task):
        return cls(
            id=entity.id,
            created_at=entity.created_at,
            scope=entity.scope,
            bot_id=entity.bot_id,
            channel=entity.channel,
            status=entity.status,
        )
