from typing import Any

from sqlalchemy import select, Result, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.bot import Bot as BotModel
from src.domain.bot import BotRepositoryProtocol, Bot as BotEntity, QueryParams
from src.exceptions import InvalidFilterFieldException


class BotRepositoryImpl(BotRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _entity_to_orm(entity: BotEntity) -> BotModel:
        return BotModel(**entity.model_dump(exclude_none=True))

    @staticmethod
    def _orm_to_entity(orm: BotModel) -> BotEntity:
        return BotEntity.model_validate(orm, from_attributes=True)

    async def create(self, bot: BotEntity) -> BotEntity:
        orm = self._entity_to_orm(bot)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._orm_to_entity(orm)

    async def delete(self, id: int) -> None:
        stmt = delete(BotModel).where(BotModel.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_fields(self, filters: dict[str, Any]) -> BotEntity | None:
        stmt = select(BotModel)

        for field, value in filters.items():
            if not hasattr(BotModel, field):
                raise InvalidFilterFieldException(field)
            stmt = stmt.where(getattr(BotModel, field) == value)

        result: Result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._orm_to_entity(orm) if orm else None

    async def update(self, bot: BotEntity) -> BotEntity:
        stmt = (
            update(BotModel)
            .where(BotModel.id == bot.id)
            .values(**bot.model_dump(exclude_none=True))
            .returning(BotModel)
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        await self.session.commit()
        return self._orm_to_entity(orm)

    async def get_all_bots(self, params: QueryParams) -> list[BotEntity]:
        stmt = select(BotModel)
        if params.limit is not None:
            stmt = stmt.limit(params.limit)
        if params.offset is not None:
            stmt = stmt.offset(params.offset)

        result: Result = await self.session.execute(stmt)
        orms = result.scalars().all()
        return [self._orm_to_entity(orm) for orm in orms]
