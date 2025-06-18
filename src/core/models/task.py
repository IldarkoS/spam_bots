from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class TaskScope(str, Enum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"


class TaskStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class Task(Base):
    channel: Mapped[str] = mapped_column(nullable=False)
    scope: Mapped[TaskScope] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(
        ForeignKey("bots.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[TaskStatus] = mapped_column(nullable=False)
