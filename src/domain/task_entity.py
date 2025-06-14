from datetime import datetime
from enum import Enum
from typing import Protocol

from pydantic import BaseModel


class TaskType(str, Enum):
    SINGLE = "SINGLE"
    SUBSCRIBE = "SUBSCRIBE"


class TaskScope(str, Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class Task(BaseModel):
    id: int | None = None
    bot_id: int | None = None
    post_id: int | None = None
    channel: str
    type: TaskType
    scope: TaskScope
    created_at: datetime | None = None


class TaskRepositoryProtocol(Protocol):
    async def add(self, task: Task) -> Task: ...

    async def get_task_by_id(self, id: int) -> Task | None: ...

    async def delete_task_by_id(self, id: int) -> None: ...

    async def get_all_tasks(self) -> list[Task]: ...


class TaskUseCaseProtocol(Protocol):
    async def add(self, task: Task) -> Task: ...

    async def delete_task(self, id: int) -> None: ...

    async def get_all_tasks(self) -> list[Task]: ...

    async def get_task_by_id(self, id: int) -> Task: ...
