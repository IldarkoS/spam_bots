from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.bot_repository import BotRepositoryImpl
from src.adapters.task_repository import TaskRepositoryImpl
from src.core.db import db_helper
from src.domain.bot_entity import BotRepositoryProtocol, BotUseCaseProtocol
from src.domain.task_entity import TaskRepositoryProtocol, TaskUseCaseProtocol
from src.service.bot_use_case import BotUseCaseImpl
from src.service.task_use_case import TaskUseCaseImpl

Session = Annotated[AsyncSession, Depends(db_helper.session_dependency)]


def get_bot_repository(session: Session) -> BotRepositoryProtocol:
    return BotRepositoryImpl(session=session)


BotRepository = Annotated[BotRepositoryProtocol, Depends(get_bot_repository)]


def get_bot_use_case(repository: BotRepository) -> BotUseCaseProtocol:
    return BotUseCaseImpl(repository=repository)


BotUseCase = Annotated[BotUseCaseProtocol, Depends(get_bot_use_case)]


def get_task_repository(session: Session) -> TaskRepositoryProtocol:
    return TaskRepositoryImpl(session=session)


TaskRepository = Annotated[TaskRepositoryProtocol, Depends(get_task_repository)]


def get_task_use_case(repository: TaskRepository) -> TaskUseCaseProtocol:
    return TaskUseCaseImpl(repository=repository)


TaskUseCase = Annotated[TaskUseCaseProtocol, Depends(get_task_use_case)]
