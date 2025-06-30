from datetime import datetime

from fastapi import APIRouter
from starlette import status

from src.api.tasks.dto import TaskRead, TaskCreate, TaskUpdate
from src.depends import TaskUseCase

router = APIRouter(prefix="", tags=["Tasks"])


@router.post("/task/", response_model=TaskRead)
async def create_task(task_in: TaskCreate, task_use_case: TaskUseCase):
    entity = await task_use_case.add(task_in.to_entity())
    return TaskRead.from_entity(entity)


@router.delete("/task/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, task_use_case: TaskUseCase):
    await task_use_case.delete_task(task_id)


@router.get("/tasks/", response_model=list[TaskRead])
async def get_list_task(
    task_use_case: TaskUseCase,
):
    tasks = await task_use_case.get_all_tasks()
    return [TaskRead.from_entity(task) for task in tasks]


@router.delete("/task/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, task_use_case: TaskUseCase):
    await task_use_case.delete_task(id=task_id)


@router.patch("/task/{task_id}/", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def patch_task(task_id: int, task_in: TaskUpdate, task_use_case: TaskUseCase):
    entity = task_in.to_entity(task_id)
    entity = await task_use_case.update_task(task=entity)
    return TaskRead.from_entity(entity)

@router.get("/task/{task_id}/", response_model=TaskRead)
async def get_task(task_id: int, task_use_case: TaskUseCase):
    entity = await task_use_case.get_task_by_id(id=task_id)
    return TaskRead.from_entity(entity)