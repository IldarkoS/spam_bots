from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.task import Task as TaskModel
from src.domain.task import Task as TaskEntity
from src.domain.task import TaskRepositoryProtocol


class TaskRepositoryImpl(TaskRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _entity_to_orm(entity: TaskEntity) -> TaskModel:
        return TaskModel(**entity.model_dump(exclude_none=True))

    @staticmethod
    def _orm_to_entity(orm: TaskModel) -> TaskEntity:
        return TaskEntity.model_validate(orm, from_attributes=True)

    async def add(self, task: TaskEntity) -> TaskEntity:
        orm = self._entity_to_orm(task)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._orm_to_entity(orm)

    async def get_task_by_id(self, id: int) -> TaskEntity | None:
        stmt = select(TaskModel).where(TaskModel.id == id)
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._orm_to_entity(orm) if orm else None

    async def delete_task_by_id(self, id: int) -> None:
        stmt = delete(TaskModel).where(TaskModel.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_all_tasks(self) -> list[TaskEntity]:
        stmt = select(TaskModel).order_by(TaskModel.id)
        result = await self.session.execute(stmt)
        orms = result.scalars().all()
        return [self._orm_to_entity(orm) for orm in orms]

    async def update(self, task: TaskEntity) -> TaskEntity:
        stmt = (
            update(TaskModel)
            .where(TaskModel.id == task.id)
            .values(**task.model_dump(exclude_none=True))
            .returning(TaskModel)
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        await self.session.commit()
        return self._orm_to_entity(orm)
