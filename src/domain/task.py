from datetime import datetime
from enum import Enum
from typing import Protocol, Any

from pydantic import BaseModel, StringConstraints


class TaskScope(str, Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class TaskStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class Task(BaseModel):
    id: int | None = None
    bot_id: int | None = None
    title: str = StringConstraints(max_length=50)
    channel: str
    scope: TaskScope
    created_at: datetime | None = None
    status: TaskStatus = TaskStatus.NEW


class TaskRepositoryProtocol(Protocol):
    async def add(self, task: Task) -> Task: ...

    async def delete_task_by_id(self, id: int) -> None: ...

    async def get_all_tasks(self) -> list[Task]: ...

    async def update(self, task: Task) -> Task: ...

    async def get_by_fields(self, filters: dict[str, Any]) -> Task | None: ...


class TaskUseCaseProtocol(Protocol):
    async def add(self, task: Task) -> Task: ...

    async def delete_task(self, id: int) -> None: ...

    async def get_all_tasks(self) -> list[Task]: ...

    async def get_task_by_id(self, id: int) -> Task: ...

    async def update_task(self, task: Task) -> Task: ...
