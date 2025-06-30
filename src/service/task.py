from src.domain.task import TaskUseCaseProtocol, TaskRepositoryProtocol, Task
from src.exceptions import TaskAlreadyExistsError, TaskNotFoundError


class TaskUseCaseImpl(TaskUseCaseProtocol):
    def __init__(self, repository: TaskRepositoryProtocol):
        self.repository = repository

    async def add(self, task: Task) -> Task:
        exist = await self.repository.get_by_fields(
            {
                "title": task.title,
                "channel": task.channel,
            }
        )
        if exist:
            raise TaskAlreadyExistsError()
        return await self.repository.add(task)

    async def delete_task(self, id: int) -> None:
        await self.repository.delete_task_by_id(id=id)

    async def get_all_tasks(self) -> list[Task]:
        return await self.repository.get_all_tasks()

    async def get_task_by_id(self, id: int) -> Task:
        task = await self.repository.get_by_fields(
            {
                "id": id,
            }
        )
        if not task:
            raise TaskNotFoundError(task_id=id)
        return task

    async def update_task(self, task: Task) -> Task:
        exist = await self.get_task_by_id(id=task.id)
        return await self.repository.update(task=task)
