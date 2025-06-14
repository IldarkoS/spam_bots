from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.bot_repository import BotRepositoryImpl
from src.core.db import db_helper
from src.domain.entity import BotRepositoryProtocol, BotUseCaseProtocol
from src.service.bot_use_case import BotUseCaseImpl

Session = Annotated[AsyncSession, Depends(db_helper.session_dependency)]


def get_bot_repository(session: Session) -> BotRepositoryProtocol:
    return BotRepositoryImpl(session=session)


BotRepository = Annotated[BotRepositoryProtocol, Depends(get_bot_repository)]


def get_bot_use_case(repository: BotRepository) -> BotUseCaseProtocol:
    return BotUseCaseImpl(repository=repository)


BotUseCase = Annotated[BotUseCaseProtocol, Depends(get_bot_use_case)]
