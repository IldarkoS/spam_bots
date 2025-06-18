from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.bot_repository import BotRepositoryImpl
from src.adapters.task_repository import TaskRepositoryImpl
from src.core.db import db_helper
from src.domain.auth_bot import AuthBotUseCaseProtocol
from src.domain.bot import BotRepositoryProtocol, BotUseCaseProtocol
from src.domain.bot_manager import BotManagerUseCaseProtocol
from src.domain.comment_generator import CommentGeneratorProtocol
from src.domain.task import TaskRepositoryProtocol, TaskUseCaseProtocol
from src.service.auth_bot import AuthBotUseCaseImpl
from src.service.bot import BotUseCaseImpl
from src.service.bot_manager import BotManagerUseCaseImpl
from src.service.comment_generator import CommentGeneratorImpl
from src.service.task import TaskUseCaseImpl

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


def get_auth_bot_use_case(bot_repository: BotRepository) -> AuthBotUseCaseProtocol:
    return AuthBotUseCaseImpl(bot_repository=bot_repository)


AuthBotUseCase = Annotated[AuthBotUseCaseProtocol, Depends(get_auth_bot_use_case)]


def get_comment_generator() -> CommentGeneratorProtocol:
    return CommentGeneratorImpl()


CommentGenerator = Annotated[CommentGeneratorProtocol, Depends(get_comment_generator)]


def get_bot_manager_use_case(
    bot_repository: BotRepository,
    task_repository: TaskRepository,
    comment_generator: CommentGenerator,
) -> BotManagerUseCaseProtocol:
    return BotManagerUseCaseImpl(
        bot_repository=bot_repository,
        task_repository=task_repository,
        comment_generator=comment_generator,
    )


BotManagerUseCase = Annotated[
    BotManagerUseCaseProtocol, Depends(get_bot_manager_use_case)
]
