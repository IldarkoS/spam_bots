from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from src.domain.task_entity import Task


class TaskType(str, Enum):
    SINGLE = "SINGLE"
    SUBSCRIBE = "SUBSCRIBE"


class TaskScope(str, Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class TaskCreateRequest(BaseModel):
    channel: str
    post_id: int | None = None
    type: TaskType
    scope: TaskScope
    bot_id: int | None = None

    def to_entity(self) -> Task:
        return Task(
            channel=self.channel,
            post_id=self.post_id,
            type=self.type,
            scope=self.scope,
            bot_id=self.bot_id,
        )


class TaskCreateResponse(TaskCreateRequest):
    id: int
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Task):
        return cls(
            id=entity.id,
            created_at=entity.created_at,
            scope=entity.scope,
            type=entity.type,
            bot_id=entity.bot_id,
            channel=entity.channel,
            post_id=entity.post_id,
        )
