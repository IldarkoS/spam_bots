from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func

from src.core.models.base import Base


class TaskType(Enum):
    SINGLE = "SINGLE"
    SUBSCRIBE = "SUBSCRIBE"


class TaskScope(Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class TaskStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class Task(Base):
    channel: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(nullable=True)
    type: Mapped[TaskType] = mapped_column(nullable=False)
    scope: Mapped[TaskScope] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[TaskStatus] = mapped_column(nullable=False)
