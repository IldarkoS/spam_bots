from fastapi import HTTPException, status


class BotError(HTTPException): ...


class BotNotFoundError(BotError):
    def __init__(self, bot_id=None):
        message = (
            "Bot not found" if bot_id is None else f"Bot with ID: {bot_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class BotAlreadyExistsError(BotError):
    def __init__(self):
        message = "Bot already exists"
        super().__init__(status_code=status.HTTP_201_CREATED, detail=message)


class TaskError(HTTPException): ...


class TaskAlreadyExistsError(TaskError):
    def __init__(self):
        message = "Task already exists"
        super().__init__(status_code=status.HTTP_201_CREATED, detail=message)


class TaskNotFoundError(TaskError):
    def __init__(self, task_id=None):
        message = (
            "Task not found"
            if task_id is None
            else f"Task with ID: {task_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class InvalidFilterFieldException(Exception):
    def __init__(self, field: str):
        super().__init__(f"Invalid filter field: '{field}' does not exist")


